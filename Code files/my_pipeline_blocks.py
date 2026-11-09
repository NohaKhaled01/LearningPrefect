# %%
from prefect import flow, task, get_run_logger
from prefect.blocks.system import Secret

# %%
@task()
def fetch_user():
    logger = get_run_logger()
    logger.info(f"Fetching user ..")
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
def call_external_api():
    logger = get_run_logger()

    #Load the block that was created earlier
    api_key_block = Secret.load("my-api-key")

    #Get the encryped secret value
    api_key = api_key_block.get()

    logger.info(f"Successfully loaded API key. It starts with: {api_key[:4]}...")
    logger.info("Calling external API with the secret key...")
    return "API response successful"
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

    # Call the external API using the secret block
    api_result = call_external_api() #saves the 'API response successful, not the api key itself
    logger.info(f"API result: {api_result}")
    
    logger.info("User pipeline finished successfully!")

# %%
if __name__ == "__main__":
    user_pipeline()


