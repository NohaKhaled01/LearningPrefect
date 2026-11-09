from prefect import task, flow, get_run_logger
import requests, time
from pathlib import Path

@task(retries = 3, retry_delay_seconds = 5)
def fetch_user(user_id):
    logger = get_run_logger()
    logger.info("fetching users details .. ")

    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}", timeout = 10)
        data = response.json()
        name = data['name']
        logger.info(f"Extracted User ID {user_id} with name {name}")
        time.sleep(2)
        return name

    except Exception as e:
        logger.info(f"Ran into an unexpected error: {e}")
        raise

@flow
def fetch_flow():
    logger = get_run_logger()
    logger.info("Starting flow")

    start_time = time.time()

    users_id = [1, 2, 3, 4, 5]

    futures = fetch_user.map(users_id) #the return will be a list of prefect objects containing the names

    user_names = [future.result() for future in futures]

    logger.info(f"All user names: {user_names}")

    end_time = time.time()
    logger.info(f"Total time taken: {end_time - start_time:.2f} seconds")

    logger.info("User pipeline finished successfully")


if __name__ == "__main__":
    fetch_flow.from_source(
    source = str(Path(__file__).parent),
    entrypoint = "Exercise3_mapping.py:fetch_flow"
    ).deploy(
      name = "mapping-pipeline-deployment",
      work_pool_name = "my-process-pool",
      tags = ["exercise3", "concurrent"]
      )
