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


SCHEMA_FILE_BY_EXAMPLE = {
    "answer-packet.example.json": "answer-packet.schema.json",
    "change-packet.example.json": "change-packet.schema.json",
    "compliance-checklist.example.json": "compliance-checklist.schema.json",
    "provision.example.json": "provision.schema.json",
    "skill-run-log.example.json": "skill-run-log.schema.json",
    "source-manifest.example.jsonl": "source-manifest.schema.json",
    "task-packet.example.json": "task-packet.schema.json",
}

SCHEMA_FILE_BY_DEMO = {
    "answer-packets.synthetic.jsonl": "answer-packet.schema.json",
    "coverage-report.json": "coverage-report.schema.json",
    "provisions.synthetic.jsonl": "provision.schema.json",
    "source-manifest.jsonl": "source-manifest.schema.json",
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


def find_skill(root: Path, name: str) -> Skill | None:
    for skill in discover_skills(root):
        if skill.name == name:
            return skill
    return None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_run_log(
    *,
    skill_name: str,
    task: str,
    actor: str,
    run_id: str | None = None,
    status: str = "planned",
    artifacts: list[str] | None = None,
    validation_passed: bool = False,
    validation_notes: str = "验证后填写。",
) -> dict[str, Any]:
    return {
        "run_id": run_id or f"run-{uuid.uuid4().hex[:12]}",
        "skill_name": skill_name,
        "task": task,
        "actor": actor,
        "started_at": utc_now(),
        "status": status,
        "artifacts": artifacts or [],
        "validation": {
            "command": "standards-skills validate",
            "passed": validation_passed,
            "notes": validation_notes,
        },
        "skill_updates_needed": [],
    }


def json_type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if value is None:
        return "null"
    return type(value).__name__


def matches_json_type(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def join_instance_path(base: str, key: str | int) -> str:
    if isinstance(key, int):
        return f"{base}[{key}]"
    if key.replace("_", "").replace("-", "").isalnum():
        return f"{base}.{key}"
    return f"{base}[{json.dumps(key, ensure_ascii=False)}]"


def short_json(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 80 else text[:77] + "..."


def validate_instance_against_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []

    expected = schema.get("type")
    expected_types = expected if isinstance(expected, list) else [expected] if isinstance(expected, str) else []
    if expected_types and not any(matches_json_type(instance, item) for item in expected_types):
        errors.append(
            f"{path}: 类型应为 {'/'.join(expected_types)}，实际为 {json_type_name(instance)}"
        )
        return errors

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: 取值 {short_json(instance)} 不在允许列表中")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in instance:
                errors.append(f"{path}: 缺少必填字段 {field}")

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for field, subschema in properties.items():
                if field in instance and isinstance(subschema, dict):
                    errors.extend(
                        validate_instance_against_schema(
                            instance[field],
                            subschema,
                            join_instance_path(path, field),
                        )
                    )

            additional = schema.get("additionalProperties", True)
            extra_fields = sorted(set(instance) - set(properties))
            if additional is False:
                for field in extra_fields:
                    errors.append(f"{path}: 不允许额外字段 {field}")
            elif isinstance(additional, dict):
                for field in extra_fields:
                    errors.extend(
                        validate_instance_against_schema(
                            instance[field],
                            additional,
                            join_instance_path(path, field),
                        )
                    )

    if isinstance(instance, list):
        items_schema = schema.get("items")
        if isinstance(items_schema, dict):
            for index, item in enumerate(instance):
                errors.extend(validate_instance_against_schema(item, items_schema, join_instance_path(path, index)))

    return errors


def schema_errors_for_record(record: Any, schema: dict[str, Any], label: str) -> list[str]:
    return [f"{label}: schema 校验失败：{error}" for error in validate_instance_against_schema(record, schema)]


def schema_for_file(
    schemas: dict[str, dict[str, Any]],
    mapping: dict[str, str],
    path: Path,
    errors: list[str],
) -> dict[str, Any] | None:
    schema_name = mapping.get(path.name)
    if not schema_name:
        errors.append(f"{path}: 未配置 schema 映射")
        return None
    schema = schemas.get(schema_name)
    if not schema:
        errors.append(f"{path}: 找不到 schema {schema_name}")
        return None
    return schema


def validate_jsonl(path: Path, schema: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{line_number}: JSONL 无效：{exc}")
            continue
        if schema is not None:
            errors.extend(schema_errors_for_record(record, schema, f"{path}:{line_number}"))
        if path.name == "source-manifest.jsonl":
            forbidden = {"full_text", "content", "standard_text"} & set(record)
            if forbidden:
                errors.append(
                    f"{path}:{line_number}: 公开 demo source manifest 不得包含："
                    + ", ".join(sorted(forbidden))
                )
    return errors


def read_jsonl_objects(path: Path) -> tuple[list[tuple[str, dict[str, Any]]], list[str]]:
    records: list[tuple[str, dict[str, Any]]] = []
    errors: list[str] = []
    if not path.exists():
        return records, [f"{path}: 缺少文件"]

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        label = f"{path}:{line_number}"
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: JSONL 无效：{exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{label}: JSONL record 必须是 object")
            continue
        records.append((label, record))
    return records, errors


def validate_citation_refs(
    *,
    label: str,
    citations: Any,
    source_ids: set[str],
    provision_source_ids: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(citations, list):
        return errors

    for index, citation in enumerate(citations):
        citation_label = f"{label}.citations[{index}]"
        if not isinstance(citation, dict):
            continue
        provision_id = citation.get("provision_id")
        source_id = citation.get("source_id")
        if isinstance(provision_id, str) and provision_id not in provision_source_ids:
            errors.append(f"{citation_label}: provision_id 不存在：{provision_id}")
        if isinstance(source_id, str) and source_id not in source_ids:
            errors.append(f"{citation_label}: source_id 不存在：{source_id}")
        if (
            isinstance(provision_id, str)
            and isinstance(source_id, str)
            and provision_id in provision_source_ids
            and source_id != provision_source_ids[provision_id]
        ):
            errors.append(
                f"{citation_label}: source_id {source_id} 与 provision {provision_id} 的 source_id "
                f"{provision_source_ids[provision_id]} 不一致"
            )
    return errors


def validate_demo_integrity(demo_root: Path) -> list[str]:
    errors: list[str] = []
    source_records, source_errors = read_jsonl_objects(demo_root / "source-manifest.jsonl")
    provision_records, provision_errors = read_jsonl_objects(demo_root / "provisions.synthetic.jsonl")
    answer_records, answer_errors = read_jsonl_objects(demo_root / "answer-packets.synthetic.jsonl")
    errors.extend(source_errors)
    errors.extend(provision_errors)
    errors.extend(answer_errors)
    if source_errors or provision_errors or answer_errors:
        return errors

    source_ids = {
        record["source_id"]
        for _, record in source_records
        if isinstance(record.get("source_id"), str)
    }
    provision_source_ids = {
        record["provision_id"]: record["source_id"]
        for _, record in provision_records
        if isinstance(record.get("provision_id"), str) and isinstance(record.get("source_id"), str)
    }

    for label, record in provision_records:
        source_id = record.get("source_id")
        if isinstance(source_id, str) and source_id not in source_ids:
            errors.append(f"{label}: source_id 不存在于 source manifest：{source_id}")

    for label, record in answer_records:
        errors.extend(
            validate_citation_refs(
                label=label,
                citations=record.get("citations"),
                source_ids=source_ids,
                provision_source_ids=provision_source_ids,
            )
        )

    coverage_path = demo_root / "coverage-report.json"
    try:
        coverage = load_json(coverage_path)
    except FileNotFoundError:
        errors.append(f"{coverage_path}: 缺少文件")
    except json.JSONDecodeError as exc:
        errors.append(f"{coverage_path}: JSON 无效：{exc}")
    else:
        expected_counts = {
            "source_count": len(source_records),
            "provision_count": len(provision_records),
            "answer_packet_count": len(answer_records),
        }
        for field, expected in expected_counts.items():
            actual = coverage.get(field) if isinstance(coverage, dict) else None
            if actual != expected:
                errors.append(f"{coverage_path}: {field} 应为 {expected}，实际为 {short_json(actual)}")
        if isinstance(coverage, dict) and "source_ids" in coverage:
            actual_source_ids = coverage.get("source_ids")
            if (
                not isinstance(actual_source_ids, list)
                or not all(isinstance(item, str) for item in actual_source_ids)
                or set(actual_source_ids) != source_ids
            ):
                errors.append(f"{coverage_path}: source_ids 必须与 source manifest 完全一致")

    for checklist_path in sorted(demo_root.glob("*checklist*.json")):
        try:
            checklist = load_json(checklist_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{checklist_path}: JSON 无效：{exc}")
            continue
        if not isinstance(checklist, dict):
            continue
        errors.extend(
            validate_citation_refs(
                label=str(checklist_path),
                citations=checklist.get("citations"),
                source_ids=source_ids,
                provision_source_ids=provision_source_ids,
            )
        )
        items = checklist.get("items")
        if isinstance(items, list):
            for index, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                source_provision_ids = item.get("source_provision_ids", [])
                if not isinstance(source_provision_ids, list):
                    continue
                for provision_id in source_provision_ids:
                    if isinstance(provision_id, str) and provision_id not in provision_source_ids:
                        errors.append(
                            f"{checklist_path}.items[{index}]: source_provision_ids 不存在：{provision_id}"
                        )

    return errors


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []

    skills = discover_skills(root)
    if not skills:
        errors.append("未找到 skills")

    seen_names: set[str] = set()
    for skill in skills:
        if not skill.name:
            errors.append(f"{skill.path}: 缺少 name")
        if not skill.description:
            errors.append(f"{skill.path}: 缺少 description")
        if skill.name in seen_names:
            errors.append(f"{skill.path}: skill name 重复：{skill.name}")
        seen_names.add(skill.name)
        if skill.path.parent.name != skill.name:
            errors.append(f"{skill.path}: 文件夹名必须匹配 skill name {skill.name}")

    index_path = root / "skills" / "index.json"
    if index_path.exists():
        try:
            index = load_json(index_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{index_path}: JSON 无效：{exc}")
        else:
            indexed_names = {item.get("name") for item in index if isinstance(item, dict)}
            missing = sorted(seen_names - indexed_names)
            extra = sorted(indexed_names - seen_names)
            if missing:
                errors.append(f"{index_path}: 缺少 skills：{', '.join(missing)}")
            if extra:
                errors.append(f"{index_path}: 未知 skills：{', '.join(extra)}")
    else:
        errors.append(f"{index_path}: 缺少 skill index")

    schemas: dict[str, dict[str, Any]] = {}
    for schema_path in sorted((root / "schemas").glob("*.schema.json")):
        try:
            schema = load_json(schema_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{schema_path}: JSON 无效：{exc}")
            continue
        for field in ("$schema", "title", "type"):
            if field not in schema:
                errors.append(f"{schema_path}: 缺少 schema 字段 {field}")
        if isinstance(schema, dict):
            schemas[schema_path.name] = schema

    for example_path in sorted((root / "examples").glob("*.json")):
        try:
            example = load_json(example_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{example_path}: JSON 无效：{exc}")
            continue
        schema = schema_for_file(schemas, SCHEMA_FILE_BY_EXAMPLE, example_path, errors)
        if schema is not None:
            errors.extend(schema_errors_for_record(example, schema, str(example_path)))

    for example_path in sorted((root / "examples").glob("*.jsonl")):
        schema = schema_for_file(schemas, SCHEMA_FILE_BY_EXAMPLE, example_path, errors)
        errors.extend(validate_jsonl(example_path, schema))

    demos_dir = root / "demos"
    if demos_dir.exists():
        for demo_json in sorted(demos_dir.glob("*/*.json")):
            try:
                demo_record = load_json(demo_json)
            except json.JSONDecodeError as exc:
                errors.append(f"{demo_json}: JSON 无效：{exc}")
                continue
            schema = schema_for_file(schemas, SCHEMA_FILE_BY_DEMO, demo_json, errors)
            if schema is not None:
                errors.extend(schema_errors_for_record(demo_record, schema, str(demo_json)))
        for demo_jsonl in sorted(demos_dir.glob("*/*.jsonl")):
            schema = schema_for_file(schemas, SCHEMA_FILE_BY_DEMO, demo_jsonl, errors)
            errors.extend(validate_jsonl(demo_jsonl, schema))
        for demo_root in sorted(path for path in demos_dir.iterdir() if path.is_dir()):
            errors.extend(validate_demo_integrity(demo_root))

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
    skill = find_skill(root, args.skill)
    if skill:
        print(skill.path.read_text(encoding="utf-8"))
        return 0
    print(f"未知 skill：{args.skill}", file=sys.stderr)
    return 2


def cmd_validate(args: argparse.Namespace) -> int:
    root = repo_root_from(Path(args.root) if args.root else None)
    errors = validate_root(root)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2, ensure_ascii=False))
    elif errors:
        print("验证失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("验证通过。")
    return 1 if errors else 0


def cmd_new_run_log(args: argparse.Namespace) -> int:
    payload = build_run_log(skill_name=args.skill, task=args.task, actor=args.actor, run_id=args.run_id)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


def cmd_run_task(args: argparse.Namespace) -> int:
    root = repo_root_from(Path(args.root) if args.root else None)
    packet_path = Path(args.packet)
    if not packet_path.is_absolute():
        packet_path = root / packet_path
    try:
        packet = load_json(packet_path)
    except json.JSONDecodeError as exc:
        print(f"{packet_path}: JSON 无效：{exc}", file=sys.stderr)
        return 2

    skill_name = args.skill or packet.get("skill_name")
    if not skill_name:
        print("task packet 必须包含 skill_name，或通过 --skill 指定", file=sys.stderr)
        return 2

    skill = find_skill(root, skill_name)
    if not skill:
        print(f"未知 skill：{skill_name}", file=sys.stderr)
        return 2

    task = packet.get("requested_outcome") or packet.get("task") or f"Run {skill_name}"
    artifacts = packet.get("allowed_outputs", [])
    if not isinstance(artifacts, list):
        print("task packet 的 allowed_outputs 必须是 list", file=sys.stderr)
        return 2

    validation_errors = validate_root(root) if args.validate else []
    validation_passed = args.validate and not validation_errors
    status = "passed" if validation_passed else "failed" if validation_errors else "planned"
    notes = "验证通过。" if validation_passed else "未请求验证。"
    if validation_errors:
        notes = "; ".join(validation_errors)

    run_log = build_run_log(
        skill_name=skill_name,
        task=task,
        actor=args.actor,
        run_id=args.run_id,
        status=status,
        artifacts=[str(item) for item in artifacts],
        validation_passed=validation_passed,
        validation_notes=notes,
    )

    output = Path(args.output) if args.output else root / "runs" / f"{run_log['run_id']}.json"
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(run_log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = {
        "ok": not validation_errors,
        "task_id": packet.get("task_id"),
        "skill_name": skill_name,
        "skill_path": str(skill.path.relative_to(root)),
        "run_log": str(output.relative_to(root) if output.is_relative_to(root) else output),
        "validation_errors": validation_errors,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 1 if validation_errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="standards-skills")
    parser.add_argument("--root", help="仓库根目录。默认自动识别。")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="列出可用 skills。")
    list_parser.add_argument("--json", action="store_true", help="输出 JSON。")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="打印 skill 文件。")
    show_parser.add_argument("skill", help="Skill 名称。")
    show_parser.set_defaults(func=cmd_show)

    validate_parser = subparsers.add_parser("validate", help="验证 skills、schemas、examples 和 demos。")
    validate_parser.add_argument("--json", action="store_true", help="输出 JSON。")
    validate_parser.set_defaults(func=cmd_validate)

    run_log_parser = subparsers.add_parser("new-run-log", help="创建 run log 模板。")
    run_log_parser.add_argument("--skill", required=True, help="Skill 名称。")
    run_log_parser.add_argument("--task", required=True, help="任务描述。")
    run_log_parser.add_argument("--actor", default="pi-agent", help="Actor 名称。")
    run_log_parser.add_argument("--run-id", help="可选稳定 run ID。")
    run_log_parser.add_argument("--output", help="可选输出路径。")
    run_log_parser.set_defaults(func=cmd_new_run_log)

    run_task_parser = subparsers.add_parser("run-task", help="从 task packet 选择 skill 并生成 run log。")
    run_task_parser.add_argument("--packet", required=True, help="Task packet JSON 路径。")
    run_task_parser.add_argument("--skill", help="覆盖 packet 中的 skill_name。")
    run_task_parser.add_argument("--actor", default="pi-agent", help="Actor 名称。")
    run_task_parser.add_argument("--run-id", help="可选稳定 run ID。")
    run_task_parser.add_argument("--output", help="Run log 输出路径。默认 runs/<run_id>.json。")
    run_task_parser.add_argument("--validate", action="store_true", help="先运行仓库 schema-aware validation。")
    run_task_parser.set_defaults(func=cmd_run_task)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
