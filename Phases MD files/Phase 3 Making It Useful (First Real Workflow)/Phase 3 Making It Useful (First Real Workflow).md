# Phase 3: Making It Useful (First Real Workflow)

**1. Logging & Observability (`get_run_logger`)**

- **The Concept:** Replaces `print()` with structured logs that are sent to the Prefect API and saved in the database.
- **How it works:** `get_run_logger()` is a function that returns a **Logger object** (an instance) tied to the current Flow/Task context.

[More details about get_run_logger()](<./More details about get_run_logger().md>)

- **Log Levels (Triage System):**
    - `debug`: Tiny details (mostly for local dev).
    - `info`: Normal events ("Fetching user...").
    - `warning`: Unexpected but handled.
    - `error`: Failed, but continuing (or raising an exception).
    - `critical`: Catastrophic, wake-up-at-3AM emergencies.
- **Under the Hood Flow:** Your code calls `logger.info()` -> The SDK packages the message + context -> SDK sends HTTP request to the API -> API saves to DB -> UI reads from API.
- **Why an API?** Instead of direct DB access, the API acts as a secure gatekeeper (vault), enforces business logic (traffic cop), provides abstraction (menu), and manages concurrency (ticket system).

**2. Retries & Error Handling**

- **Task Retries:** `@task(retries=3, retry_delay_seconds=5)`. Handles transient errors (API blips, network hiccups). Requires a `raise Exception` to trigger the failure state. Prefect's API manages the loop: `Failed` -> `Retrying` -> `Running`.
- **Flow Retries:** `@flow(retries=2)`. A broader safety net. Re-runs the *entire* flow from the beginning. To avoid redundant work, tasks must have **Result Persistence** enabled so Prefect can skip already-completed tasks on the retry.

**3. Deployments, Workers, & Scheduling**

- **The Deployment:** The *configuration* (recipe). Tells Prefect what to run, how (cron), and where (tags). It lives in the Prefect Cloud database.
- **The Worker:** The *execution engine* (chef). A process running on your machine that polls the API and executes the code.
- **`.serve()`:** A shortcut that creates a deployment AND starts a worker in one command. It blocks the terminal, keeping the worker alive.
- **The Scheduler:** Lives inside the **Prefect API** (not the worker). A background process checks the database. When the cron time hits, the API creates a `Scheduled` run. The worker picks it up.
- **Code vs. Metadata:** The API only knows the *metadata* (deployment name, schedule). The actual Python code stays on your local machine. When you restart a worker, it reloads the local file from disk.

**4. Concurrency & Worker Lifecycle (Production Realities)**

- **Overlapping Runs:** By default, Prefect creates a new run at the scheduled time even if the previous one is still running. Fix this by setting a **Concurrency Limit** (limit = 1) on the work pool/queue.
- **Late Runs:** If the worker is offline when a schedule fires, the API creates the run in a `Late` state. It waits for a worker to come back online.
- **Zombie Runs:** If a worker dies *mid-execution*, the run stays stuck in `Running` forever. With a concurrency limit of 1, this blocks the queue.
- **Graceful Shutdown:** Hitting `Ctrl+C` on a `.serve()` worker automatically pauses the deployment before shutting down.
- **Production Best Practices:** In real teams, code lives in Git, deployments are created via CI/CD, workers run in Docker/systemd (auto-restart), and secrets are stored in Blocks (never hardcoded).