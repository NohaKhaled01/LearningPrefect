# Phase 4.3: Concurrency - Running in parallel

**1. Sequential vs. Concurrent Execution**

- **Sequential (Default):** Tasks run one after the other. `result = my_task()`. The flow pauses and waits for each task to finish before starting the next one.
- **Concurrent:** Tasks run at the same time. `future = my_task.submit()`. The flow continues immediately without waiting. This is much faster when tasks are independent of each other (Task B doesn't need Task A's output).
- **Analogy:** Sequential is a chef boiling pasta, waiting 10 mins, then chopping onions, waiting 5 mins. Concurrent is a chef boiling pasta *while* chopping onions and making the sauce.

**2. The `.submit()` Method and `PrefectFuture`**

- **`.submit()`:** Tells Prefect to run the task in the background. It returns a `PrefectFuture` object immediately.
- **`PrefectFuture`:** Think of it as a coat check ticket. You hand over your coat (the task), you get a ticket (the future), and you can go do other things.
- **`.result()`:** When you actually need the output of the task, you call `future.result()`. This is the moment the flow pauses and waits for that specific task to finish.
- **Best Practice:** Submit all your independent tasks first, then call `.result()` on all of them at the end. This maximizes concurrency.

**3. Task Runners (Thread vs. Process)**

- **`ThreadPoolTaskRunner` (Default):** Runs tasks in separate threads within the same Python process. It is perfect for **I/O-bound work** (API calls, database queries, file downloads). The threads release the GIL while waiting for external resources, allowing other tasks to run.
- **`ProcessPoolTaskRunner`:** Runs tasks in separate Python processes. It is designed for **CPU-bound work** (heavy math, image processing, ML training). It bypasses Python's Global Interpreter Lock (GIL) by using multiple CPU cores.
- **Syntax:** `@flow(task_runner=ProcessPoolTaskRunner())`

**4. Benchmarking & UI Visualization**

- **The Benchmark:** 3 tasks, each taking 3 seconds.
    - Sequential: ~9.0 seconds.
    - Concurrent: ~3.0 seconds.
- **In the UI:**
    - **Sequential Flow:** Tasks form a vertical "staircase" in the timeline. Each task waits for the previous one to finish.
    - **Concurrent Flow:** Tasks appear side-by-side on the same horizontal line, starting and ending at approximately the same time.

**5. Critical Caveat: The Caching Interference**

- **The Problem:** When benchmarking sequential vs. concurrent in the same script, if caching is enabled, the second flow will instantly read the cached results from the first flow and finish in 0 seconds, ruining the benchmark.
- **The Fix:** Use different inputs for each flow (e.g., `fetch_user(1)` for sequential, `fetch_user(4)` for concurrent), OR ensure caching is not enabled on the task.