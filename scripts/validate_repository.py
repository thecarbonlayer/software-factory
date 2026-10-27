#!/usr/bin/env python3
"""Validate Software Factory packaging and repository hygiene."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote


PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
SHARED_MANIFEST_FIELDS = ("name", "version", "description")
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLUGIN_NAME_PATTERN = re.compile(
    r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"
)
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKILL_REFERENCE_PATTERN = re.compile(r"software-factory:([a-z0-9]+(?:-[a-z0-9]+)*)")
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
LOCAL_PATH_PATTERNS = (
    re.compile(r"/" + r"Users/[^/\s]+/"),
    re.compile(r"/" + r"home/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\" + r"Users\\[^\\\s]+\\", re.IGNORECASE),
)


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing required JSON file: {path}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}")
        return None

    if not isinstance(value, dict):
        errors.append(f"JSON root must be an object: {path}")
        return None
    return value


def parse_semver(value: object) -> tuple[tuple[int, int, int], list[str] | None] | None:
    if not isinstance(value, str):
        return None
    match = SEMVER_PATTERN.fullmatch(value)
    if not match:
        return None
    core = tuple(int(part) for part in match.group(1, 2, 3))
    prerelease = match.group(4).split(".") if match.group(4) else None
    return core, prerelease


def prerelease_is_greater(current: list[str], base: list[str]) -> bool:
    for current_part, base_part in zip(current, base):
        if current_part == base_part:
            continue
        current_numeric = current_part.isdigit()
        base_numeric = base_part.isdigit()
        if current_numeric and base_numeric:
            return int(current_part) > int(base_part)
        if current_numeric != base_numeric:
            return not current_numeric
        return current_part > base_part
    return len(current) > len(base)


def semver_is_greater(current: object, base: object) -> bool:
    current_version = parse_semver(current)
    base_version = parse_semver(base)
    if current_version is None or base_version is None:
        return False

    current_core, current_prerelease = current_version
    base_core, base_prerelease = base_version
    if current_core != base_core:
        return current_core > base_core
    if current_prerelease is None:
        return base_prerelease is not None
    if base_prerelease is None:
        return False
    return prerelease_is_greater(current_prerelease, base_prerelease)


def repository_files(root: Path) -> list[Path]:
    command = [
        "git",
        "-C",
        str(root),
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
    ]
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode == 0:
        return sorted(
            root / Path(item.decode("utf-8"))
            for item in result.stdout.split(b"\0")
            if item
        )
    return sorted(path for path in root.rglob("*") if path.is_file())


def extract_frontmatter(path: Path, errors: list[str]) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"skill must begin with YAML frontmatter: {path}")
        return None

    try:
        closing_line = lines.index("---", 1)
    except ValueError:
        errors.append(f"skill frontmatter is not closed: {path}")
        return None

    values: dict[str, str] = {}
    for line in lines[1:closing_line]:
        if not line or line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if key not in {"name", "description"}:
            continue
        if key in values:
            errors.append(f"duplicate skill frontmatter field '{key}': {path}")
            continue
        value = raw_value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value

    if not any(line.strip() for line in lines[closing_line + 1 :]):
        errors.append(f"skill instructions are empty: {path}")
    return values


def validate_manifests(root: Path, errors: list[str]) -> dict[str, Any] | None:
    portable_path = root / "plugin.json"
    client_path = root / ".claude-plugin" / "plugin.json"
    portable = load_json(portable_path, errors)
    client = load_json(client_path, errors)
    if portable is None or client is None:
        return portable

    unknown_fields = sorted(set(portable) - PLUGIN_FIELDS)
    if unknown_fields:
        errors.append(
            f"unsupported plugin.json fields: {', '.join(unknown_fields)}"
        )

    if portable.get("$schema") != PLUGIN_SCHEMA:
        errors.append(f"plugin.json must use schema {PLUGIN_SCHEMA}")

    plugin_name = portable.get("name")
    if not isinstance(plugin_name, str) or not (1 <= len(plugin_name) <= 64):
        errors.append("plugin.json name must contain 1 to 64 characters")
    elif not PLUGIN_NAME_PATTERN.fullmatch(plugin_name):
        errors.append("plugin.json name does not follow the Agent Plugins name format")

    if parse_semver(portable.get("version")) is None:
        errors.append("plugin.json version must be a semantic version")
    description = portable.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("plugin.json description must be a non-empty string")

    for field in SHARED_MANIFEST_FIELDS:
        if portable.get(field) != client.get(field):
            errors.append(
                f"manifest field '{field}' must match in plugin.json and "
                ".claude-plugin/plugin.json"
            )
    return portable


def validate_skills(root: Path, errors: list[str]) -> set[str]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        errors.append("missing required skills directory")
        return set()

    skill_names: set[str] = set()
    skill_directories = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not skill_directories:
        errors.append("skills directory contains no skills")

    for directory in skill_directories:
        path = directory / "SKILL.md"
        if not path.is_file():
            errors.append(f"skill directory is missing SKILL.md: {directory}")
            continue
        frontmatter = extract_frontmatter(path, errors)
        if frontmatter is None:
            continue

        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if not SKILL_NAME_PATTERN.fullmatch(name) or len(name) > 64:
            errors.append(f"invalid Agent Skills name '{name}' in {path}")
        if name != directory.name:
            errors.append(
                f"skill name '{name}' must match its directory '{directory.name}': {path}"
            )
        if name in skill_names:
            errors.append(f"duplicate skill name '{name}': {path}")
        skill_names.add(name)

        if not description:
            errors.append(f"skill description must be non-empty: {path}")
        elif len(description) > 1024:
            errors.append(f"skill description exceeds 1024 characters: {path}")

    return skill_names


def markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def validate_markdown_links(root: Path, files: Iterable[Path], errors: list[str]) -> None:
    resolved_root = root.resolve()
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_PATTERN.finditer(text):
            target = markdown_target(match.group(1))
            if (
                not target
                or target.startswith("#")
                or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target)
                or "{" in target
            ):
                continue
            path_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not path_part:
                continue
            candidate = (path.parent / path_part).resolve()
            try:
                candidate.relative_to(resolved_root)
            except ValueError:
                errors.append(f"relative link escapes the plugin root in {path}: {target}")
                continue
            if not candidate.exists():
                errors.append(f"broken relative link in {path}: {target}")


def validate_local_paths(files: Iterable[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(text) for pattern in LOCAL_PATH_PATTERNS):
            errors.append(f"local workstation path found in public file: {path}")


def validate_skill_references(
    files: Iterable[Path], skill_names: set[str], errors: list[str]
) -> None:
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for referenced_name in SKILL_REFERENCE_PATTERN.findall(text):
            if referenced_name not in skill_names:
                errors.append(
                    f"unknown native skill reference 'software-factory:{referenced_name}' "
                    f"in {path}"
                )


def validate_version_bump(
    portable_manifest: dict[str, Any] | None,
    base_manifest: dict[str, Any] | None,
    changed_paths: set[str] | None,
    errors: list[str],
) -> None:
    if portable_manifest is None or base_manifest is None or changed_paths is None:
        return
    behavior_changed = any(
        path.startswith("skills/") or path in {"plugin.json", ".claude-plugin/plugin.json"}
        for path in changed_paths
    )
    if not behavior_changed:
        return

    current_version = portable_manifest.get("version")
    base_version = base_manifest.get("version")
    if not semver_is_greater(current_version, base_version):
        errors.append(
            "plugin behavior or metadata changed, so both manifests must increase "
            f"the plugin version above {base_version!r}; current version is {current_version!r}"
        )


def validate_repository(
    root: Path,
    *,
    base_manifest: dict[str, Any] | None = None,
    changed_paths: set[str] | None = None,
) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    files = repository_files(root)

    for path in files:
        if path.suffix.lower() == ".json":
            load_json(path, errors)

    portable_manifest = validate_manifests(root, errors)
    skill_names = validate_skills(root, errors)
    validate_markdown_links(root, files, errors)
    validate_local_paths(files, errors)
    validate_skill_references(files, skill_names, errors)
    validate_version_bump(
        portable_manifest, base_manifest, changed_paths, errors
    )
    return sorted(set(errors))


def load_base_inputs(root: Path, base_ref: str) -> tuple[dict[str, Any] | None, set[str]]:
    manifest_result = subprocess.run(
        ["git", "-C", str(root), "show", f"{base_ref}:plugin.json"],
        capture_output=True,
        check=False,
        text=True,
    )
    if manifest_result.returncode != 0:
        raise RuntimeError(
            f"could not read plugin.json from base ref {base_ref}: "
            f"{manifest_result.stderr.strip()}"
        )
    base_manifest = json.loads(manifest_result.stdout)

    diff_result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", base_ref, "--"],
        capture_output=True,
        check=True,
        text=True,
    )
    untracked_result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "ls-files",
            "--others",
            "--exclude-standard",
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    changed_paths = {
        line
        for line in (diff_result.stdout + untracked_result.stdout).splitlines()
        if line
    }
    return base_manifest, changed_paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path.cwd(), help="plugin repository root"
    )
    parser.add_argument(
        "--base-ref",
        help="Git revision used to enforce a version increase for plugin changes",
    )
    arguments = parser.parse_args()

    base_manifest = None
    changed_paths = None
    if arguments.base_ref:
        try:
            base_manifest, changed_paths = load_base_inputs(
                arguments.root, arguments.base_ref
            )
        except (json.JSONDecodeError, RuntimeError, subprocess.CalledProcessError) as exc:
            print(f"Repository quality checks could not inspect the base revision: {exc}")
            return 2

    errors = validate_repository(
        arguments.root,
        base_manifest=base_manifest,
        changed_paths=changed_paths,
    )
    if errors:
        for error in errors:
            if os.environ.get("GITHUB_ACTIONS") == "true":
                print(f"::error::{error}")
            else:
                print(f"ERROR: {error}")
        return 1

    skill_count = len(list((arguments.root / "skills").glob("*/SKILL.md")))
    print(
        "Repository quality checks passed: "
        f"{skill_count} skills, synchronized manifests, valid links and clean paths."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
