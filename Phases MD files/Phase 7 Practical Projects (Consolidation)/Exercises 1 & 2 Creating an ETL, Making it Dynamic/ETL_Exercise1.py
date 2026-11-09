# %%
from prefect import get_run_logger, task, flow
from pathlib import Path

# %%
import requests
import pandas as pd
import os

# %%
url = 'https://jsonplaceholder.typicode.com/posts'

# %% Extract the data, with a try and except block for network issues
@task(retries = 3, retry_delay_seconds = 5)
def extract_data():
  logger = get_run_logger()
  logger.info('Extracting data')

  try:

    response = requests.get(url, timeout =10)
    response.raise_for_status()
    data = response.json()
    logger.info('Extracting done')
    return data

  except requests.exceptions.ConnectionError as e:
    #log a specific message for network issues
    logger.error(f"Network error occurred while fetching data: {e}")
    # Re-raise the exception so Prefect knows the task failed and triggers a retry
    raise

  except Exception as e:
    # Catch any other errors:
    logger.error(f"An unexpected error occurred: {e}")
    raise


# %% Simple transformations to the extracted data
@task
def transform_data(data):
  logger = get_run_logger()
  df = pd.DataFrame(data)
  df.drop(columns = 'body', inplace = True)
  logger.info(f"Deleted column 'body' from data. {len(df)} rows affected")
  return df

# %% Save  data to a local csv file in the current working directory
@task
def save_data(df):
  logger = get_run_logger()
  logger.info(f'Saving file to {os.getcwd()}')
  df.to_csv('df_data.csv', index = False)
  logger.info('Saved file!')

# %% The flow - extract data - transform data - save data
@flow
def etl_pipeline():
  logger = get_run_logger()
  logger.info('Starting ETL pipeline ...')
  data = extract_data()
  df = transform_data(data)
  save_data(df)

  logger.info("User pipeline finished successfully")

# %%
if __name__ == "__main__":
  etl_pipeline.from_source(
    source = str(Path(__file__).parent),
    entrypoint = "ETL_Exercise1.py:etl_pipeline"
    ).deploy(
      name = "etl-pipeline-deployment",
      work_pool_name = "my-process-pool",
      cron = "0 6 * * *", 
      tags = ["exercise1", "etl"]
      )


