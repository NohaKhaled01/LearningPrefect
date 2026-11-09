# %%
import random
from prefect import flow, task, get_run_logger

# %%
# Global counter to simulate a flaky API
attempt_count = 0

# %%
@task(retries = 3, retry_delay_seconds=5)
def fetch_user():
    global attempt_count
    logger = get_run_logger()
    attempt_count += 1

    logger.info(f"Fetching user .. (Attempt{attempt_count})")

    # Simulate a failure on the first two attempts
    if attempt_count < 3:
        logger.warning(f"API is down! Attempt {attempt_count} failed. Retrying...")
        raise ConnectionError("API is temporarily down!")

    logger.info("API succeeded! User fetched.")
    return {"name": "alice", "age": 30}

# %%
@task
def process_user(user):
    #print("Processing user...")
    logger = get_run_logger()
    logger.info("Processing user ..")
    user["name"] = user["name"].upper()
    return user

# %%
@task
def save_user(user):
    #print(f"Saving user: {user}")
    logger = get_run_logger()
    logger.info(f"Saving user: {user}")

# %%
@flow
def user_pipeline():
    logger = get_run_logger()
    logger.info("Starting user pipeline ..")

    user = fetch_user()
    processed = process_user(user)
    save_user(processed)

    logger.info("User pipeline finished successfully.")

# %%
if __name__ == "__main__":
    user_pipeline()


