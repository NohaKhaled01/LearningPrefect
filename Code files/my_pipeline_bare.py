# %%

# %%
def fetch_user():
    print("Fetching user...")
    return {"name": "alice", "age": 30}

# %%
def process_user(user):
    print("Processing user...")
    user["name"] = user["name"].upper()
    return user

# %%
def save_user(user):
    print(f"Saving user: {user}")

# %%
if __name__ == "__main__":
    user = fetch_user()
    processed = process_user(user)
    save_user(processed)


