from __future__ import annotations

import argparse
import json
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path


REQUIRED_EXAMPLE_FIELDS = {
    "source-manifest.example.jsonl": {
        "source_id",
        "title",
        "source_type",
        "issuer",
        "jurisdiction",
        "access_level",
        "redistribution_policy",
        "locator",
    },
    "provision.example.json": {
        "provision_id",
        "source_id",
        "document_id",
        "locator",
        "text",
        "review_status",
        "version_status",
    },
    "answer-packet.example.json": {
        "answer_id",
        "question",
        "short_answer",
        "scope",
        "citations",
        "version_safety",
        "confidence",
        "unresolved_issues",
    },
    "skill-run-log.example.json": {
        "run_id",
        "skill_name",
        "task",
        "actor",
        "started_at",
        "status",
        "artifacts",
        "validation",
    },
}

REQUIRED_DEMO_FIELDS = {
    "source-manifest.jsonl": REQUIRED_EXAMPLE_FIELDS["source-manifest.example.jsonl"],
    "provisions.synthetic.jsonl": REQUIRED_EXAMPLE_FIELDS["provision.example.json"],
    "answer-packets.synthetic.jsonl": REQUIRED_EXAMPLE_FIELDS["answer-packet.example.json"],
    "coverage-report.json": {
        "demo_id",
        "title",
        "source_count",
        "provision_count",
        "answer_packet_count",
        "content_boundary",
        "validation",
    },
}


