# Testing

[Summary](<./Summary.md>)

Testing a Prefect flow has a unique challenge: if you run your flow function to test it, it will connect to the real Prefect API, create a real Flow Run, hit the real database, and clutter your UI. You don't want your unit tests polluting your production dashboard.

### **🧪 The Solution: `prefect_test_harness`**

Prefect provides a context manager called `prefect_test_harness` that creates a **temporary, isolated, in-memory database and API** for the duration of your test.

When the test enters the context, it spins up a fake Prefect server. When the test exits, the fake server is destroyed, and all the test data is wiped out. Your real Prefect database is never touched.

### **🧑‍💻 The Code (Using `pytest`)**

Here is a practical example of how to write a unit test for the `user_pipeline` flow we built earlier.

First, make sure you have `pytest` installed:

bash

```
pip install pytest
```

Then, create a file called `test_my_pipeline.py`:

python

```
import pytest
from prefect.testing.utilities import prefect_test_harness
from my_pipeline import user_pipeline, fetch_user

# 1. A fixture to wrap all tests in the harness
@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield

# 2. Test the flow itself
def test_user_pipeline_runs_successfully():
    # This will run against a temporary, in-memory API
    result = user_pipeline()
    # Assert that the flow completed without raising an exception
    assert result is None

# 3. Test individual tasks in isolation
def test_fetch_user_returns_correct_data():
    result = fetch_user.fn()  # .fn() calls the raw function without Prefect orchestration
    assert result == {"name": "alice", "age": 30}
    assert result["name"] == "alice"
```

### **🔍 Breaking Down the Test**

1. **The Fixture (`prefect_test_fixture`):**
    
    The `@pytest.fixture(autouse=True)` line means this fixture runs automatically before *every* test in the file. It wraps the entire test session in the `prefect_test_harness()`. This ensures that no test ever touches your real Prefect server.
    
2. **Testing the Flow (`test_user_pipeline_runs_successfully`):**
    
    We call `user_pipeline()`. The test harness intercepts all API calls and routes them to the temporary in-memory database. We assert that the flow completes successfully (returns `None`).
    
3. **Testing Tasks in Isolation (`test_fetch_user_returns_correct_data`):**
    
    Notice the `.fn()` at the end of `fetch_user.fn()`. This is a crucial Prefect feature. Calling `.fn()` executes the **raw, undecorated Python function**, bypassing all Prefect orchestration. This is perfect for testing the *logic* of your task without spinning up any Prefect machinery at all.
    

### **🎯 Best Practices for Testing Prefect Flows**

| **What to Test** | **How to Test It** |
| --- | --- |
| **The pure logic of a task** | Call `my_task.fn()` directly. No Prefect needed. Fast. |
| **The orchestration (order, retries)** | Use `prefect_test_harness()` and call the flow. |
| **External dependencies (APIs, DBs)** | Mock them with `unittest.mock` or `pytest-mock`. Don't hit real services in tests. |
| **Integration tests** | Run a flow against a staging environment (not production, not the test harness). |

### **⚠️ The Crucial Rule: Mock External Calls**

Even inside the test harness, your code will still try to make real HTTP requests to external APIs or databases. **You must mock these out.**

python

```
from unittest.mock import patch

@patch("my_pipeline.requests.get")
def test_fetch_user_mocks_api(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"name": "alice", "age": 30}

    result = fetch_user.fn()
    assert result["name"] == "alice"
```

The test harness isolates Prefect, but it doesn't isolate the rest of the internet. You have to handle that yourself.

### **🚀 Why This Matters for CI/CD**

Remember CI/CD? You can't have a robust CI/CD pipeline without automated tests. The `prefect_test_harness` is what allows you to run your Prefect flows in a CI environment (like GitHub Actions) without needing a real Prefect server or a real database. It keeps your tests fast, isolated, and reliable.