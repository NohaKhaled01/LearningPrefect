# Phase 4.2: Caching

**1. Caching Basics**

- **What it is:** Storing the result of a task so that if it is run again with the same inputs, Prefect skips execution and returns the stored result. The state becomes `Cached`.
- **Why use it:** Saves time, money, and compute. Avoids re-running expensive operations (API calls, large downloads).
- **Syntax:**
    
    python
    
    ```
    @task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=5))
    ```
    
- **`task_input_hash`:** A built-in function that hashes all arguments of the task to create the cache key.
- **Expiration:** `cache_expiration` controls how long the cache is valid. After that, the task runs fresh.

**2. Custom Cache Keys (`cache_key_fn`)**

- **Why:** `task_input_hash` uses *all* arguments. If you have "noise" arguments (e.g., `debug`, `retry_count`, `timestamp`) that don't affect the output, changing them will unnecessarily invalidate the cache.
- **How:** Write a function `f(context, *args, **kwargs) -> str | None`.
    - `context`: A Prefect object with metadata (task_run.id, flow_run.id, etc.).
    - `args`: Tuple of positional arguments.
    - `*kwargs`: Dict of keyword arguments.
    - Return a string to enable caching, or `None` to skip it.
- **Example:** `def my_key(context, *args, **kwargs): return f"user-cache-{args[0]}"` (ignores all other arguments).
- **Rule of Thumb:** "Which arguments, if changed, would produce a different result?" Only those should be in the cache key.

**3. Cache Policies (Prefect 3.x)**

- **What it is:** Composable building blocks for cache keys. Combine with `+`, subtract with .
- **Built-in Policies:**
    - `DEFAULT`: Inputs + Task Source + Flow Run ID (safest, least reusable).
    - `INPUTS`: Only inputs (reuses across flows/runs).
    - `TASK_SOURCE`: Includes the task's code (invalidates when code changes).
    - `FLOW_PARAMETERS`: Includes parameters passed to the flow.
    - `NO_CACHE`: Disables caching.
- **Example:** `@task(cache_policy=INPUTS - "debug")` (ignores the `debug` parameter).

**4. In-Memory vs. Persistent Caching**

- **In-Memory (Default):** Cache lives in the worker's memory. Lost when the worker restarts.
- **Persistent:** Cache is saved to external storage (S3, local filesystem, GCS). Survives worker restarts and is shared across workers. Enable with `persist_result=True` on the task.

**5. Flow Caching (Not Supported)**

- Flows always execute from the beginning. Only tasks cache.
- Setting `persist_result=True` on a flow cascades to all tasks inside it, but the flow itself is never skipped.

**6. Python Mutability Gotcha (The `.copy()` Fix)**

- **The Problem:** Dictionaries/lists are mutable and passed by reference. If a cached task returns a dictionary and another task modifies it in-place (`user["name"] = user["name"].upper()`), the cached object is modified too. This causes weird bugs where later calls show the modified value.
- **The Fix:** Inside tasks that modify mutable data, make a copy first: `new_user = user.copy()`.

**7. Prefect Retries vs. Function Arguments**

- Prefect's `@task(retries=3)` does **not** add arguments to your function's signature. It happens outside your code.
- Therefore, Prefect's internal retries do **not** invalidate the cache. `fetch_user(1)` will still cache across retries and flow runs.
- Only manually added "noise" parameters (like a custom `retry_count` argument) affect `task_input_hash`.

**📌 FUTURE TO-DO (Phase 7 Practical Projects):**

- □
    
    Experiment with custom `cache_key_fn` and cache policies in a real project.