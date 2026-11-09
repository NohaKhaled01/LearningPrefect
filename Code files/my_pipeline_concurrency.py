# %%
from prefect import flow, task, get_run_logger
import time

# %%
@task()
def fetch_user(user_id: int):
    logger = get_run_logger()
    logger.info(f"Fetching user: {user_id} ...")
    time.sleep(3) #simulate a 3 second api call
    return {"id": user_id, "name": f"user_{user_id}"}

# %%
@flow(name = "Sequential Pipeline")
def sequential_user_pipeline():
    logger = get_run_logger()
    logger.info("Starting Sequential pipeline ..")

    start_time = time.time()

    # Submitting the tasks .. they will run in series
    user1 = fetch_user(1)
    user2 = fetch_user(2)
    user3 = fetch_user(3)

    end_time = time.time()


    logger.info(f"Fetched: {user1}, {user2}, {user3}")
    logger.info(f"Total time: {end_time - start_time:.2f} seconds")

    logger.info("User pipeline finished successfully!")

# %%
@flow(name = "Concurrent Pipeline")
def concurrent_user_pipeline():
    logger = get_run_logger()
    logger.info("Starting Concurrent pipeline ..")

    start_time = time.time()

    # Submitting the tasks all at once .. they will run in parallel
    future1 = fetch_user.submit(1)
    future2 = fetch_user.submit(2)
    future3 = fetch_user.submit(3)

    # Login their results to the variables when they are finished
    user1 = future1.result()
    user2 = future2.result()
    user3 = future3.result()

    end_time = time.time()


    logger.info(f"Fetched: {user1}, {user2}, {user3}")
    logger.info(f"Total time: {end_time - start_time:.2f} seconds")

    logger.info("User pipeline finished successfully!")

# %%
if __name__ == "__main__":
    sequential_user_pipeline()
    concurrent_user_pipeline()


