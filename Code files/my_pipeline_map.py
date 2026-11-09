# %%
from prefect import flow, task, get_run_logger
import time

# %%
@task
def process_customer(customer_id: int):
    logger = get_run_logger()
    logger.info(f"Processing customer {customer_id}...")
    time.sleep(2)  # Simulate work
    return f"Customer {customer_id} processed"

# %%
@flow
def batch_pipeline():
    logger = get_run_logger()
    logger.info("Starting batch pipeline...")
    
    # A list of customer IDs (could come from a DB query)
    customer_ids = [101, 102, 103, 104, 105]
    
    # Map the task over the list
    results = process_customer.map(customer_ids)
    
    logger.info(f"All results: {results}")

# %%
if __name__ == "__main__":
    batch_pipeline()


