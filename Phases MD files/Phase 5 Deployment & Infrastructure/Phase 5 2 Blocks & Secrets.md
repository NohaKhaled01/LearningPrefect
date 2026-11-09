# Phase 5.2: Blocks & Secrets

**1. Blocks & Secrets (The Problem & Solution)**

- **The Problem:** Hardcoding passwords or API keys into Python scripts is a massive security risk (especially if pushed to Git).
- **The Solution:** Prefect Blocks. A secure, encrypted way to store configuration and credentials in the Prefect API/Database.
- **How it works:** You create a Block in the UI or via Python. The API encrypts it and stores it in the DB. Your code fetches it at runtime.
- **Types of Blocks:** `Secret` (single string), `String` (config), `JSON` (structured config), and integration blocks (AWS, GCP, Postgres, Slack, etc.).
- **Creation via Python:** `Secret(value="my-secret").save("my-block-name")`

**2. The Secret Lifecycle (Load vs. Get)**

- **Create:** You run the bootstrap script (containing the raw secret) once. You then delete it or keep it secure. The secret is now encrypted in the Cloud.
- **Load:** `secret_block = Secret.load("my-block-name")`
    - This is a **Class Method** (called on `Secret`).
    - It fetches the *block object* (the sealed envelope) from the API.
    - It does **not** yet expose the raw secret string.
- **Get:** `raw_value = secret_block.get()`
    - This is an **Instance Method** (called on `secret_block`).
    - It decrypts and returns the actual raw secret into your program's memory.

**3. Security Reality Check (The Trade-offs)**

- **Who runs `.get()`:** The Worker process (the Python interpreter running on your laptop or an Azure VM).
- **The Vulnerability:** If the worker's machine is compromised, the decrypted secret in memory can be stolen.
- **Production Mitigations:**
    - Run workers in isolated, firewalled environments (never personal laptops).
    - Use short-lived credentials (IAM roles, temporary tokens) instead of static keys.
    - Use external secret managers (Vault, AWS Secrets Manager) and store only references in Prefect.
    - Never log raw secrets. Always mask them (`api_key[:4] + "..."`).
- **The Goal:** Minimize the window of exposure; perfect security doesn't exist, managed risk does.

**4. Secret Encapsulation (Best Practice)**

- Tasks should **use** secrets internally but **never return** them.
- Return the *result* of using the secret (e.g., an API response), not the secret value itself.
- This minimizes the "blast radius"—the secret stays in the local memory of the task that needs it and never leaks into the wider flow's memory, logs, or persisted results.
- If another task needs the same secret, it calls `Secret.load()` again in its own context.