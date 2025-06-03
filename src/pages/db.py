# filepath: c:\Users\athul\OneDrive\Desktop\projects\md first-flet-app\my-app\src\storage\db.py
import os
import json
import asyncio
import flet as ft

app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
app_temp_path = os.getenv("FLET_APP_STORAGE_TEMP")

# Determine the base directory of the application (my-app)
# __file__ is .../my-app/src/pages/db.py
# os.path.dirname(__file__) is .../my-app/src/pages
# os.path.join(os.path.dirname(__file__), "..", "..") is .../my-app
APP_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if app_data_path is None:
    app_data_path = os.path.join(APP_ROOT_DIR, "storage", "data")
    # Create the directory if it doesn't exist
    if not os.path.exists(app_data_path):
        os.makedirs(app_data_path, exist_ok=True)

if app_temp_path is None:
    app_temp_path = os.path.join(APP_ROOT_DIR, "storage", "temp")
    # Create the directory if it doesn't exist
    if not os.path.exists(app_temp_path):
        os.makedirs(app_temp_path, exist_ok=True)

my_file_path = os.path.join(app_data_path, "app_db.json")

class AppDatabase:
    db = {
        "users": {},
        "logined_user": {}
    }


    @staticmethod
    async def initialize():
        """Initialize the database if it doesn't exist"""
        try:
            with open(my_file_path, "r") as f:
                file_content = f.read()
                if file_content:
                    loaded_db = json.loads(file_content)
                    AppDatabase.db = loaded_db
                    # Ensure essential keys exist if loaded db is partial or malformed
                    if "users" not in AppDatabase.db or not isinstance(AppDatabase.db["users"], dict):
                        AppDatabase.db["users"] = {}
                    if "logined_user" not in AppDatabase.db or not isinstance(AppDatabase.db["logined_user"], dict):
                        AppDatabase.db["logined_user"] = {}
                else:
                    # File is empty, initialize with default structure
                    AppDatabase.db = {"users": {}, "logined_user": {}}
            print(f"Database content after initialize: {AppDatabase.db}")
        except FileNotFoundError:
            print(f"Database file '{my_file_path}' not found. Initializing with empty DB.")
            AppDatabase.db = {"users": {}, "logined_user": {}}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{my_file_path}'. Initializing with empty DB.")
            AppDatabase.db = {"users": {}, "logined_user": {}}
        except Exception as e:
            error_msg = str(e)
            print(f"Error initializing database: {error_msg}. Initializing with empty DB.")
            AppDatabase.db = {"users": {}, "logined_user": {}} # Fallback

    @staticmethod
    async def save_db():
        """Save current DB state to the file"""
        with open(my_file_path, "w") as f:
            f.write(json.dumps(AppDatabase.db, indent=4))

    @staticmethod
    def save_db_2():
        """Save current DB state to the file"""
        with open(my_file_path, "w") as f:
            f.write(json.dumps(AppDatabase.db, indent=4))
    @staticmethod
    async def save_user(name, email, password):
        """Save a new user to the database"""
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                users = AppDatabase.db.get("users", {})

                if users.get(email):
                    # Simplified check: if email key exists, user exists.
                    return False, "User with this email already exists"

                new_user = {
                    "name": name,
                    "email": email,
                    "password": password  # In a real app, you should hash this password
                }

                users[email] = new_user
                AppDatabase.db["users"] = users

                await AppDatabase.save_db()
                return True, "User registered successfully"
            except Exception as e:
                error_msg = str(e)
                retry_count += 1
                print(f"Error saving user (attempt {retry_count}/{max_retries}): {error_msg}")
                if "Timeout" in error_msg and retry_count >= max_retries:
                    return False, "Timeout saving user data. Please try again."
                elif retry_count >= max_retries:
                    return False, f"Registration failed after {max_retries} attempts: {error_msg}"
                await asyncio.sleep(1)  # Wait for 1 second before retrying

        return False, "Registration failed after multiple attempts."

    @staticmethod
    async def get_all_users():
        """Get all users from the database"""
        return AppDatabase.db.get("users", {})

    @staticmethod
    async def get_self_user():
        """Get the currently logged-in user's details"""
        user_email = AppDatabase.db.get("logined_user", {}).get("email")
        users_data = AppDatabase.db.get("users", {})
        if user_email and user_email in users_data:
            return users_data[user_email]
        return 
    @staticmethod
    def get_self_user_2():
        """Get the currently logged-in user's details"""
        user_email = AppDatabase.db.get("logined_user", {}).get("email")
        users_data = AppDatabase.db.get("users", {})
        if user_email and user_email in users_data:
            return users_data[user_email]
        return 

    
    @staticmethod
    async def authenticate_user(email, password):
        """Check if user credentials are valid and log them in"""
        try:
            users = await AppDatabase.get_all_users() # Uses static call
            user = users.get(email, {})
            if user.get("email") == email and user.get("password") == password:
                AppDatabase.db["logined_user"] = {"email": email}
                await AppDatabase.save_db() # Uses static call
                return True, user
            return False, "Invalid email or password"
        except Exception as e:
            error_msg = str(e)
            print(f"Authentication error: {error_msg}")

            if "Timeout" in error_msg:
                return False, "Timeout waiting for authentication. Please check your connection and try again."

            return False, f"Login failed: {error_msg}"

    @staticmethod
    async def save_self_user_data(data):
        """Save the currently logged-in user's data"""
        try:
            user_email = AppDatabase.db.get("logined_user", {}).get("email")
            if not user_email:
                return False, "No user is currently logged in"

            users = AppDatabase.db.get("users", {})
            if user_email not in users:
                return False, "User not found"

            # Update user data
            users[user_email].update(data)
            AppDatabase.db["users"] = users

            await AppDatabase.save_db()  # Uses static call
            return True, "User data updated successfully"
        except Exception as e:
            error_msg = str(e)
            print(f"Error saving user data: {error_msg}")
            return False, f"Failed to save user data: {error_msg}"
        
    @staticmethod
    def delete_self_user():
        email = AppDatabase.db.get("logined_user", {}).get("email")
        """Delete a user from the database"""
        try:
            users = AppDatabase.db.get("users", {})
            if email in users:
                del users[email]
                AppDatabase.db["users"] = users
                AppDatabase.save_db_2()  # Uses static call
                return True, "User deleted successfully"
            return False, "User not found"
        except Exception as e:
            error_msg = str(e)
            print(f"Error deleting user: {error_msg}")
            return False, f"Failed to delete user: {error_msg}"

    @staticmethod
    def save_self_user_data_2(data):
        """Save the currently logged-in user's data"""
        try:
            user_email = AppDatabase.db.get("logined_user", {}).get("email")
            if not user_email:
                return False, "No user is currently logged in"

            users = AppDatabase.db.get("users", {})
            if user_email not in users:
                return False, "User not found"

            # Update user data
            users[user_email].update(data)
            AppDatabase.db["users"] = users

            AppDatabase.save_db_2()  # Uses static call
            return True, "User data updated successfully"
        except Exception as e:
            error_msg = str(e)
            print(f"Error saving user data: {error_msg}")
            return False, f"Failed to save user data: {error_msg}"
        
    