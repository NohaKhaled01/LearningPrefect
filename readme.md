# Learning & Understanding Prefect - Zero to Hero Guide

A guideline for learning how to use Prefect [the data orchestration tool], from the very basics up to advanced concepts like event driven workflows and pausing workflows for human input.

I prepared this guideline as I was learning Prefect myself with DeepSeek AI as my teacher. The phases were devised by DeepSeek, and we (DeepSeek & I) went over the phases one by one, where I understood each concept and wrote its code myself. The explanations and summaries for each phase were written by DeepSeek after finishing the phase.

## How to use it:

This repo can be used as a guideline for your own learning, and you can share it with the AI tool of your choice to help explain parts of it, and to create custom exercises for you to practice on. Phase 7 (practical projects) contains multiple suggested projects to work on as more practice.

Each title contains the summary points, plus detailed notes in the included paths/links.

There are also multiple py files for the code I wrote in each phase, in addition to 4 exercise and their codes in phase 7. Feel free to check them if needed.

## **Phase 1: Environment Setup & Mental Model**

[**Phase 1: Environment Setup & Mental Model**](<./Phases MD files/Phase 1 Environment Setup & Mental Model/Phase 1 Environment Setup & Mental Model.md>)

- **Install Prefect** — `pip install -U prefect` (requires Python 3.9+). Prefect works in any Python environment you already use.
- **Choose your backend** — You need either a self-hosted Prefect server (`prefect server start`) or a free Prefect Cloud account. Start with Prefect Cloud for the smoothest learning experience; it gives you a UI, logging, and scheduling out of the box without managing infrastructure.
- **Understand what Prefect is NOT** — It is not an execution engine like Spark or Dask. It orchestrates *your* Python functions. It doesn't replace your code; it observes, schedules, retries, and tracks it. Your code stays in your infrastructure (or wherever you deploy it).

---

## **Phase 2: Core Concepts (The Building Blocks)**

[**Phase 2: Core Concepts (The Building Blocks)**](<./Phases MD files/Phase 2 Core Concepts (The Building Blocks)/Phase 2 Core Concepts (The Building Blocks).md>)

- **Flows** — The top-level container. Any Python function becomes a flow with `@flow`. A flow is the core observable, deployable unit and the primary entrypoint to orchestrated work.
- **Tasks** — The smallest unit of observed work. Decorate with `@task`. Tasks give you granular retries, caching, and observability. You can choose how much to break your logic into tasks—there's no wrong level of granularity, only trade-offs in control vs. complexity.
- **Flow Runs vs. Task Runs** — Understand that every execution of a flow creates a *flow run*, and every task within it creates a *task run*. Each has its own state (Pending, Running, Completed, Failed, etc.). This distinction is fundamental to how Prefect tracks and recovers work.
- **States** — Prefect's state machine is what enables recovery. A task can be in `Retrying`, `Cached`, `Failed`, etc. Flows and tasks transition through states, and you can hook into these transitions for custom logic.
- **The UI** — Open the Prefect UI (Cloud dashboard or `http://localhost:4200` for self-hosted). See your flow runs, task dependencies, logs, and state transitions in real time. This is how you debug and monitor.

---

## **Phase 3: Making It Useful (First Real Workflow)**

[**Phase 3: Making It Useful (First Real Workflow)**](<./Phases MD files/Phase 3 Making It Useful (First Real Workflow)/Phase 3 Making It Useful (First Real Workflow).md>)

- **Write a flow with tasks** — Take a simple script (e.g., fetch data → transform → save) and split it into `@task`-decorated functions called inside a `@flow`. Run it locally. Watch it appear in the UI.
- **Add retries** — Use `@task(retries=2, retry_delay_seconds=10)` to handle transient failures (API hiccups, network blips). This is one of the most immediately valuable features.
- **Use logging** — Prefect captures logs automatically. Use `log_prints=True` on your flow to capture `print()` statements, or use `get_run_logger()` for structured logging.
- **Create a Deployment** — A deployment makes your flow remotely configurable and schedulable. The simplest way: call `.serve(name="my-deployment")` at the end of your script. This creates a deployment that runs a local worker to execute your flow on a schedule.
- **Run on a schedule** — Within your deployment, set a cron or interval schedule (e.g., `cron="0 6 * * *"` for daily at 6 AM). Confirm it runs without you manually triggering it.

---

## **Phase 4: Reliability & Observability**

- **Error handling patterns** — Understand how Prefect handles exceptions. A task that raises an exception fails; a flow can catch it or let it propagate. Learn about `on_failure` hooks and custom failure states.

[Phase 4.1: Error Handling Hooks](<./Phases MD files/Phase 4 Reliability & Observability/Phase 4 1 Error Handling Hooks.md>)

- **Caching** — Use `cache_key_fn` or `cache_policy` on tasks to avoid re-running expensive computations. Understand the difference between in-memory caching and persistent caching across runs.

[Phase 4.2: Caching](<./Phases MD files/Phase 4 Reliability & Observability/Phase 4 2 Caching.md>)

- **Concurrency** — Use `.submit()` instead of calling tasks directly to run them concurrently. Understand task runners (default is `ThreadPoolTaskRunner`; use `ProcessPoolTaskRunner` for CPU-bound work).

[Phase 4.3: Concurrency - Running in parallel](<./Phases MD files/Phase 4 Reliability & Observability/Phase 4 3 Concurrency - Running in parallel.md>)

- **Flow runs and deployment runs** — Distinguish between a *flow run* (one execution) and a *deployment run* (a scheduled/triggered run of a deployment). Understand how Prefect retries, cancels, and resumes runs.

