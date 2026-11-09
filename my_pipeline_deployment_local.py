# %%
import random
from prefect import flow, task, get_run_logger
from pathlib import Path
# %%
@task()
def fetch_user():
    logger = get_run_logger()

    logger.info(f"Fetching user ..")

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
    user_pipeline.from_source(
        source = str(Path(__file__).parent),
        entrypoint = "my_pipeline_deployment_local.py:user_pipeline"
    ).deploy(
        name = "user-pipeline-deployment",
        work_pool_name = "my-process-pool",
        tags = ["demo", "phase5"]
    )



