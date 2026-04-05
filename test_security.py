import unittest
import auth_system


class TestSecurityAuthSystem(unittest.TestCase):

    def setUp(self):
        auth_system.user_db.clear()
        auth_system.user_profiles.clear()

        auth_system.user_db.update({
            "john_doe": "Secure123!",
            "jane_doe": "Password!"
        })

        auth_system.user_profiles.update({
            "john_doe": {"name": "John", "email": "john@example.com", "last_login": None},
            "jane_doe": {"name": "Jane", "email": "jane@example.com", "last_login": None}
        })

    def test_sql_like_username_signup(self):
        malicious_username = "john_doe'; DROP TABLE users; --"
        result = auth_system.signup(malicious_username, "Strong123!")

        self.assertEqual(result, "Signup successful.")
        self.assertIn(malicious_username, auth_system.user_db)

    def test_sql_like_username_login(self):
        malicious_username = "john_doe'; DROP TABLE users; --"
        auth_system.signup(malicious_username, "Strong123!")
        result = auth_system.login(malicious_username, "Strong123!")

        self.assertTrue(result)

    def test_weak_password_numeric_only(self):
        self.assertFalse(auth_system.is_valid_password("12345"))

    def test_weak_password_common_word(self):
        self.assertFalse(auth_system.is_valid_password("password"))

    def test_weak_password_no_special_character(self):
        self.assertFalse(auth_system.is_valid_password("Password123"))

    def test_weak_password_no_uppercase(self):
        self.assertFalse(auth_system.is_valid_password("password123!"))

    def test_strong_password(self):
        self.assertTrue(auth_system.is_valid_password("Strong123!"))


if __name__ == "__main__":
    unittest.main()