[Phase 4.4: **Flow runs and deployment runs**](<./Phases MD files/Phase 4 Reliability & Observability/Phase 4 4 Flow runs and deployment runs.md>)

---

## **Phase 5: Deployment & Infrastructure**

[Phase 5 - **Deployment & Infrastructure (minus Blocks)**](<./Phases MD files/Phase 5 Deployment & Infrastructure/Phase 5 - Deployment & Infrastructure (minus Block).md>)

- **Work Pools & Workers** — A work pool defines *where* and *how* your flows run (e.g., local process, Docker, Kubernetes, cloud VM). A worker polls the pool and executes flows. This is Prefect 3.x's replacement for the older "agents" concept.
- **Blocks** — Prefect's way of storing configuration securely: credentials, cloud storage paths, database connections, etc. Blocks are reusable across deployments. Learn to create a block (e.g., an AWS credential block) and reference it in a deployment.

[Phase 5.2: Blocks & Secrets](<./Phases MD files/Phase 5 Deployment & Infrastructure/Phase 5 2 Blocks & Secrets.md>)

- **Deployment methods** — Compare `.serve()` (simplest, local worker), `prefect deploy` CLI, and programmatic deployment via `flow.deploy()`. Know when to use each.
- **Infrastructure as code** — For production, define your work pool and deployment in a `prefect.yaml` or via the Python API. This lets you version-control your orchestration config alongside your code.

[CI/CD Definition](<./Phases MD files/Phase 5 Deployment & Infrastructure/Side Phase CI CD Definition.md>)

---

## **Phase 6: Advanced Patterns (When You Need Them)**

- **Event-driven workflows** — Trigger flows based on external events (file arrival in S3, database changes, webhook). Prefect 3.0 has native event and automation support.

[**Event-driven workflows**](<./Phases MD files/Phase 6 Advanced Patterns/Event-driven workflows/Event-driven workflows.md>)

- **Pause and human-in-the-loop** — Use `pause_flow_run()` or `suspend_flow_run()` to wait for human approval or external input before continuing. Useful for approval gates in data pipelines.

[**Pause and human-in-the-loop**](<./Phases MD files/Phase 6 Advanced Patterns/Pause and human-in-the-loop/Pause and human-in-the-loop.md>)

- **Dynamic task creation** — Create tasks at runtime based on data (e.g., map over a list of unknown length). Prefect's `.map()` and `unmapped()` are key here.

[**Dynamic task creation**](<./Phases MD files/Phase 6 Advanced Patterns/Dynamic task creation.md>)

- **Testing** — Use `prefect_test_harness()` to test flows and tasks without hitting the real API or database. Write unit tests for your task functions independently of Prefect.

[Testing](<./Phases MD files/Phase 6 Advanced Patterns/Testing/Testing.md>)

- **CLI mastery** — Learn `prefect deployment ls`, `prefect flow-run ls`, `prefect worker start`, `prefect work-pool create`, `prefect block register`. The CLI is often faster than the UI for debugging.

[CLI Mastery](<./Phases MD files/Phase 6 Advanced Patterns/CLI Mastery/CLI Mastery.md>)

---

## **Phase 7: Practical Projects (Consolidation)**

Do at least two of these to cement your knowledge:

- **ETL pipeline** — Fetch from an API → transform with pandas → write to CSV/S3. Add retries on the fetch task and a daily schedule.
- **File processing watcher** — A flow that runs when a new file appears in a directory (or S3 bucket), processes it, and moves it to a "processed" folder. Use events or a polling flow.
- **Parameterized batch job** — A deployment that accepts parameters (e.g., date range) and processes data for that range. Trigger it via the UI and via the CLI.
- **Failure recovery demo** — Intentionally fail a task, configure a retry, and observe Prefect resuming from the last successful point (not from the beginning).

[The exercises I did, and my notes from them](<./Phases MD files/Phase 7 Practical Projects (Consolidation)/Notes from Exercises.md>)

---

## **What to Ask / Search When You Get Stuck**

Once you have this foundation, you'll be able to formulate precise questions. For example:

- *"How do I pass a secret from an AWS block to a task?"* → Search: "Prefect block credentials task"
- *"My flow runs but the deployment doesn't trigger on schedule"* → Check: Is a worker running for the work pool? Is the deployment active?
- *"I need to run 1000 tasks in parallel without blowing memory"* → Look into: `ProcessPoolTaskRunner`, concurrency limits, and `task_runner` configuration.
- *"How do I test a flow that calls an external API?"* → Search: "Prefect test harness mock API"

---

## **Recommended Learning Resources**

The key insight is that Prefect is designed to be *incremental*. You can start with a single `@flow` decorator on an existing script and add tasks, retries, deployments, and infrastructure one layer at a time. You don't need to understand everything before you start getting value.

| **Resource** | **Why** |
| --- | --- |
| **Prefect Foundations** (free Instruqt course) | Structured, hands-on, covers flows/tasks → error handling → caching → Cloud |
| **Official Quickstart** ([docs.prefect.io](https://docs.prefect.io/)) | Fastest path to a running deployment |
| **Tutorial Overview** ([docs-2.prefect.io](https://docs-2.prefect.io/)) | Guided walkthrough of core concepts with clear prerequisites |
| **Prefect 3.0 What's New** | Understand workers, events, and performance improvements if you're starting fresh |
| **Prefect Community Slack** | Fastest place to get answers; the "Marvin" bot is particularly useful for "how do I..." questions |