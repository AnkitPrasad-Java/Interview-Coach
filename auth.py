import json
import os

AUTH_FILE = "users.json"

# Ensure users.json exists
if not os.path.exists(AUTH_FILE):
    with open(AUTH_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    """Load users from the JSON file."""
    with open(AUTH_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Save users to the JSON file."""
    with open(AUTH_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register(username, password):
    """Register a new user. Returns True if successful, False if username exists."""
    users = load_users()
    if username in users:
        return False  # Username already exists
    users[username] = password  # Store password (consider hashing for security)
    save_users(users)
    return True

def login(username, password):
    """Authenticate user. Returns True if login is successful."""
    users = load_users()
    return users.get(username) == password
