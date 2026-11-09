# Summary

**1. What is Human-in-the-Loop?**

- Pausing a flow mid-execution to wait for a human to review, approve, or provide input before continuing.
- Used for high-stakes decisions (ML deployment, financial approvals, data quality sign-off).

**2. The Core Function: `pause_flow_run()`**

- **What it does:** Puts the flow into a `Paused` state. The worker releases resources. The flow waits.
- **Syntax:** `pause_flow_run(timeout=3600)` (waits up to 1 hour).
- **Resuming:** A human clicks "Resume" in the UI. The flow continues exactly where it left off.
- **State Preservation:** All variables and state are preserved across the pause.

**3. Passing Data Back: `wait_for_input`**

- **What it does:** Allows the human to send structured data back into the flow when resuming.
- **Syntax:**
    
    python
    
    ```
    from prefect.input import RunInput
    class MyInput(RunInput):
        approved: bool
        comments: str
    user_input = pause_flow_run(wait_for_input=MyInput)
    ```
    
- **The UI:** Presents a form to the human. The flow receives the filled data as a Python object.

**4. Pause vs. Suspend**

- **`pause_flow_run()`:** Worker keeps a light connection. Fast resume. For short waits (minutes to hours).
- **`suspend_flow_run()`:** Worker disconnects completely. Requires a new worker to resume. For long waits (days to weeks).

**5. Best Practices**

- Use it for high-stakes decisions only. Don't pause for trivial approvals.
- Set a `timeout` so the flow doesn't wait forever.
- Use `wait_for_input` to capture structured feedback, not just a binary "approve/reject."

**🛑 CHECKPOINT 6 (Part 3) COMPLETE.**