def repo_root_from(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "skills").is_dir():
            return candidate
    return current


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing YAML frontmatter")

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        raise ValueError(f"{path}: unclosed YAML frontmatter")

    data: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if ":" not in raw:
            raise ValueError(f"{path}: invalid frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def discover_skills(root: Path) -> list[Skill]:
    skills_dir = root / "skills"
    skills: list[Skill] = []
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        meta = parse_frontmatter(path)
        skills.append(
            Skill(
                name=meta.get("name", ""),
                description=meta.get("description", ""),
                path=path,
            )
        )
    return skills


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_jsonl(path: Path, required_fields: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    required = required_fields if required_fields is not None else REQUIRED_EXAMPLE_FIELDS.get(path.name, set())
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{line_number}: invalid JSONL: {exc}")
            continue
        missing = sorted(required - set(record))
        if missing:
            errors.append(f"{path}:{line_number}: missing fields: {', '.join(missing)}")
        if path.name == "source-manifest.jsonl":
            forbidden = {"full_text", "content", "standard_text"} & set(record)
            if forbidden:
                errors.append(
                    f"{path}:{line_number}: public demo source manifests must not contain: "
                    + ", ".join(sorted(forbidden))
                )
    return errors


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []

    skills = discover_skills(root)
    if not skills:
        errors.append("No skills found")

    seen_names: set[str] = set()
    for skill in skills:
        if not skill.name:
            errors.append(f"{skill.path}: missing name")
        if not skill.description:
            errors.append(f"{skill.path}: missing description")
        if skill.name in seen_names:
            errors.append(f"{skill.path}: duplicate skill name {skill.name}")
        seen_names.add(skill.name)
        if skill.path.parent.name != skill.name:
            errors.append(f"{skill.path}: folder name must match skill name {skill.name}")

    index_path = root / "skills" / "index.json"
    if index_path.exists():
        try:
            index = load_json(index_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{index_path}: invalid JSON: {exc}")
        else:
            indexed_names = {item.get("name") for item in index if isinstance(item, dict)}
            missing = sorted(seen_names - indexed_names)
            extra = sorted(indexed_names - seen_names)
            if missing:
                errors.append(f"{index_path}: missing skills: {', '.join(missing)}")
            if extra:
                errors.append(f"{index_path}: unknown skills: {', '.join(extra)}")
    else:
        errors.append(f"{index_path}: missing skill index")

    for schema_path in sorted((root / "schemas").glob("*.schema.json")):
        try:
            schema = load_json(schema_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{schema_path}: invalid JSON: {exc}")
            continue
        for field in ("$schema", "title", "type"):
            if field not in schema:
                errors.append(f"{schema_path}: missing schema field {field}")

    for example_path in sorted((root / "examples").glob("*.json")):
        try:
            example = load_json(example_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{example_path}: invalid JSON: {exc}")
            continue
        missing = sorted(REQUIRED_EXAMPLE_FIELDS.get(example_path.name, set()) - set(example))
        if missing:
            errors.append(f"{example_path}: missing fields: {', '.join(missing)}")

    for example_path in sorted((root / "examples").glob("*.jsonl")):
        errors.extend(validate_jsonl(example_path))

    demos_dir = root / "demos"
    if demos_dir.exists():
        for demo_json in sorted(demos_dir.glob("*/*.json")):
            try:
                demo_record = load_json(demo_json)
            except json.JSONDecodeError as exc:
                errors.append(f"{demo_json}: invalid JSON: {exc}")
                continue
            missing = sorted(REQUIRED_DEMO_FIELDS.get(demo_json.name, set()) - set(demo_record))
            if missing:
                errors.append(f"{demo_json}: missing fields: {', '.join(missing)}")
        for demo_jsonl in sorted(demos_dir.glob("*/*.jsonl")):
            errors.extend(validate_jsonl(demo_jsonl, REQUIRED_DEMO_FIELDS.get(demo_jsonl.name, set())))

    return errors


def cmd_list(args: argparse.Namespace) -> int:
    root = repo_root_from(Path(args.root) if args.root else None)
    skills = discover_skills(root)
    if args.json:
        payload = [
            {
                "name": skill.name,
                "description": skill.description,
                "path": str(skill.path.relative_to(root)),
            }
            for skill in skills
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    for skill in skills:
        rel_path = skill.path.relative_to(root)
        print(f"{skill.name}\t{rel_path}\t{skill.description}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    root = repo_root_from(Path(args.root) if args.root else None)
    for skill in discover_skills(root):
        if skill.name == args.skill:
            print(skill.path.read_text(encoding="utf-8"))
            return 0
    print(f"unknown skill: {args.skill}", file=sys.stderr)
    return 2


def cmd_validate(args: argparse.Namespace) -> int:
    root = repo_root_from(Path(args.root) if args.root else None)
    errors = validate_root(root)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2, ensure_ascii=False))
    elif errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Validation passed.")
    return 1 if errors else 0


def cmd_new_run_log(args: argparse.Namespace) -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload = {
        "run_id": args.run_id or f"run-{uuid.uuid4().hex[:12]}",
        "skill_name": args.skill,
        "task": args.task,
        "actor": args.actor,
        "started_at": now,
        "status": "planned",
        "artifacts": [],
        "validation": {
            "command": "standards-skills validate",
            "passed": False,
            "notes": "Fill after validation.",
        },
        "skill_updates_needed": [],
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="standards-skills")
    parser.add_argument("--root", help="Repository root. Defaults to auto-detection.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available skills.")
    list_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="Print a skill file.")
    show_parser.add_argument("skill", help="Skill name.")
    show_parser.set_defaults(func=cmd_show)

    validate_parser = subparsers.add_parser("validate", help="Validate skills and examples.")
    validate_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    validate_parser.set_defaults(func=cmd_validate)

    run_log_parser = subparsers.add_parser("new-run-log", help="Create a run log template.")
    run_log_parser.add_argument("--skill", required=True, help="Skill name.")
    run_log_parser.add_argument("--task", required=True, help="Task description.")
    run_log_parser.add_argument("--actor", default="pi-agent", help="Actor name.")
    run_log_parser.add_argument("--run-id", help="Optional stable run ID.")
    run_log_parser.add_argument("--output", help="Optional output path.")
    run_log_parser.set_defaults(func=cmd_new_run_log)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
