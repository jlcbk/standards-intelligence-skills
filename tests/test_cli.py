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

    def test_gb_vehicle_safety_demo_counts(self) -> None:
        demo_root = ROOT / "demos" / "gb-vehicle-safety"
        sources = demo_root.joinpath("source-manifest.jsonl").read_text(encoding="utf-8").splitlines()
        provisions = demo_root.joinpath("provisions.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        answers = demo_root.joinpath("answer-packets.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        coverage = json.loads(demo_root.joinpath("coverage-report.json").read_text(encoding="utf-8"))

        self.assertEqual(len([line for line in sources if line.strip()]), 2)
        self.assertEqual(len([line for line in provisions if line.strip()]), 12)
        self.assertEqual(len([line for line in answers if line.strip()]), 5)
        self.assertFalse(coverage["content_boundary"]["standard_pdf_text_stored"])

    def test_change_packet_example_shape(self) -> None:
        example = json.loads(ROOT.joinpath("examples/change-packet.example.json").read_text(encoding="utf-8"))

        self.assertEqual(example["change_type"], "metadata_refresh")
        self.assertEqual(example["version_relation"]["relation"], "same_version_metadata_refresh")
        self.assertFalse(example["review_tasks"][0]["required_human_decision"])

    def test_compliance_checklist_example_shape(self) -> None:
        example = json.loads(
            ROOT.joinpath("examples/compliance-checklist.example.json").read_text(encoding="utf-8")
        )

        self.assertEqual(example["status"], "draft_demo")
        self.assertEqual(len(example["items"]), 3)
        self.assertEqual(example["items"][2]["status"], "blocked")

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
