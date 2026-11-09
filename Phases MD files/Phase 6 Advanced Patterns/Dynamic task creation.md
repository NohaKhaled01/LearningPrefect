# Dynamic task creation

**1. What is `.map()`?**

- **The Problem:** You have a variable-length list of items (unknown at code-writing time) that all need the same task applied to them. A `for` loop is sequential (slow). `.submit()` in a loop is verbose.
- **The Solution:** `.map()` is a one-line shortcut that creates a Task Run for each item in an iterable.
- **Syntax:** `results = my_task.map(my_list)`
- **Return Value:** A list of results, in the same order as the input list.

**2. How `.map()` Works Under the Hood**

- `.map()` is a shortcut for a `for` loop with `.submit()`:
    
    python
    
    ```
    # What you write:
    results = my_task.map(items)
    
    # What Prefect translates it to:
    futures = [my_task.submit(item) for item in items]
    results = [f.result() for f in futures]
    ```
    
- All items are **submitted at the same time** (concurrent).
- The flow **waits for all of them to finish** before returning the full list. It does NOT stream results back one by one — this is only in the case of using the map output in another task, like the following:

```
@task
def log_names(names):
    logger = get_run_logger()
    logger.info(f"Here are the names:{names}")

@flow
def fetch_flow():
    users_id = [1, 2, 3, 4, 5]
    futures = fetch_user.map(users_id) #create the objects

    # Passing the futures directly to a task forces Prefect to resolve them!
    log_names(futures) #give the objects to another task
```

- If you do not hand the map output to another task, you will have to manually stop the flow from existing before finishing the tasks:

```python
@flow
def fetch_flow():
    logger = get_run_logger()
    logger.info("Starting flow")

    start_time = time.time()

    users_id = [1, 2, 3, 4, 5]

    futures = fetch_user.map(users_id) 
    #the return will be a list of prefect objects containing the names

    user_names = [future.result() for future in futures]

    logger.info(f"All user names: {user_names}")

```

**3. The Precise Timing (The Coat Check)**

- `.map()` returns a list of `PrefectFuture` objects (tickets).
- When you access the results, Prefect blocks and waits for **all** items to finish.
- <u>It does NOT return item #1's result as soon as item #1 is done. It waits for item #100 too. Then it gives you the full list.</u>
- **Why?** Simplicity. You get a clean, ordered list without managing callbacks.

**4. `unmapped()` (Multiple Arguments)**

- **What it is:** A wrapper that tells `.map()` "do not iterate over this argument; use the same value for every task run."
- **When to use it:** When a task takes multiple arguments and only some of them should vary per iteration.
- **Syntax:**
    
    python
    
    ```
    my_task.map(varying_arg=my_list, constant_arg=unmapped(my_value))
    ```
    
- **Without `unmapped()`:** Prefect would try to pair the first item with the first character of the constant, causing a crash.

**5. When to Use `.map()` vs. `for` Loop**

| **Scenario** | **Use `.map()`?** | **Why?** |
| --- | --- | --- |
| Process 100 independent files | ✅ Yes | No dependencies. All can run at once. |
| Fetch data from 50 APIs | ✅ Yes | Independent calls. |
| Update a shared balance | ❌ No | Each step depends on the previous one. |
| A list where Item B needs Item A's output | ❌ No | Race conditions. Use a `for` loop. |
| Fetch all data, then process it | ✅ Then ❌ | Fetch with `.map()`, process with a `for` loop. |

**6. Dependencies and Race Conditions**

- `.map()` runs all items concurrently. There is no "before" and "after."
- If items depend on each other, they share state (a balance, a file, a database row).
- Concurrent modification of shared state causes **race conditions** (incorrect results).
- **The Fix:** Use a `for` loop for dependent items. The loop waits for each item to finish before starting the next one.

**7. `.map()` with DataFrames**

- **Convert first:** Always convert a pandas column to a plain list: `df["column"].tolist()`.
- **Full rows:** Use `df.to_dict(orient="records")` to get a list of dicts (one per row).
- **Multiple columns:** Pass each column as a separate list, using `unmapped()` for constants.
- **Watch out for numpy types:** Directly passing a Series sends numpy ints/floats, which can break downstream code.

**8. The Scale Limitation (Why You Can't Map 100,000 Rows)**

- **Orchestration Overhead:** 1 mapped item = 1 Task Run = 1 database row + HTTP requests + state transitions. 100,000 items overwhelms the API/DB/UI.
- **Compute Bottleneck:** 100,000 items = 100,000 threads/processes. The worker runs out of memory.
- **Latency:** The orchestration overhead (metadata) dwarfs the actual data processing time.
- **The Solution:** Chunk your data. Map over chunks (100 tasks), not rows (100,000 tasks).
    
    python
    
    ```
    chunks = [df[i:i+1000] for i in range(0, len(df), 1000)]
    results = process_chunk.map(chunks)
    ```
    

**9. The Golden Rule**

- Prefect is an **orchestrator**, not a **distributed compute engine**.
- For massive datasets, use a compute engine (Spark, Dask, Polars) inside a Prefect task.
- Use Prefect to orchestrate the *flow* of work, not to *be* the compute.

**10. Real-Time vs. Batch (Where Prefect Fits)**

- Prefect is NOT for real-time user requests (e-commerce browsing, ordering).
- Real-time traffic is handled by a web stack (Load Balancers, Redis, Kafka, Web Servers).
- Prefect is for **backend batch processes** (order fulfillment, reporting, ETL).
- For backend batch jobs: Chunk the data, use `.map()` over chunks, and set concurrency limits to avoid overwhelming downstream systems.