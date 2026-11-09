# Phase 4.1: Error Handling Hooks

An **`on_failure` hook** is a function you write that Prefect automatically calls if the task fails. It receives the task's metadata (the error, the state, the inputs).

python

```
def alert_on_failure(task, task_run, state):
    print(f"ALERT! Task{task.name} failed with state{state}!")

@task(on_failure=[alert_on_failure], retries=1)
def risky_task():
    raise ValueError("Something broke!")
```

In this example, if `risky_task` fails, Prefect calls `alert_on_failure` before triggering the retry. In production, that hook would send a Slack message, create a PagerDuty alert, or trigger another flow.

**Catching failures in a flow:**

You can also use standard Python `try/except` inside your flow to catch a task failure and continue:

python

```
@flow
def my_flow():
    try:
        risky_task()
    except Exception as e:
        logger.error(f"Risky task failed, but the flow continues:{e}")
    # This still runs
    save_user()
```