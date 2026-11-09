# Phase 2: Core Concepts (The Building Blocks

### **1. Flows (`@flow`)**

**The Concept:** A Flow is the top-level container for your work. It is the blueprint for the entire project.

**In Python:** You turn any regular Python function into a Prefect Flow by adding the `@flow` decorator above it.

**In the Analogy:** This is the **Project Blueprint**. It defines the overall goal (e.g., "Build a House" or "Process Daily Sales Data").

- The Flow is what gets scheduled, triggered, and tracked as a single unit in the UI.
- It is the entry point for your orchestration.

### **2. Tasks (`@task`)**

**The Concept:** A Task is a single, distinct unit of work inside your Flow. It is the smallest piece of observable and trackable work.

**In Python:** You add the `@task` decorator above a function.

**In the Analogy:** These are the **Contractor's individual jobs**. "Pour Foundation," "Frame Walls," "Install Roof."

- Tasks are where the magic happens (retries, caching, concurrency).
- You don't *have* to break everything into tasks. You can put all your logic in a Flow. But the more you break it into Tasks, the more control and visibility you get.

### **3. Flow Runs vs. Task Runs**

**The Concept:** This is a crucial distinction between the *definition* of your code and the *execution* of your code.

**In Python:** When you write `def my_flow():`, that is the definition. When you actually execute it (e.g., `my_flow()`), that creates a **Flow Run**.

**In the Analogy:**

- **The Definition (Flow/Task):** The blueprint for the house. It sits on the shelf. Nothing is happening.
- **The Run (Flow Run/Task Run):** The actual construction project happening right now on Tuesday at 2:00 PM.
- Every single time you execute your flow, Prefect creates a new **Flow Run** (with a unique ID), and inside it, a new **Task Run** for every task executed. This is how Prefect keeps track of history. Run it 100 times, you get 100 Flow Runs.

### **4. States**

**The Concept:** Prefect is a state machine. Every Flow Run and Task Run is always in a specific "state." The state tells the Project Manager (the API) exactly what is happening at any given millisecond.

**In the Analogy:** The status update on the walkie-talkie.

**The Core States:**

- **Pending:** "I'm ready to start, but waiting for the go-ahead."
- **Running:** "I am currently doing the work."
- **Completed:** "I finished successfully."
- **Failed:** "I crashed. I need help."
- **Retrying:** "I crashed, but the Project Manager told me to wait 5 seconds and try again."
- **Cached:** "I already did this exact same work yesterday, so I'm skipping it and just reusing yesterday's result."
    
    *Why this matters:* Because Prefect tracks states, it can make intelligent decisions. If a task fails, Prefect knows to trigger a retry. If a task is cached, Prefect knows to skip it.
    

### **5. The UI (Revisited)**

**The Concept:** Now that you know about Flows, Tasks, Runs, and States, the UI will make perfect sense.

**In the Analogy:** The dashboard in the Project Manager's office.

- When you open the UI, you will see a list of **Flow Runs**.
- Click on one, and you will see a visual graph (a DAG - Directed Acyclic Graph) of all the **Task Runs** inside it.
- Each task will be color-coded by its **State** (Green for Completed, Red for Failed, Yellow for Running).
- You can click on any task to read its logs and see exactly why it failed or how long it took.

### **6. Basic Syntax**

[Code Explanation](<./Code Explanation.md>)

python

```
from prefect import flow, task

@task
def my_task():
    pass

@flow
def my_flow():
    my_task()

my_flow() # This triggers a Flow Run
```

### **7. Flows vs. Tasks: The Design Rule**

- **Both are functions.** The decorator (`@flow` or `@task`) assigns their role.
- **Flows** are the Directors/Managers. They orchestrate the order of operations. Flows call Tasks. (Flows can also call Subflows, but that's for advanced modularization).
- **Tasks** are the Actors/Workers. They do the actual, granular work.
- **Why use Tasks?** To unlock retries, caching, concurrency, and granular observability in the UI.
- **Can you put everything in one Flow?** Yes, but you lose all the granular control. You should put your orchestration logic in the Flow, and your actual work in Tasks.