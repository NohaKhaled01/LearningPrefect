# Phase 5 - Deployment & Infrastructure (minus Blocks)

**1. Work Pools & Workers (The Core Architecture)**

- **Work Pool:** A queue/bucket that categorizes work based on resource needs (CPU, GPU, memory, network). It lives as a configuration in the Prefect API.
- **Worker:** A long-running process that polls a specific Work Pool for new runs. It lives on a machine (your laptop, a server, a Kubernetes pod).
- **The Relationship:** Work Pool = the bucket. Worker = the person emptying the bucket.
- **Types of Work Pools:**
    - **Process:** Runs flow as a subprocess on the Worker's machine.
    - **Docker:** Runs flow in an isolated Docker container. (Best for production reproducibility).
    - **Kubernetes:** Runs flow as a K8s Job. (Best for massive scale).
    - **Cloud VMs (ECS, ACI):** Serverless. (Best for paying only for what you use).

**2. Pull vs. Push Work Pools (Crucial Distinction)**

- **Pull (Hybrid) Pools:** Require a **worker** process on your infrastructure. The worker polls the pool for runs. Examples: `Process`, `Docker`, `Kubernetes`. (You must run `prefect worker start`).
- **Push Pools:** **Do not require a worker.** Prefect Cloud directly submits runs to a serverless provider. Code must come from a Git repo or cloud storage. (Example: Prefect Serverless).
- **Cloud Free Tier Limitation:** Only allows Push/Serverless pools. Pull pools (Process, Docker) require a paid tier OR Self-Hosted Prefect.

**3. Self-Hosted Prefect**

- Prefect is open-source (Apache 2.0). The entire platform (API, UI, DB, Scheduler) can run on your laptop.
- **Setup:**
    1. `prefect server start` (starts the API, UI, DB, Scheduler).
    2. `prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api` (points the SDK to your local server).
    3. Access the UI at `http://127.0.0.1:4200`.
- **Why use it:** Zero cost, full feature access (no tier restrictions), perfect for learning.
- **Trade-off:** Local-only. No cloud persistence. You manage everything.

**4. Deployment Methods: `.serve()` vs `.deploy()` vs `prefect deploy` (CLI)**

- **`.serve()` (Static Infrastructure):**
    - Creates the deployment AND starts a worker in the same terminal.
    - Bypasses the Work Pool system entirely. No work pool is created.
    - Blocks the terminal. Exits only when you press `Ctrl+C`.
    - Ideal for local development, testing, and simple single-machine jobs.
- **`.deploy()` (Dynamic Infrastructure):**
    - Creates the deployment ONLY. Exits immediately.
    - Requires a Work Pool. Assigns the deployment to a specific pool.
    - Requires a separate worker process to be running.
    - Ideal for production, CI/CD, and work-pool-based execution.
- **`prefect deploy` (CLI + `prefect.yaml`):**
    - Declarative, YAML-based configuration (Infrastructure as Code).
    - Ideal for CI/CD pipelines and version-controlled, team-based configurations.

---

**5. The `flow.deploy()` Pattern**

- **The Two-Part Pattern:**

The whole block is answering two questions for Prefect:

1. **Where is the code?** (The `from_source` part)
2. **How do I want to run it?** (The `.deploy` part)

Here is the visual breakdown:

python

```
if __name__ == "__main__":
    user_pipeline.from_source(          # Step 1: Point to the code
        source=str(Path(__file__).parent),
        entrypoint="my_pipeline_deployment_local.py:user_pipeline",
    ).deploy(                           # Step 2: Configure the deployment
        name="user-pipeline-deployment",
        work_pool_name="my-process-pool",
        tags=["demo", "phase5"],
    )
```

**Step 1: `from_source(...)` — Telling Prefect WHERE the code is**

When you run a flow locally (like `user_pipeline()`), Prefect just uses the code that's already in memory. But when you create a **Deployment** and a **Worker** picks it up later, the Worker is a separate process. It needs to go find the code file on disk.

`from_source()` is how you tell it where to look.

**`source=str(Path(__file__).parent)`**

This is the tricky Python part. Let's dissect it:

- `__file__` is a special Python variable that holds the path to the current script (e.g., `C:\Users\nohak\Desktop\Learning Prefect\my_pipeline_deployment_local.py`).
- `Path(__file__).parent` takes that path and goes up one level to get just the *folder* (e.g., `C:\Users\nohak\Desktop\Learning Prefect`).
- `str(...)` converts that path object into a plain string, which is what Prefect expects.

**Why do it this way?** Because it's dynamic. If you move your project folder to a different location, the code will still work. It always looks in the folder where the script lives.

**`entrypoint="my_pipeline_deployment_local.py:user_pipeline"`**

Now that Prefect knows the folder, it needs to know the exact file and function to run.

- The part before the colon is the filename: `my_pipeline_deployment_local.py`
- The part after the colon is the flow function name: `user_pipeline`

Think of it like a GPS address: `source` is the city, and `entrypoint` is the street address.

**Step 2: `.deploy(...)` — Telling Prefect HOW to run it**

This part is chained directly onto the end of `from_source()`. It uses the code source you just defined to create the deployment configuration.

**`name="user-pipeline-deployment"`**

The name of the deployment as it will appear in the UI.

**`work_pool_name="my-process-pool"`**

This tells Prefect which Work Pool (which queue) this deployment belongs to. This is the link between the deployment and the worker you started earlier.

**`tags=["demo", "phase5"]`**

Labels for filtering and organization in the UI.

---

**6. `prefect.yaml` (Infrastructure as Code)**

- **What it is:** A declarative YAML file that describes all your deployments, their schedules, and how the worker should retrieve the code.
- **Why use it:** Separates the code (data logic) from the infrastructure config (how/when/where it runs). Version-controlled in Git. CI/CD friendly.
- **Key Sections:**
    - `pull`: How the worker fetches the code (e.g., `git_clone` or `set_working_directory`).
    - `deployments`: A list of all deployment blueprints (name, entrypoint, work pool, tags, schedule).
- **The Command:** `prefect deploy --all` reads the YAML and registers all deployments with the API. It does NOT run the flows. (Similar to `dbt compile`, not `dbt build`).

**7. Production Worker Lifecycle & The Decoupled Architecture**

- **Workers are Services:** In production, workers run 24/7 as `systemd` services, Docker containers, or Kubernetes deployments. They start on server boot and restart automatically on crash.
- **`prefect deploy` is a One-Time Setup:** It registers the deployment with the API and exits. It does NOT touch the worker.
- **The API is the Meeting Point:** The worker polls the API. The API creates runs based on the schedule. The worker picks up runs from the API. The worker and the deployment are completely decoupled.
- **The Timeline:**
    1. Worker starts (server setup, runs forever).
    2. `prefect deploy` runs (CI/CD, registers the blueprint).
    3. A run is triggered (cron or manual).
    4. Worker picks it up and executes it.
    5. Worker goes back to waiting.