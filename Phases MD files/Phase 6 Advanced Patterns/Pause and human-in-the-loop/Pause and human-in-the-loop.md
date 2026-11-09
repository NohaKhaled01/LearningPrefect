# Pause and human-in-the-loop

[Summary](<./Pause and human-in-the-loop Summary.md>)

Imagine a pipeline that trains a machine learning model and automatically deploys it to production.

- **Without HITL:** The model trains, gets deployed, and starts making predictions. If the model is garbage (e.g., 40% accuracy because of a data glitch), it silently ruins the user experience until someone notices.
- **With HITL:** The model trains, pauses, and waits for a data scientist to look at the metrics. The data scientist reviews the accuracy, clicks "Approve," and the model is deployed. If the metrics look bad, the scientist clicks "Reject," and the pipeline stops.

### **🏗️ How `pause_flow_run()` Works**

Prefect provides a function called `pause_flow_run()`. When your flow hits this line, the flow enters a **`Paused`** state.

Here is the crucial part: **The worker stops consuming resources for that flow.** It doesn't sit there in a `while True: sleep(1)` loop burning CPU. The worker is free to pick up other work. The flow just sits in the database, waiting.

When a human "Resumes" the flow (from the UI or API), the worker picks it back up, and the flow **continues exactly where it left off**. All the variables and state are preserved.

### **🧑‍💻 The Code**

Here is a simple example of a pipeline that pauses for approval:

python

```
from prefect import flow, task, get_run_logger
from prefect.flow_runs import pause_flow_run

@task
def train_model():
    logger = get_run_logger()
    logger.info("Training model...")
    return {"accuracy": 0.95, "model_id": "abc-123"}

@task
def deploy_model(model_info):
    logger = get_run_logger()
    logger.info(f"Deploying model{model_info['model_id']} to production!")

@flow
def ml_pipeline():
    logger = get_run_logger()

    # 1. Train the model
    model_info = train_model()

    # 2. Pause and wait for a human to approve
    logger.info("Model trained. Waiting for human approval...")
    pause_flow_run(timeout=3600)  # Wait up to 1 hour

    # 3. This line only runs AFTER the human resumes the flow
    logger.info("Approval received! Deploying...")
    deploy_model(model_info)

if __name__ == "__main__":
    ml_pipeline()
```

### **🎮 How the Human Interacts**

When the flow hits `pause_flow_run()`, here is what happens:

1. **The UI:** The flow run turns purple (the color for `Paused`) in the Prefect UI.
2. **The Human:** A data scientist opens the UI, looks at the logs (which show the accuracy is 0.95), and clicks the **"Resume"** button.
3. **The Flow Continues:** The worker picks up the flow, and `deploy_model()` executes.

### **📥 Passing Data Back to the Flow**

The killer feature of `pause_flow_run()` is that the human can send data back into the flow when they resume it. This is done with `wait_for_input`.

python

```
from prefect import flow, pause_flow_run
from prefect.input import RunInput

# Define what input you expect from the human
class ApprovalInput(RunInput):
    approved: bool
    comments: str

@flow
def pipeline():
    # ... some work ...

    # Pause and wait for structured input
    user_input = pause_flow_run(wait_for_input=ApprovalInput, timeout=3600)

    if user_input.approved:
        print(f"Approved! Comments:{user_input.comments}")
        # ... continue ...
    else:
        print("Rejected. Halting pipeline.")
        # ... stop ...
```

When the flow pauses, the UI will present a **form** to the human with fields for `approved` (a checkbox) and `comments` (a text box). The human fills it out, clicks Resume, and the flow receives that data as a Python object.

### **⏸️ Pause vs. Suspend**

Prefect has two similar functions. It's important to know the difference:

- **`pause_flow_run()`**: The worker keeps a light connection. The flow can be resumed very quickly. Use this for short waits (minutes to hours).
- **`suspend_flow_run()`**: The worker completely disconnects. The flow is suspended indefinitely. It requires a new worker to pick it up when resumed. Use this for long waits (days or weeks).

### **🚫 The Anti-Pattern: Don't Use It for Everything**

HITL is powerful, but don't abuse it. If you have a flow that pauses 10 times a day for trivial approvals, your team will hate you. Use it for high-stakes decisions:

- Deploying a model to production.
- Approving a large financial transaction.
- Signing off on a data quality report before publishing it.

### **Where is the data stored?**

When a Prefect flow is paused, the data isn't stored in a single place. Instead, it's split into two distinct categories: the flow's **state and metadata** are always saved in the Prefect database, while the **actual data (task results)** are only saved if you explicitly enable result persistence.

Here’s a detailed breakdown of where each piece of information lives.

### **🗄️ What is Always Stored: Flow State and Metadata**

Every time a flow pauses, Prefect's orchestration engine updates the flow run's state in its central database to `Paused`. This is not the data your code is processing, but the administrative record that the flow is waiting.

This database, which can be SQLite (the default) or PostgreSQL, is the system of record for all Prefect operations. It reliably stores information such as:

- **Flow and task run states**: The current status of every part of your workflow (e.g., `Paused`, `Completed`, `Failed`).
- **Run history**: A log of all state transitions that have occurred.
- **Logs**: Any messages your flow has generated.
- **Deployment and infrastructure details**: Information about how and where the flow is configured to run.

So, the fact that the flow is paused and needs to be resumed is always saved in the database, ensuring the system knows to wait for input.

### **💾 What is Optional: Task Results and Data**

The actual data your tasks produce—for example, a DataFrame, a trained model, or a string—is considered a **"result"**. By default, Prefect does **not** persist these results.

If you don't enable persistence, the data exists only in the memory of the process running the flow. If that process is restarted or the flow is resumed by a different worker, the data is lost, and the flow will fail with a `MissingResult` error.

To avoid this, you must enable **result persistence**. When enabled, Prefect serializes the return value of your tasks and flows and writes them to a storage location. This allows the state to be retrieved and used when the flow resumes.

### **📍 Where Persisted Results are Stored**

When you enable result persistence, you have several options for where the data is actually written:

- **Local Filesystem (Default)**: If you enable persistence without specifying a storage location, Prefect saves the data locally, by default in the `~/.prefect/storage/` directory. This is suitable for simple, single-server setups.
- **Remote Storage (Recommended for Production)**: For any production or distributed setup, you should configure a remote storage block. This points to a service like **AWS S3, Google Cloud Storage, or Azure Blob Storage**. This ensures that results are accessible from any worker, even if the original machine is no longer available.

### **🔄 Putting It All Together: The Pause-and-Resume Lifecycle**

Here is the sequence of events for a typical paused flow with persistence enabled:

1. **Execution Halts**: Your flow hits a `pause_flow_run()` call.
2. **State is Saved**: Prefect's engine updates the flow run's state to `Paused` in the **database**.
3. **Results are Persisted (If Enabled)**: The return values from any previously completed tasks are serialized and written to the configured **result storage location** (e.g., a local folder or an S3 bucket).
4. **Infrastructure is Freed (Optional)**: Depending on your settings, the worker process may shut down entirely (a "suspended" state), releasing compute resources.
5. **Resumption**: When you click "Resume" in the UI, a worker picks up the flow run. It reads the state from the **database** and retrieves the persisted results from the **storage location** to reconstruct the flow's context, allowing it to continue seamlessly.

In short, the **database** holds the "where" and "what" of the pause, while the **result storage** holds the "data" your flow was working on.