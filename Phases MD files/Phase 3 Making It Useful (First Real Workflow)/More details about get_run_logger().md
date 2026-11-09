# More details about get_run_logger()

[Log Levels](More%20details%20about%20get_run_logger()/Log%20Levels%203faf18192572806da84af4de038c097e.md)

### **1. "logger is an instance of an object"**

**Yes.** When you write `logger = get_run_logger()`, you are creating an **instance** of a Logger object. The function builds it, customizes it with the current context, and hands it to you. You assign it to the variable `logger`.

### **2. "we start using the object's method later, like info"**

**Yes.** `logger.info()`, `logger.error()`, `logger.warning()` are all methods that belong to that specific Logger instance.

### **3. "the get_run_logger has a built in feature that sends the logs to the UI"**

**Almost perfectly stated.** Just a tiny shift in phrasing:

- The `get_run_logger()` **function** doesn't send the logs.
- The `logger` **object** it returns is the thing that has the built-in feature (the methods) to send the logs.

Think of it like a delivery truck. `get_run_logger()` is the dispatcher who hands you the keys. The `logger` object is the truck. When you call `logger.info()`, you are loading a package into the truck. The truck itself then drives that package to the UI.

### **4. "we create a logger instance inside each task so that the feature sends the context with it"**

**YES. Exactly.**

This is the core reason we do it inside every task. The Logger object is pre-programmed with the context of the task it was born in.

When you call `logger.info("Fetching user...")` inside `fetch_user`, the Logger object says to itself:

"I know I was created inside `fetch_user`. I will attach that ID to this message so the UI knows exactly where it came from."

If you did it in `process_user`, that Logger instance would say:

"I was created inside `process_user`. I will attach that ID instead."

---

### **Which part of the code sends the log to the UI?**

Here is the important distinction: **Your code does not send logs to the UI.**

Your code sends logs to the **Prefect API**. The UI then **reads** those logs from the API.

Let's trace the exact journey of a single log message, using `logger.info("Fetching user...")` as our example:

**Step 1: You press the button (Your code)**

You call `logger.info("Fetching user...")`. You are handing a message to the Logger instance.

**Step 2: The Logger formats and packages it (Inside the Logger object)**

The Logger instance takes your message and wraps it in a neat little package. It adds metadata to the package:

- The message: "Fetching user..."
- The severity: INFO
- The timestamp: 10:45:01 AM
- The Task Run ID: `fetch_user-8a2`
- The Flow Run ID: `primitive-petrel`

**Step 3: The Prefect SDK picks it up (The Hidden Worker)**

Attached to that Logger instance is a "handler." Think of the handler as the delivery driver. The handler takes the packaged log and hands it to the Prefect SDK's internal HTTP client.

**Step 4: The HTTP Request is sent (The SDK)**

The SDK client (the part of the `prefect` package you installed) says: "I have a log package here. I need to send this to the Prefect API." It makes an HTTP POST request to the API URL you configured (which is `api.prefect.cloud` right now).

**Step 5: The API saves it (Prefect Cloud)**

The Prefect Cloud API receives the HTTP request. It looks at the package, extracts the Flow Run ID and Task Run ID, and saves the log message into its database.

**Step 6: The UI reads it (Your Browser)**

You open your web browser and go to the Prefect Cloud UI. The UI constantly asks the API: "Are there any new logs for this flow run?" The API says, "Yes, here is a log from `fetch_user`." The UI then draws it on your screen in the Logs tab.

### **Why this matters**

Understanding this flow explains a few things:

- **Why you need to be logged into Cloud:** The SDK needs to know *where* the API is to send the logs. That's what `prefect cloud login` did—it configured the SDK with the URL of your Cloud API.
- **Why logs appear almost instantly:** The HTTP request is sent the moment you call `logger.info()`. It doesn't wait until the end of the flow.
- **Why you might lose logs if you're offline:** If your internet cuts out and the SDK can't reach the API, that log message won't make it to the UI. (Though Prefect has buffering mechanisms to help with this.)