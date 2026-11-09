# Exercise 3 - Running in Parallel

[Exercise3_mapping.py](Exercise%203%20-%20Running%20in%20Parallel/Exercise3_mapping.py)

Script with the passing of user ids that didn’t complete using raise on failure = false:

[Exercise3_mapping.py](Exercise%203%20-%20Running%20in%20Parallel/Exercise3_mapping%201.py)

**1. The Goal of Exercise 3**

- Use `.map()` to fetch data for multiple users concurrently instead of sequentially.
- Simulate slow API responses using `time.sleep()` to observe concurrency in action.

**2. The `.map()` "Gotcha" (Futures vs. Results)**

- **What `.map()` actually returns:** It does **NOT** wait for the tasks to finish. It immediately returns a list of `PrefectFuture` objects (think of them as claim tickets).
- **The Error:** If you log the output of `.map()` directly, you get object references like `<prefect.futures.PrefectConcurrentFuture object at 0x...>`, not the actual data.
- **The Flow Cancellation (CancelledError):** Because `.map()` doesn't wait, the parent flow reaches the end of the code and exits while the tasks are still running in the background. Prefect then cleans up by canceling those running tasks, resulting in a `CancelledError`.
- **The Fix:** You must explicitly redeem the tickets using `.result()` to force the flow to wait and extract the actual data:
    
    python
    
    ```
    futures = fetch_user.map(user_ids)
    user_names = [future.result() for future in futures] # Blocks until all are done
    ```
    

**3. The "Weakest Link" Rule**

- When mapping concurrently, the total execution time is determined by the **slowest** task.
- Even if 4 out of 5 tasks finish in 2 seconds, the flow will wait 13 seconds if the 5th task (e.g., User 1) hits a network error and exhausts 3 retries.

**4. Failure Behavior ("All or Nothing")**

- If one task in the `.map()` fails and exhausts its retries, calling `.result()` on that future raises an exception.
- This crashes the list comprehension, fails the parent flow immediately, and prevents any subsequent tasks (like saving the data) from running.
- The UI will show the successful tasks as green, the failed task as red, and the parent flow as red.

**5. Handling Partial Failures (`raise_on_failure=False,`**or **`return_exceptions=True`** in newer Prefect versions)

- If you want the pipeline to continue even if some items fail (e.g., "save whatever data we can"), you can tell `.result()` not to raise the error.
- **Syntax:**
    
    python
    
    ```
    user_names = []
    for future in futures:
        result = future.result(raise_on_failure=False)
        user_names.append(result)
    
    # Or the list comprehension version:
    user_names = [future.result(raise_on_failure=False) for future in futures]
    ```
    
- **Behavior:** Instead of crashing the flow, the failed future will return the **Exception object** itself. Your `results` list will be a mix of successful data and error objects. You are responsible for handling the error objects in your downstream code:
`['Leanne Graham', 'Ervin Howell', 'Clementine Bauch', 'Patricia Lebsack', <ConnectionError>]`