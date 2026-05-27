from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from standards_intelligence_skills import cli


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_discover_skills(self) -> None:
        skills = cli.discover_skills(ROOT)
        names = {skill.name for skill in skills}
        self.assertEqual(
            names,
            {
                "source-intake",
                "provision-compiler",
                "regulatory-answer",
                "change-impact",
                "compliance-checklist",
            },
        )

    def test_validate_root(self) -> None:
        self.assertEqual(cli.validate_root(ROOT), [])

    def test_new_run_log_outputs_json(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = cli.main(
                [
                    "--root",
                    str(ROOT),
                    "new-run-log",
                    "--skill",
                    "source-intake",
                    "--task",
                    "Register a source.",
                    "--run-id",
                    "run-test-001",
                ]
            )
        self.assertEqual(code, 0)
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["run_id"], "run-test-001")
        self.assertEqual(payload["skill_name"], "source-intake")
        self.assertEqual(payload["status"], "planned")


if __name__ == "__main__":
    unittest.main()
