import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repository import validate_repository


class RepositoryValidatorTests(unittest.TestCase):
    def make_repository(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)

        manifest = {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "example-plugin",
            "version": "1.2.3",
            "description": "Example plugin for validator tests.",
        }
        (root / "plugin.json").write_text(json.dumps(manifest), encoding="utf-8")
        (root / ".claude-plugin").mkdir()
        (root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(
                {
                    "name": manifest["name"],
                    "version": manifest["version"],
                    "description": manifest["description"],
                }
            ),
            encoding="utf-8",
        )
        (root / "skills" / "example-skill").mkdir(parents=True)
        (root / "skills" / "example-skill" / "SKILL.md").write_text(
            """---
name: example-skill
description: Use when validating an example skill.
---

# Example skill

Read the [reference](references/guide.md).
""",
            encoding="utf-8",
        )
        (root / "skills" / "example-skill" / "references").mkdir()
        (root / "skills" / "example-skill" / "references" / "guide.md").write_text(
            "# Guide\n", encoding="utf-8"
        )
        (root / "README.md").write_text("# Example plugin\n", encoding="utf-8")
        return root

    def test_valid_repository_passes(self) -> None:
        root = self.make_repository()

        self.assertEqual([], validate_repository(root))

    def test_shared_manifest_fields_must_match(self) -> None:
        root = self.make_repository()
        client_manifest = root / ".claude-plugin" / "plugin.json"
        data = json.loads(client_manifest.read_text(encoding="utf-8"))
        data["version"] = "1.2.4"
        client_manifest.write_text(json.dumps(data), encoding="utf-8")

        errors = validate_repository(root)

        self.assertTrue(any("manifest field 'version'" in error for error in errors))

    def test_skill_name_must_match_directory(self) -> None:
        root = self.make_repository()
        skill = root / "skills" / "example-skill" / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                "name: example-skill", "name: another-skill"
            ),
            encoding="utf-8",
        )

        errors = validate_repository(root)

        self.assertTrue(any("must match its directory" in error for error in errors))

    def test_relative_markdown_links_must_resolve(self) -> None:
        root = self.make_repository()
        skill = root / "skills" / "example-skill" / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                "references/guide.md", "references/missing.md"
            ),
            encoding="utf-8",
        )

        errors = validate_repository(root)

        self.assertTrue(any("broken relative link" in error for error in errors))

    def test_local_workstation_paths_are_rejected(self) -> None:
        root = self.make_repository()
        (root / "README.md").write_text(
            "Run `" + "/" + "Users/example/Projects/plugin/check.py`.\n",
            encoding="utf-8",
        )

        errors = validate_repository(root)

        self.assertTrue(any("local workstation path" in error for error in errors))

    def test_skill_changes_require_a_version_increase(self) -> None:
        root = self.make_repository()
        base_manifest = {
            "name": "example-plugin",
            "version": "1.2.3",
            "description": "Example plugin for validator tests.",
        }

        errors = validate_repository(
            root,
            base_manifest=base_manifest,
            changed_paths={"skills/example-skill/SKILL.md"},
        )

        self.assertTrue(any("must increase the plugin version" in error for error in errors))

    def test_higher_version_allows_skill_changes(self) -> None:
        root = self.make_repository()
        base_manifest = {
            "name": "example-plugin",
            "version": "1.2.2",
            "description": "Example plugin for validator tests.",
        }

        errors = validate_repository(
            root,
            base_manifest=base_manifest,
            changed_paths={"skills/example-skill/SKILL.md"},
        )

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
