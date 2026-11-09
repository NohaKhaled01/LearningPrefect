# CLI Mastery

[Summary](<./CLI Mastery Summary.md>)

Up until now, we've been using a mix of Python scripts, the `.deploy()` method, and the UI. But in the real world, when you're debugging a production issue at 2 AM or writing a CI/CD script, you don't want to open a browser or write a full Python script. You want to type a fast, precise command in your terminal.

The Prefect CLI is your command center. It allows you to inspect, trigger, cancel, and manage everything in your Prefect ecosystem without leaving your terminal.

### **🏗️ The Command Structure**

Every Prefect CLI command follows a consistent pattern:

bash

```
prefect <resource> <action> [arguments] [--flags]
```

For example:

- `prefect deployment run` (Resource: deployment, Action: run)
- `prefect flow-run cancel` (Resource: flow-run, Action: cancel)
- `prefect work-pool ls` (Resource: work-pool, Action: ls/list)

### **📋 The Cheat Sheet: The Commands You'll Use Daily**

Here are the most important commands, grouped by what you're trying to do.

#### **1. Configuration & Connection**

- `prefect version`: Check the installed version, Python version, and current API URL.
- `prefect config view`: See your current profile settings (like `PREFECT_API_URL`).
- `prefect profile ls`: List all your configured profiles (e.g., Cloud vs. Local).
- `prefect cloud login` / `prefect server start`: Switch between Cloud and Self-Hosted.

#### **2. Deployments**

- `prefect deploy --all`: Register all deployments defined in `prefect.yaml`.
- `prefect deployment ls`: List all registered deployments.
- `prefect deployment inspect <name>`: Get detailed info about a deployment (ID, work pool, schedule).
- `prefect deployment run <name>`: **Trigger a deployment manually from the terminal.** (e.g., `prefect deployment run "user-pipeline-deployment"`).
- `prefect deployment schedule ls <name>`: See the cron schedules for a deployment.
- `prefect deployment schedule pause <name>`: Pause a deployment's schedule (as we did earlier!).
- `prefect deployment schedule resume <name>`: Resume a paused schedule.

#### **3. Flow Runs (The most useful for debugging)**

- `prefect flow-run ls`: List recent flow runs (with their states and IDs).
- `prefect flow-run ls --limit 10 --state Failed`: Filter to see only the last 10 failed runs.
- `prefect flow-run inspect <run-id>`: Get detailed info about a specific run.
- `prefect flow-run logs <run-id>`: **Print the logs of a flow run directly to your terminal.** (Huge time-saver).
- `prefect flow-run cancel <run-id>`: Cancel a stuck or long-running flow.
- `prefect flow-run delete <run-id>`: Delete a flow run from the database.

#### **4. Work Pools & Workers**

- `prefect work-pool ls`: List all work pools.
- `prefect work-pool create --type process my-pool`: Create a new pool.
- `prefect work-pool inspect <name>`: See the details of a pool.
- `prefect worker start --pool <name>`: Start a worker for a specific pool.
- `prefect work-queue ls`: List work queues within pools (advanced).

#### **5. Blocks (Secrets & Config)**

- `prefect block ls`: List all blocks in your workspace.
- `prefect block inspect <name>`: See the details of a block (not the secret value!).
- `prefect block delete <name>`: Delete a block.

### **🛠️ Real-World Scenarios**

**Scenario A: "I just pushed code, and I want to trigger the pipeline manually to test it."**

Instead of opening the UI, clicking Deployments, finding the deployment, and clicking Run, you just type:

bash

```
prefect deployment run "user-pipeline-deployment"
```

**Scenario B: "A pipeline failed 10 minutes ago. I need to see the error."**

Instead of hunting through the UI, you type:

bash

```
prefect flow-run ls --state Failed
```

Grab the run ID from the output, then:

bash

```
prefect flow-run logs <run-id>
```

You'll see the exact Python traceback in your terminal.

**Scenario C: "A flow is stuck in a `Running` state because a worker died."**

You need to clear the queue. You find the run ID and type:

bash

```
prefect flow-run cancel <run-id>
```

**Scenario D: "I need to change the schedule of a deployment in production without editing code."**

You can pause it, edit the schedule in the UI, and resume it:

bash

```
prefect deployment schedule pause "user-pipeline-deployment" --all
# Edit in UI...
prefect deployment schedule resume "user-pipeline-deployment" --all
```

*(Note: The exact CLI syntax for schedule pause/resume changed slightly in Prefect 3.x, so always check `prefect deployment schedule --help`)*.

### **💡 The Golden Rule of the CLI**

If you ever forget a command, use the built-in help:

bash

```
prefect --help
prefect deployment --help
prefect flow-run --help
```

Prefect's CLI is beautifully documented, and the `--help` flag is your best friend.