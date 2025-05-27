# filepath: c:\Users\athul\OneDrive\Desktop\projects\md first-flet-app\my-app\src\storage\db.py
import os
import json
import asyncio
import flet as ft

class UserDatabase:
    def __init__(self, page: ft.Page):
        self.page = page
        self.client_storage = page.client_storage
        
    async def initialize(self):
        """Initialize the database if it doesn't exist"""
        # Try initialization up to 3 times
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                users_json = await self.client_storage.get("users")
                if users_json is None:
                    # Create empty users list if it doesn't exist
                    await self.client_storage.set("users", json.dumps([]))
                    print("Database initialized with empty users list")
                return True
            except Exception as e:
                error_msg = str(e)
                retry_count += 1
                print(f"Error initializing database (attempt {retry_count}/{max_retries}): {error_msg}")
                
                if "Timeout" in error_msg:
                    print(f"Timeout detected during database initialization. Retrying ({retry_count}/{max_retries})...")
                    # Short sleep before retry
                    await asyncio.sleep(0.5)
                else:
                    # If it's not a timeout error, don't retry
                    break
        
        return False
    
    async def save_user(self, name, email, password):
        """Save a new user to the client storage"""
        try:
            # Get existing users or initialize empty list
            users = await self.get_all_users()
            
            # Check if user with this email already exists
            for user in users:
                if user.get("email") == email:
                    return False, "User with this email already exists"
            
            # Create new user record
            new_user = {
                "name": name,
                "email": email,
                "password": password  # In a real app, you should hash this password
            }
            
            # Add to user list
            users.append(new_user)
            
            # Save updated list
            await self.client_storage.set("users", json.dumps(users))
            return True, "User registered successfully"
        except Exception as e:
            print(f"Error saving user: {str(e)}")
            return False, f"Registration failed: {str(e)}"
    
    async def get_all_users(self):
        """Get all users from storage"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                users_json = await self.client_storage.get("users")
                if users_json:
                    return json.loads(users_json)
                return []
            except Exception as e:
                error_msg = str(e)
                retry_count += 1
                print(f"Error retrieving users (attempt {retry_count}/{max_retries}): {error_msg}")
                
                if "Timeout" in error_msg and retry_count < max_retries:
                    print(f"Timeout detected when retrieving users. Retrying ({retry_count}/{max_retries})...")
                    await asyncio.sleep(0.5)
                else:
                    if "Timeout" in error_msg:
                        raise Exception(f"Timeout when retrieving users after {max_retries} attempts. Please check your connection.")
                    return []
        
        return []
    
    async def authenticate_user(self, email, password):
        """Check if user credentials are valid"""
        try:
            users = await self.get_all_users()
            
            for user in users:
                if user.get("email") == email and user.get("password") == password:
                    return True, user
                    
            return False, "Invalid email or password"
        except Exception as e:
            error_msg = str(e)
            print(f"Authentication error: {error_msg}")
            
            if "Timeout" in error_msg:
                return False, "Timeout waiting for authentication. Please check your connection and try again."
            
            return False, f"Login failed: {error_msg}"
