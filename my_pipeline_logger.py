# %%
from prefect import flow, task, get_run_logger

# %%
@task
def fetch_user():
    #print("Fetching user...")
    logger = get_run_logger()
    logger.info("Fetching user ..")
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


