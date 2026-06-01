# AGENTS.md

This file is intended for AI coding agents. It is kept human-readable so contributors can also use it as a quick-reference guide.

## What This Project Is

An Ansible collection (`servicenow.itsm`) providing modules for managing ServiceNow resources via the REST api. No roles exist — only modules and shared utilities. This qualifies as a "Certified" collection.

The collection namespace, name, and version number can all be found in the `galaxy.yml` file.

## Development Environment

The collection must reside at `ansible_collections/NAMESPACE/NAME/` (relative to a directory on `ANSIBLE_COLLECTIONS_PATHS`) for imports to resolve correctly.

All required packages are listed in `requirements.txt`.

## Coding Guidelines

- Follow these software development principles: KISS (Keep It Simple, Stupid), DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), Separation of Concerns, Composition over Inheritance, and Convention Over Configuration.
- Prioritize code simplicity and readability over flexibility.
- Favor simple, short, and easily testable functions with no side effects over classes. Use classes only when they naturally fit the problem and help avoid boilerplate code while grouping tightly related functionality.
- Use `snake_case` for all variable and parameter names.
- Shared code used by multiple modules belongs in `plugins/module_utils/` (DRY principle). Do not duplicate connection or utility logic in individual modules.
- Do not add connection parameters to individual modules. Extend the doc fragment in `plugins/doc_fragments/` instead.
- All modules must pass sanity and integration tests before merging.
- Keep each piece of work focused on solving a single, specific issue or task. Do not mix unrelated changes (e.g., a bugfix and an unrelated refactoring) in the same branch or PR.
- Use conventional commit message prefixes: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `ci:`. Example: `fix: handle empty database list in mysql_info`.

## Development Conventions

- Every PR that changes module behavior needs a changelog fragment in `changelogs/fragments/<something>.yaml`. Docs/tests/refactoring PRs are exempt. Valid fragment sections: `major_changes`, `minor_changes`, `bugfixes`, `breaking_changes`, `deprecated_features`, `removed_features`, `security_fixes`, `known_issues`. Fragments are consumed (deleted) at release time (`keep_fragments: false` in `changelogs/config.yaml`).

## Integration CI (ServiceNow instances)

Integration tests run in `.github/workflows/integration_source.yml` against three ServiceNow PDIs in the `protected-snow` GitHub environment.

- **Matrix label** (`servicenow-version`): the SNOW release codename under test (e.g. `australia`). Used for job names only.
- **GitHub secrets**: named by **PDI instance ID**, not release codename — `SN_HOST_<id>`, `SN_USERNAME_<id>`, etc. (e.g. `SN_HOST_7056` for instance `dev7056`). Instances are upgraded in place; credentials stay the same.

When supporting a new SNOW release on an existing instance:

1. Upgrade the instance in ServiceNow.
2. Change the `servicenow-version` string in the workflow matrix (and update `README.md` compatibility table + changelog fragment).
3. Do **not** create new GitHub secrets.

When adding a **new** PDI to the matrix, create the eight `SN_*_<instance_id>` secrets once, then add a new `include` block with that instance ID.

Legacy rows may still reference `SN_*_YOKOHAMA` / `SN_*_ZURICH` until those secrets are renamed in GitHub to instance IDs and the workflow is updated to match.

## Subagents

Subagent definitions live in `.agents/subagents/`. When a task matches a subagent's trigger conditions, delegate to it.

## Project Skills

Skills live in `.agents/skills/*/SKILL.md` (YAML frontmatter + instructions). At session start, scan and register all skills. When a request matches a skill's trigger, load and apply it.

- **update-snow-release** — add/drop ServiceNow release support (CI matrix, README, changelog).

## Lola Skills

These skills are installed by Lola and provide specialized capabilities.
When a task matches a skill's description, read the skill's SKILL.md file
to learn the detailed instructions and workflows.

**How to use skills:**
1. Check if your task matches any skill description below
2. Use `read_file` to read the skill's SKILL.md for detailed instructions
3. Follow the instructions in the SKILL.md file
