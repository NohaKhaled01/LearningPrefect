# Summary

**1. The Command Structure**

- `prefect <resource> <action> [arguments] [--flags]`
- Example: `prefect deployment run "my-deployment"`

**2. Essential Commands by Category**

- **Config:** `prefect config view`, `prefect version`
- **Deployments:** `prefect deploy --all`, `prefect deployment ls`, `prefect deployment run`, `prefect deployment inspect`, `prefect deployment schedule pause/resume`
- **Flow Runs:** `prefect flow-run ls` (with `-state Failed` filter), `prefect flow-run logs <id>`, `prefect flow-run cancel <id>`
- **Work Pools:** `prefect work-pool ls`, `prefect work-pool create --type process`, `prefect worker start --pool`
- **Blocks:** `prefect block ls`, `prefect block inspect`

**3. Why CLI Mastery Matters**

- **Speed:** Faster than the UI for debugging.
- **Automation:** Essential for CI/CD scripts.
- **Scripting:** You can pipe output to other tools (e.g., grep).
- **Remote Work:** Manage your orchestration from an SSH session on a server.

**4. The Golden Rule**

- `prefect --help` and `prefect <resource> --help` are your best friends.