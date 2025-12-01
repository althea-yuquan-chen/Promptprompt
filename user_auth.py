import sqlite3
import hashlib
import os

# Define the database filename
DB_NAME = "users.db"

class UserAuth:
    def __init__(self):
        """
        Initialize the UserAuth system.
        It automatically checks if the database exists and creates the table if needed.
        """
        self._init_db()

    def _init_db(self):
        """
        Create the 'users' table if it does not exist.
        Columns:
            - id: Unique ID for each user
            - username: The user's login name (must be unique)
            - password_hash: The encrypted version of the password
            - salt: Random data added to the password before hashing (for security)
        """
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def _hash_password(self, password, salt=None):
        """
        Helper function to securely hash a password.
        
        Args:
            password (str): The plain text password.
            salt (str, optional): The salt to use. If None, generates a new one.
            
        Returns:
            tuple: (hashed_password, salt)
        """
        if salt is None:
            # Generate a random 16-byte hex string as salt
            salt = os.urandom(16).hex()
        
        # Combine password and salt, then encode to bytes
        input_str = password + salt
        # Use SHA-256 for hashing
        hashed = hashlib.sha256(input_str.encode()).hexdigest()
        
        return hashed, salt

    def register_user(self, username, password):
        """
        Register a new user in the database.
        
        Args:
            username (str): Desired username.
            password (str): Plain text password.
            
        Returns:
            bool: True if registration is successful, False if username exists.
        """
        # Create security hash
        hashed_password, salt = self._hash_password(password)
        
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # Insert user data securely
            cursor.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)", 
                (username, hashed_password, salt)
            )
            conn.commit()
            conn.close()
            print(f"[System] User '{username}' registered successfully.")
            return True
        except sqlite3.IntegrityError:
            # This happens if the username is already in the database
            print(f"[Error] Username '{username}' already exists.")
            return False
        except Exception as e:
            print(f"[Error] Database error: {e}")
            return False

    def login_user(self, username, password):
        """
        Verify a user's login credentials.
        
        Args:
            username (str): The username.
            password (str): The plain text password to check.
            
        Returns:
            bool: True if credentials match, False otherwise.
        """
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Retrieve the stored hash and salt for this user
        cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_hash, stored_salt = result
            # Re-calculate hash using the input password and the STORED salt
            check_hash, _ = self._hash_password(password, stored_salt)
            
            # Compare the calculated hash with the stored hash
            if check_hash == stored_hash:
                print(f"[System] Login successful. Welcome, {username}!")
                return True
            else:
                print("[Error] Invalid password.")
                return False
        else:
            print("[Error] User not found.")
            return False

# --- Unit Test ---
if __name__ == "__main__":
    auth = UserAuth()
    
    print("--- Test 1: Register New User ---")
    auth.register_user("test_user", "password123")
    
    print("\n--- Test 2: Duplicate Registration (Should Fail) ---")
    auth.register_user("test_user", "password123")
    
    print("\n--- Test 3: Wrong Password Login ---")
    auth.login_user("test_user", "wrong_password")
    
    print("\n--- Test 4: Correct Login ---")
    auth.login_user("test_user", "password123")