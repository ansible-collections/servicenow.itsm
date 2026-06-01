---
name: update-snow-release
description: >-
  Add or drop ServiceNow release support in servicenow.itsm (integration CI
  matrix, README compatibility table, changelog fragment). Use when the user
  asks to support a new SNOW release, drop an EOL release, update the test
  matrix, or mentions release codenames (e.g. Australia, Xanadu, Zurich).
---

# Update ServiceNow release support

This collection does **not** branch module code on SNOW release names. Support is expressed through CI, README, and changelogs. See also `AGENTS.md` → Integration CI.

## Scope

**In scope:** `.github/workflows/integration_source.yml`, `README.md` compatibility table, `changelogs/fragments/`, maintainer notes in `AGENTS.md` if conventions change.

**Out of scope (unless integration tests fail):** `plugins/`, `tests/`, module doc URLs with old bundle names (`bundle/tokyo-...`), hand-editing `CHANGELOG.rst` or `changelogs/changelog.yaml` (generated at release).

## Decision: upgrade in place vs new PDI

| Scenario | Workflow change | GitHub secrets |
|----------|-----------------|----------------|
| **Upgrade existing newest PDI** (usual) | Change `servicenow-version` label only; keep `SN_*_<instance_id>` | Rename existing secrets to instance ID if still on codename; **do not** create new secrets |
| **Add a new PDI** to the matrix | Add matrix entry + full `include` block | The user will need to create eight secrets in Github once: `SN_HOST_<id>`, `SN_USERNAME_<id>`, `SN_PASSWORD_<id>`, `SN_CLIENT_ID_<id>`, `SN_CLIENT_SECRET_<id>`, `SN_API_KEY_<id>`, `SN_CLIENT_CERTIFICATE_<id>`, `SN_CLIENT_KEY_<id>` |

Instance ID = numeric suffix from the PDI hostname (e.g. `dev7056` → `7056`).

## Workflow checklist

Copy and track progress:

```
- [ ] Confirm new release codename and which PDI instance is upgraded
- [ ] Update integration_source.yml matrix
- [ ] Update README.md compatibility table
- [ ] Add changelogs/fragments/<issue>-<topic>.yaml
- [ ] Remind maintainer: GitHub secrets / instance upgrade (if not done)
- [ ] Open PR using .github/pull_request_template.md
```

### 1. Integration CI — `.github/workflows/integration_source.yml`

Only file with release-specific configuration. Matrix keeps **three** SNOW versions (newest + two older).

**Upgrade in place (replace oldest / dropped release on newest instance):**

```yaml
servicenow-version:
  - "<new_release>"   # was <old_release>
  - "yokohama"
  - "zurich"
include:
  - servicenow-version: "<new_release>"
    sn_host_secret: SN_HOST_<instance_id>
    sn_username_secret: SN_USERNAME_<instance_id>
    # ... same pattern for all eight SN_*_<instance_id> secrets
```

**Do not** switch secrets back to `SN_*_<RELEASE_CODENAME>` — instances upgrade in place.

Leave workflow comments above `servicenow-version` intact (they document the instance-ID convention).

### 2. README — compatibility table

In `README.md` (Supported ServiceNow versions):

1. Add new release at the top: `| <NewRelease> | <next_collection_version>+ | TBA |`
2. Retire dropped release: set EOL quarter and bound collection range (e.g. `2.7.0 - 2.14.0 | Q2 2026`), following Washington/Vancouver/Xanadu rows.
3. Next collection version = bump after current `galaxy.yml` `version` (e.g. `2.14.0` → document `2.15.0+`).

### 3. Changelog fragment — required

Create `changelogs/fragments/<descriptive-name>.yaml`:

```yaml
---
minor_changes:
  - add support for SNOW <NEW_RELEASE> release
  - tests - Drop testing of <OLD_RELEASE>, as it is no longer supported by the collection
```

Adjust wording if only adding (no drop) or only dropping. Per `AGENTS.md`, behavior/support changes need a fragment.

### 4. Discover other references

```bash
rg -i '<old_release>|<new_release>' --glob '!CHANGELOG*' --glob '!changelogs/changelog.yaml'
```

Expect hits only in workflow, README, changelogs, and historical docs — not in `plugins/` or `tests/`.

### 5. Pull request

Use `.github/pull_request_template.md`:

- **ISSUE TYPE:** Feature Pull Request (release support)
- **COMPONENT NAME:** `integration CI / collection compatibility`
- **ADDITIONAL INFORMATION:** List maintainer GitHub secret actions and which matrix leg uses which instance ID

Prefer `ci:` commit prefix. Example: `ci: add Australia release support and drop Xanadu from test matrix`

Draft PR against `ansible-collections/servicenow.itsm` `main` from the contributor fork.

The user should be able to confirm the new version is valid via the CI running in their PR.

## Reference: Australia / Xanadu (2026)

| Item | Value |
|------|-------|
| Added | `australia` on instance `7056` (`SN_*_7056`) |
| Dropped from CI | `xanadu` (same instance, upgraded in place) |
| README | Australia `2.15.0+`; Xanadu `2.7.0 - 2.14.0`, EOL Q2 2026 |
| Legacy secrets | Yokohama/Zurich rows may still use `SN_*_YOKOHAMA` / `SN_*_ZURICH` until migrated to instance IDs |

Prior art: upstream PR adding Zurich (dropped Washington from matrix); commit adding Xanadu to matrix.
