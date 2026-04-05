import time
import re
from datetime import datetime
import smtplib
import threading
import random

user_db = {
    "john_doe": "Secure123!",
    "jane_doe": "Password!"
}

user_profiles = {
    "john_doe": {"name": "John", "email": "john@example.com", "last_login": None},
    "jane_doe": {"name": "Jane", "email": "jane@example.com", "last_login": None}
}

def login(username, password):
    processing_delay = random.uniform(0.05, 0.2)  # Simulate variable processing delay
    time.sleep(processing_delay)
    if username in user_db and user_db[username] == password:
        user_profiles[username]["last_login"] = datetime.now()
        return True
    return False

def signup(username, password):
    if username in user_db:
        return "User already exists."
    if not is_valid_password(password):
        return "Invalid password format."
    user_db[username] = password
    user_profiles[username] = {"name": username, "email": None, "last_login": None}
    return "Signup successful."

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password) or not re.search(r"[@$!%*?&]", password):
        return False
    return True

def send_reset_email(username):
    print("SMTP called:")
    if username not in user_profiles:
        return "User not found."
    email = user_profiles[username].get("email")
    if email:
        with smtplib.SMTP('localhost') as server:
            server.sendmail("noreply@example.com", email, "Password reset link")
        return "Password reset email sent."
    return "Email not set."

def view_profile(username):
    return user_profiles.get(username, "Profile not found.")

def update_profile(username, name=None, email=None):
    if username in user_profiles:
        if name:
            user_profiles[username]["name"] = name
        if email:
            user_profiles[username]["email"] = email
        return "Profile updated successfully."
    return "User not found."

def delete_account(username, password):
    if login(username, password):
        del user_db[username]
        del user_profiles[username]
        return "Account deleted."
    return "Authentication failed."
