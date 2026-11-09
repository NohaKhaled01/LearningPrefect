# Phase 1: Environment Setup & Mental Model

**What is Prefect? (The Big Picture)**

- Prefect is an **orchestration system**, not just a logging library.
- It is like a **Project Manager** or **Air Traffic Controller** for your code. It doesn't do the actual data work; it schedules it, manages traffic, handles retries when things fail, and keeps logs.
- **It is all just code:** The SDK, the Server, the API, and the UI are all just text files full of instructions (Python, JavaScript, HTML) that computers execute. There is no magic.

**2. The Three Main Layers**

- **The Client (Python SDK):** The `prefect` package you `pip install`. It provides the `@flow` and `@task` decorators. It is the "remote control" you use to tell the server what your code is doing.
- **The Server (API + Database):** The "brains." It receives messages from your code, stores run history in a database, and enforces rules (like schedules and retries).
- **The UI (Dashboard):** A web application hosted *alongside* the server. It reads the database and shows you pretty graphs, logs, and statuses in your browser.

**3. The Architecture & Execution Flow (e.g., Azure VM)**

- Your Python code **stays** wherever you put it (laptop, Azure VM, Docker container). Prefect does not run your code on its servers.
- When your code hits a `@task` decorator, the SDK pauses for a millisecond and sends a tiny **HTTP request (metadata)** over the internet to the Prefect API saying: *"Task A started."*
- The API logs it, and sends a response back. Your code then does the actual work **locally on your machine/Azure VM**.
- When the task finishes, the SDK sends another HTTP request: *"Task A finished."*
- The UI reads this from the API and updates the dashboard.

**4. Installation & Hosting Options**

- When you run `pip install prefect`, it's a "two-in-one" package. It downloads *both* the Client (SDK) and the Server code. You just choose which parts to turn on.
- **Option A (Prefect Cloud):** You use the Prefect company's servers. You only use the SDK locally and point it to `api.prefect.cloud`. You don't run the server yourself.
- **Option B (Self-Hosted):** You run `prefect server start` on your own machine or Azure VM. This turns on the API and UI on *your* infrastructure. You point your SDK to your own IP address (e.g., `localhost:4200`).

**5. The Core Mental Model**

- Think of a Contractor (your code) on a construction site (Azure). They have a Walkie-Talkie (the SDK).
- The Project Manager (the API) sits in an office (either Prefect's Cloud or your own Azure VM).
- The Contractor does all the physical work on-site. They just use the Walkie-Talkie to check in with the Project Manager. The Contractor never teleports to the office to do the work.