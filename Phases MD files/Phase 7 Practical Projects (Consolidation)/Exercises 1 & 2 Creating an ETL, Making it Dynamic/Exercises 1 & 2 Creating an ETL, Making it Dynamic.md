# Exercises 1 & 2: Creating an ETL, Making it Dynamic

[ETL_Exercise1.py](<./ETL_Exercise1.py>)

[ETL_Exercise2_dynamic.py](<./ETL_Exercise2_dynamic.py>)

**1. The Core ETL Pattern (Exercise 1)**

- **Extract:** Fetch data from an API using `requests`. Handle network errors.
- **Transform:** Convert JSON to a pandas DataFrame, drop unnecessary columns.
- **Load:** Save the DataFrame to a CSV file using `df.to_csv()`.
- **Orchestration:** Use `@task` for the individual steps and `@flow` to chain them together.

**2. Error Handling & Resilience (The Network Blip)**

- **Transient Errors:** Network errors (like `ConnectionResetError`) happen. The internet is flaky.
- **`try/except` Block:** Wrap the `requests.get()` in a `try` block.
- **Catch Specific Errors:** Use `except requests.exceptions.ConnectionError as e:` instead of the built-in `ConnectionError`. `requests` has its own custom exception hierarchy.
- **The `raise` Keyword:** Log the error, then **`raise`** it. If you don't `raise`, Python swallows the error, returns `None`, and Prefect marks the task as `Completed` (which breaks the pipeline). `raise` tells Prefect the task `Failed` so it can trigger a **Retry**.
- **The `timeout` Parameter:** `requests.get(..., timeout=10)`. Prevents the script from hanging forever if the server silently drops the connection. Triggers a `Timeout` exception instead of freezing the worker.

**3. Deployment Architecture & Entrypoints**

- **Deployment Overwriting:** Deployments are identified by their `name`. If you run a `.deploy()` script with a name that already exists (e.g., `"etl-pipeline-deployment"`), Prefect **overwrites** the blueprint. It changes the pointer to the new script. (Script 1 is safe on disk, but the deployment now runs Script 2).
- **The `entrypoint` String:** It is a GPS coordinate: `"filename.py:function_name"`. It tells the Worker exactly which file to open and which function to run.
- **The Worker is Blind:** The Worker doesn't know what the code does. It just reads the `entrypoint` from the deployment blueprint, goes to the `source` directory, and executes the string. (If you point `ETL_Exercise2.py` to an entrypoint of `ETL_Exercise1.py`, the Worker will run the old script!).
- **Multiple Scripts, One Deployer:** You can write a `deploy_all.py` script that imports flows from multiple different files and deploys them all at once. Each deployment gets its own `entrypoint`.
- **Multiple Flows in One Script:** A single Python file can contain multiple `@flow` functions. You can create separate deployments that point to different functions within the same script.

**4. Dynamic Parameters (Exercise 2)**

- **Flow Arguments:** You can add arguments to your flow: `def etl_pipeline(num_posts: int = 10):`.
- **Passing Parameters:** Pass them down to the tasks: `extract_data(num_posts)`.
- **API Quirks:** Different APIs use different parameter names. JSONPlaceholder uses `_limit` (with an underscore), not `limit`. If ignored, it defaults to returning everything.
- **Overriding in UI:** When you click "Run" in the UI, you can pass custom parameters (e.g., `{"num_posts": 3}`). The flow uses the default (`10`) if you don't pass anything.
- **Overriding in CLI:**
prefect deployment run "etl-pipeline-deployment/etl-pipeline" --param num_posts=5

**5. Real-World Debugging Lessons**

- **SQLAlchemy Bug:** If the Prefect Self-Hosted Scheduler fails with `InvalidRequestError`, it's a known bug with SQLAlchemy 2.1. Fix it by pinning the version: `pip install "sqlalchemy<2.1"`.
- **API Typo:** `raise_response()` doesn't exist. It's `raise_for_status()`.
- **Global Variables vs. In-Memory:** The data passed between tasks (e.g., the `df` from `transform_data` to `save_data`) lives in the worker's memory. It is not saved to the database unless you enable Result Persistence.