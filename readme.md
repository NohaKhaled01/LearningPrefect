# Understanding Prefect - Phases [DeepSeek]

## **Phase 1: Environment Setup & Mental Model**

[**Phase 1: Environment Setup & Mental Model**](./Phase 1 Environment Setup & Mental Model/Phase 1 Environment Setup & Mental Model.md)

- **Install Prefect** — `pip install -U prefect` (requires Python 3.9+). Prefect works in any Python environment you already use.
- **Choose your backend** — You need either a self-hosted Prefect server (`prefect server start`) or a free Prefect Cloud account. Start with Prefect Cloud for the smoothest learning experience; it gives you a UI, logging, and scheduling out of the box without managing infrastructure.
- **Understand what Prefect is NOT** — It is not an execution engine like Spark or Dask. It orchestrates *your* Python functions. It doesn't replace your code; it observes, schedules, retries, and tracks it. Your code stays in your infrastructure (or wherever you deploy it).

---

## **Phase 2: Core Concepts (The Building Blocks)**

[**Phase 2: Core Concepts (The Building Blocks**](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%202%20Core%20Concepts%20(The%20Building%20Blocks%203edf18192572807a9629c932effcd981.md)

- **Flows** — The top-level container. Any Python function becomes a flow with `@flow`. A flow is the core observable, deployable unit and the primary entrypoint to orchestrated work.
- **Tasks** — The smallest unit of observed work. Decorate with `@task`. Tasks give you granular retries, caching, and observability. You can choose how much to break your logic into tasks—there's no wrong level of granularity, only trade-offs in control vs. complexity.
- **Flow Runs vs. Task Runs** — Understand that every execution of a flow creates a *flow run*, and every task within it creates a *task run*. Each has its own state (Pending, Running, Completed, Failed, etc.). This distinction is fundamental to how Prefect tracks and recovers work.
- **States** — Prefect's state machine is what enables recovery. A task can be in `Retrying`, `Cached`, `Failed`, etc. Flows and tasks transition through states, and you can hook into these transitions for custom logic.
- **The UI** — Open the Prefect UI (Cloud dashboard or `http://localhost:4200` for self-hosted). See your flow runs, task dependencies, logs, and state transitions in real time. This is how you debug and monitor.

---

## **Phase 3: Making It Useful (First Real Workflow)**

[**Phase 3: Making It Useful (First Real Workflow)**](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%203%20Making%20It%20Useful%20(First%20Real%20Workflow)%203edf181925728061abfed8c3dbc2f577.md)

- **Write a flow with tasks** — Take a simple script (e.g., fetch data → transform → save) and split it into `@task`-decorated functions called inside a `@flow`. Run it locally. Watch it appear in the UI.
- **Add retries** — Use `@task(retries=2, retry_delay_seconds=10)` to handle transient failures (API hiccups, network blips). This is one of the most immediately valuable features.
- **Use logging** — Prefect captures logs automatically. Use `log_prints=True` on your flow to capture `print()` statements, or use `get_run_logger()` for structured logging.
- **Create a Deployment** — A deployment makes your flow remotely configurable and schedulable. The simplest way: call `.serve(name="my-deployment")` at the end of your script. This creates a deployment that runs a local worker to execute your flow on a schedule.
- **Run on a schedule** — Within your deployment, set a cron or interval schedule (e.g., `cron="0 6 * * *"` for daily at 6 AM). Confirm it runs without you manually triggering it.

---

## **Phase 4: Reliability & Observability**

- **Error handling patterns** — Understand how Prefect handles exceptions. A task that raises an exception fails; a flow can catch it or let it propagate. Learn about `on_failure` hooks and custom failure states.

[Phase 4.1: Error Handling Hooks](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%204%201%20Error%20Handling%20Hooks%203f0f1819257280fab35ff0cefe9be2ea.md)

- **Caching** — Use `cache_key_fn` or `cache_policy` on tasks to avoid re-running expensive computations. Understand the difference between in-memory caching and persistent caching across runs.

[Phase 4.2: Caching](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%204%202%20Caching%203eff18192572804587daffbd07d1a891.md)

- **Concurrency** — Use `.submit()` instead of calling tasks directly to run them concurrently. Understand task runners (default is `ThreadPoolTaskRunner`; use `ProcessPoolTaskRunner` for CPU-bound work).

[Phase 4.3: Concurrency - Running in parallel](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%204%203%20Concurrency%20-%20Running%20in%20parallel%203f0f1819257280a3a7d8fa61597daa2d.md)

- **Flow runs and deployment runs** — Distinguish between a *flow run* (one execution) and a *deployment run* (a scheduled/triggered run of a deployment). Understand how Prefect retries, cancels, and resumes runs.

[Phase 4.4: **Flow runs and deployment runs**](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%204%204%20Flow%20runs%20and%20deployment%20runs%203f0f18192572803d9282c1cdd76cbc65.md)

---

## **Phase 5: Deployment & Infrastructure**

[Phase 5 - **Deployment & Infrastructure (minus Blocks)**](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%205%20-%20Deployment%20&%20Infrastructure%20(minus%20Block%203f0f18192572809eb2b3e4f14bc387c2.md)

- **Work Pools & Workers** — A work pool defines *where* and *how* your flows run (e.g., local process, Docker, Kubernetes, cloud VM). A worker polls the pool and executes flows. This is Prefect 3.x's replacement for the older "agents" concept.
- **Blocks** — Prefect's way of storing configuration securely: credentials, cloud storage paths, database connections, etc. Blocks are reusable across deployments. Learn to create a block (e.g., an AWS credential block) and reference it in a deployment.

[Phase 5.2: Blocks & Secrets](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Phase%205%202%20Blocks%20&%20Secrets%203eff181925728076a7b5d9fea9477ad3.md)

- **Deployment methods** — Compare `.serve()` (simplest, local worker), `prefect deploy` CLI, and programmatic deployment via `flow.deploy()`. Know when to use each.
- **Infrastructure as code** — For production, define your work pool and deployment in a `prefect.yaml` or via the Python API. This lets you version-control your orchestration config alongside your code.

[CI/CD Definition](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/CI%20CD%20Definition%203f0f1819257280bcaa4edc1c42ab6930.md)

---

## **Phase 6: Advanced Patterns (When You Need Them)**

- **Event-driven workflows** — Trigger flows based on external events (file arrival in S3, database changes, webhook). Prefect 3.0 has native event and automation support.

[**Event-driven workflows**](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Event-driven%20workflows%203f7f1819257280aab879d12dbeb99a26.md)

- **Pause and human-in-the-loop** — Use `pause_flow_run()` or `suspend_flow_run()` to wait for human approval or external input before continuing. Useful for approval gates in data pipelines.

[**Pause and human-in-the-loop**](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Pause%20and%20human-in-the-loop%203f7f1819257280788b52ca5f87528dc4.md)

- **Dynamic task creation** — Create tasks at runtime based on data (e.g., map over a list of unknown length). Prefect's `.map()` and `unmapped()` are key here.

[**Dynamic task creation**](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Dynamic%20task%20creation%203f7f18192572804199acfb13e34634d7.md)

- **Testing** — Use `prefect_test_harness()` to test flows and tasks without hitting the real API or database. Write unit tests for your task functions independently of Prefect.

[Testing](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Testing%203f7f181925728085ad04e376195a5cb2.md)

- **CLI mastery** — Learn `prefect deployment ls`, `prefect flow-run ls`, `prefect worker start`, `prefect work-pool create`, `prefect block register`. The CLI is often faster than the UI for debugging.

[CLI Mastery](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/CLI%20Mastery%203f7f181925728078ab55c38aef79c84d.md)

---

## **Phase 7: Practical Projects (Consolidation)**

Do at least two of these to cement your knowledge:

- **ETL pipeline** — Fetch from an API → transform with pandas → write to CSV/S3. Add retries on the fetch task and a daily schedule.
- **File processing watcher** — A flow that runs when a new file appears in a directory (or S3 bucket), processes it, and moves it to a "processed" folder. Use events or a polling flow.
- **Parameterized batch job** — A deployment that accepts parameters (e.g., date range) and processes data for that range. Trigger it via the UI and via the CLI.
- **Failure recovery demo** — Intentionally fail a task, configure a retry, and observe Prefect resuming from the last successful point (not from the beginning).

[Notes from Exercises](Understanding%20Prefect%20-%20Phases%20%5BDeepSeek%5D/Notes%20from%20Exercises%203fcf181925728016a2c9e076f8f5165d.md)

---

## **What to Ask / Search When You Get Stuck**

Once you have this foundation, you'll be able to formulate precise questions. For example:

- *"How do I pass a secret from an AWS block to a task?"* → Search: "Prefect block credentials task"
- *"My flow runs but the deployment doesn't trigger on schedule"* → Check: Is a worker running for the work pool? Is the deployment active?
- *"I need to run 1000 tasks in parallel without blowing memory"* → Look into: `ProcessPoolTaskRunner`, concurrency limits, and `task_runner` configuration.
- *"How do I test a flow that calls an external API?"* → Search: "Prefect test harness mock API"

---

## **Recommended Learning Resources**

| **Resource** | **Why** |
| --- | --- |
| **Prefect Foundations** (free Instruqt course) | Structured, hands-on, covers flows/tasks → error handling → caching → Cloud |
| **Official Quickstart** ([docs.prefect.io](https://docs.prefect.io/)) | Fastest path to a running deployment |
| **Tutorial Overview** ([docs-2.prefect.io](https://docs-2.prefect.io/)) | Guided walkthrough of core concepts with clear prerequisites |
| **Prefect 3.0 What's New** | Understand workers, events, and performance improvements if you're starting fresh |
| **Prefect Community Slack** | Fastest place to get answers; the "Marvin" bot is particularly useful for "how do I..." questions |

The key insight is that Prefect is designed to be *incremental*. You can start with a single `@flow` decorator on an existing script and add tasks, retries, deployments, and infrastructure one layer at a time. You don't need to understand everything before you start getting value.