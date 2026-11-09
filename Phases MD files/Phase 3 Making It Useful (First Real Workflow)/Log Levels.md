# Log Levels

### **The Severity Scale (Low to High)**

Think of the log levels like a hospital triage system.

**1. `logger.debug()` — The Magnifying Glass**

- **When to use:** When you are developing the code and you want to see every tiny detail. "The variable `x` is currently 5." "Entering the loop for the 3rd time."
- **In Production:** You almost always turn this off. It creates too much noise.
- **The Analogy:** The patient's detailed medical chart. Only the doctor needs to see it.

**2. `logger.info()` — The Narrator**

- **When to use:** Normal, expected events. "Flow started." "Fetched 100 records." "Saved to database."
- **The Analogy:** "Patient checked in at the front desk." Everything is going according to plan.

**3. `logger.warning()` — The Yellow Flag**

- **When to use:** Something unexpected happened, but the code handled it and can continue. You want to know about it, but you don't need to wake up at 3 AM.
- **Example:** `if response.status_code == 429: logger.warning("API rate limit hit. Slowing down...")`
- **The Analogy:** "Patient has a slight fever. We're keeping an eye on it, but they are stable."

**4. `logger.error()` — The Red Flag**

- **When to use:** Something failed. The task cannot complete its job. This usually happens inside an `except` block or an `if` condition where a critical assumption was broken.
- **Example:**
    
    python
    
    ```
    try:
        data = fetch_from_api()
    except ConnectionError:
        logger.error("Failed to connect to the API! Task cannot continue.")
        raise # Re-raise the error so Prefect marks the task as Failed
    ```
    
- **The Analogy:** "Patient needs stitches. The doctor is on it, but this is a problem."
1. **`logger.critical()` — The Siren 🚨**
- **When to use:** Catastrophic failure. The entire system is compromised. This is the "wake me up at 3 AM" level.
- **Example:**
    
    python
    
    ```
    if not database.is_connected():
        logger.critical("DATABASE IS DOWN! Entire pipeline halting. All data at risk!")
        raise SystemExit("Database connection lost")
    ```
    
- **The Analogy:** "Code Blue! Patient's heart stopped! Everyone drop what you're doing!"