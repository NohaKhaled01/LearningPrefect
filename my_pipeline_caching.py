# %%
from prefect import flow, task, get_run_logger
from prefect.blocks.system import Secret
from prefect.tasks import task_input_hash
from datetime import timedelta

# %%
@task(cache_key_fn = task_input_hash, cache_expiration = timedelta(minutes=5))
def fetch_user(user_id: int):
    logger = get_run_logger()
    logger.info(f"Fetching user: {user_id} from the API ..")
    return {"id": user_id, "name": "alice"}

# %%
@task
def process_user(user):
    #print("Processing user...")
    logger = get_run_logger()
    logger.info("Processing user ..")
    user["name"] = user["name"].upper()
    return user

# %%
@flow
def user_pipeline():
    logger = get_run_logger()
    logger.info("Starting the user pipeline ..")

    user1 = fetch_user(1)

    user2 = fetch_user(1)

    user3 = fetch_user(2)

    processed = process_user(user1)
    processed2 = process_user(user3)

    logger.info(f"User 1: {user1}")
    logger.info(f"User 2 (cached): {user2}")
    logger.info(f"User 3: {user3}")
    logger.info("User pipeline finished successfully!")

# %%
if __name__ == "__main__":
    user_pipeline()


