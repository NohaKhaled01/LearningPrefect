# Phase 4.4: Flow runs and deployment runs

**Flow Runs vs. Deployment Runs**

- **Deployment:** The configuration (recipe). It defines *how* and *when* flow runs should be created.
- **Flow Run:** A single execution of a flow. Created by a deployment, a manual trigger, or a local script.
- **"Deployment Run" (Colloquial):** A Flow Run that was created by a deployment's schedule or manual UI trigger.

**Canceling, Pausing, and Resuming**

- **Cancel:** Stop a running flow. `prefect flow-run cancel <id>` or the UI "Cancel" button. Transitions to `Cancelled`.
- **Pause:** `pause_flow_run()` puts the flow into a `Paused` state. Used for human-in-the-loop approvals. Does not consume worker resources.
- **Resume:** Click "Resume" in the UI or call the API to continue from where it paused.
- **Manual Retry:** Failed flows can be retried from the UI. A new Flow Run is created, reusing cached results from the previous run where possible.

python

```
from prefect import flow, pause_flow_run, get_run_logger

@flow
def approval_pipeline():
    logger = get_run_logger()
    logger.info("Starting pipeline...")
    # ... do some work ...

    logger.info("Waiting for human approval...")
    pause_flow_run(timeout=3600)  # Wait up to 1 hour

    logger.info("Approved! Continuing...")
    # ... continue work ...
```