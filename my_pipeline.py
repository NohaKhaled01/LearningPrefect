# %%
from prefect import flow, task

# %%
@task
def fetch_user():
    print("Fetching user...")
    return {"name": "alice", "age": 30}

# %%
@task
def process_user(user):
    print("Processing user...")
    user["name"] = user["name"].upper()
    return user

# %%
@task
def save_user(user):
    print(f"Saving user: {user}")

@flow
def user_pipeline():
    user = fetch_user()
    processed = process_user(user)
    save_user(processed)
# %%
if __name__ == "__main__":
    user_pipeline()


