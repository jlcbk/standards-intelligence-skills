from __future__ import annotations

import io
import json
import shutil
import tempfile
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

    def test_validate_root_uses_schema_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            shutil.copytree(ROOT, repo)
            example_path = repo / "examples" / "answer-packet.example.json"
            example = json.loads(example_path.read_text(encoding="utf-8"))
            example["version_safety"] = "current-ish"
            example_path.write_text(json.dumps(example, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            errors = cli.validate_root(repo)

        self.assertTrue(any("answer-packet.example.json" in error for error in errors))
        self.assertTrue(any("$.version_safety" in error for error in errors))

    def test_schema_validator_catches_nested_errors(self) -> None:
        schema = {
            "type": "object",
            "required": ["status", "items"],
            "properties": {
                "status": {"type": "string", "enum": ["ok"]},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {"name": {"type": "string"}},
                        "additionalProperties": False,
                    },
                },
            },
            "additionalProperties": False,
        }

        errors = cli.validate_instance_against_schema(
            {"status": "bad", "items": [{"name": 7, "extra": True}], "unexpected": 1},
            schema,
        )

        self.assertTrue(any("$.status" in error and "允许列表" in error for error in errors))
        self.assertTrue(any("$.items[0].name" in error and "string" in error for error in errors))
        self.assertTrue(any("额外字段 extra" in error for error in errors))
        self.assertTrue(any("额外字段 unexpected" in error for error in errors))

    def test_validate_root_checks_demo_coverage_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            shutil.copytree(ROOT, repo)
            coverage_path = repo / "demos" / "gb-vehicle-safety" / "coverage-report.json"
            coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
            coverage["answer_packet_count"] = 999
            coverage_path.write_text(json.dumps(coverage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            errors = cli.validate_root(repo)

        self.assertTrue(any("coverage-report.json" in error for error in errors))
        self.assertTrue(any("answer_packet_count" in error and "应为 5" in error for error in errors))

    def test_validate_root_checks_demo_citation_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            shutil.copytree(ROOT, repo)
            answers_path = repo / "demos" / "gb-vehicle-safety" / "answer-packets.synthetic.jsonl"
            lines = answers_path.read_text(encoding="utf-8").splitlines()
            first_answer = json.loads(lines[0])
            first_answer["citations"][0]["provision_id"] = "missing-provision"
            lines[0] = json.dumps(first_answer, ensure_ascii=False)
            answers_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            errors = cli.validate_root(repo)

        self.assertTrue(any("answer-packets.synthetic.jsonl:1" in error for error in errors))
        self.assertTrue(any("missing-provision" in error for error in errors))

    def test_validate_root_checks_document_family_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            shutil.copytree(ROOT, repo)
            families_path = repo / "demos" / "gb-vehicle-safety" / "document-families.synthetic.jsonl"
            lines = families_path.read_text(encoding="utf-8").splitlines()
            first_family = json.loads(lines[0])
            first_family["current_document_ids"] = ["missing-document"]
            first_family["relations"][0]["evidence_source_id"] = "missing-source"
            lines[0] = json.dumps(first_family, ensure_ascii=False)
            families_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            errors = cli.validate_root(repo)

        self.assertTrue(any("document-families.synthetic.jsonl:1" in error for error in errors))
        self.assertTrue(any("missing-document" in error for error in errors))
        self.assertTrue(any("missing-source" in error for error in errors))

    def test_validate_root_checks_watchlist_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            shutil.copytree(ROOT, repo)
            watchlist_path = repo / "demos" / "gb-vehicle-safety" / "source-watchlist.synthetic.jsonl"
            lines = watchlist_path.read_text(encoding="utf-8").splitlines()
            first_watch = json.loads(lines[0])
            first_watch["source_id"] = "missing-source"
            lines[0] = json.dumps(first_watch, ensure_ascii=False)
            watchlist_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            errors = cli.validate_root(repo)

        self.assertTrue(any("source-watchlist.synthetic.jsonl:1" in error for error in errors))
        self.assertTrue(any("missing-source" in error for error in errors))

    def test_check_sources_reports_due_items(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = cli.main(
                [
                    "--root",
                    str(ROOT),
                    "check-sources",
                    "--as-of",
                    "2026-06-27",
                    "--fail-on-due",
                    "--json",
                ]
            )

        payload = json.loads(out.getvalue())
        self.assertEqual(code, 1)
        self.assertEqual(payload["due_count"], 2)
        self.assertEqual({item["state"] for item in payload["items"]}, {"due"})

    def test_check_sources_passes_before_due_date(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = cli.main(
                [
                    "--root",
                    str(ROOT),
                    "check-sources",
                    "--as-of",
                    "2026-05-27",
                    "--fail-on-due",
                    "--json",
                ]
            )

        payload = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(payload["due_count"], 0)
        self.assertEqual({item["state"] for item in payload["items"]}, {"ok"})

    def test_inspect_corpus_outputs_private_safe_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            text_dir = Path(tmp) / "text"
            text_dir.mkdir()
            usable_lines = [
                f"{index}.1 synthetic requirement line with enough text for inspection"
                for index in range(1, 50)
            ]
            text_dir.joinpath("usable.txt").write_text("\n".join(usable_lines) + "\n", encoding="utf-8")
            text_dir.joinpath("poor.txt").write_text("too short\n", encoding="utf-8")

            out = io.StringIO()
            with redirect_stdout(out):
                code = cli.main(["inspect-corpus", "--text-dir", str(text_dir), "--json"])

        payload = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertFalse(payload["content_boundary"]["raw_text_included"])
        self.assertTrue(payload["content_boundary"]["public_repo_safe"])
        self.assertEqual(payload["summary"]["document_count"], 2)
        self.assertEqual(payload["summary"]["usable_count"], 1)
        self.assertEqual(payload["summary"]["poor_count"], 1)

    def test_gb_vehicle_safety_demo_counts(self) -> None:
        demo_root = ROOT / "demos" / "gb-vehicle-safety"
        sources = demo_root.joinpath("source-manifest.jsonl").read_text(encoding="utf-8").splitlines()
        families = demo_root.joinpath("document-families.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        watchlist = demo_root.joinpath("source-watchlist.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        provisions = demo_root.joinpath("provisions.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        answers = demo_root.joinpath("answer-packets.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        coverage = json.loads(demo_root.joinpath("coverage-report.json").read_text(encoding="utf-8"))

        self.assertEqual(len([line for line in sources if line.strip()]), 2)
        self.assertEqual(len([line for line in families if line.strip()]), 2)
        self.assertEqual(coverage["document_family_count"], 2)
        self.assertEqual(len([line for line in watchlist if line.strip()]), 2)
        self.assertEqual(coverage["watchlist_count"], 2)
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

    def test_run_task_creates_run_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "run-log.json"
            out = io.StringIO()
            with redirect_stdout(out):
                code = cli.main(
                    [
                        "--root",
                        str(ROOT),
                        "run-task",
                        "--packet",
                        "examples/task-packet.example.json",
                        "--run-id",
                        "run-test-task-001",
                        "--output",
                        str(output),
                        "--validate",
                    ]
                )

            self.assertEqual(code, 0)
            summary = json.loads(out.getvalue())
            run_log = json.loads(output.read_text(encoding="utf-8"))
            self.assertTrue(summary["ok"])
            self.assertEqual(summary["skill_name"], "regulatory-answer")
            self.assertEqual(run_log["run_id"], "run-test-task-001")
            self.assertEqual(run_log["status"], "passed")
            self.assertTrue(run_log["validation"]["passed"])

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
