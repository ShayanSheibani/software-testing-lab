import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import auth_system


class TestUnitAuthSystem(unittest.TestCase):

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

    def test_signup_success(self):
        result = auth_system.signup("shayan", "Strong123!")
        self.assertEqual(result, "Signup successful.")
        self.assertIn("shayan", auth_system.user_db)
        self.assertIn("shayan", auth_system.user_profiles)

    def test_signup_duplicate_user(self):
        result = auth_system.signup("john_doe", "Strong123!")
        self.assertEqual(result, "User already exists.")

    def test_signup_invalid_password(self):
        result = auth_system.signup("new_user", "12345")
        self.assertEqual(result, "Invalid password format.")

    @patch("auth_system.time.sleep", return_value=None)
    def test_login_success(self, mock_sleep):
        result = auth_system.login("john_doe", "Secure123!")
        self.assertTrue(result)

    @patch("auth_system.time.sleep", return_value=None)
    def test_login_wrong_password(self, mock_sleep):
        result = auth_system.login("john_doe", "wrongpass")
        self.assertFalse(result)

    def test_view_profile_existing_user(self):
        profile = auth_system.view_profile("john_doe")
        self.assertEqual(profile["name"], "John")

    def test_update_profile(self):
        result = auth_system.update_profile("john_doe", name="Johnny", email="johnny@example.com")
        self.assertEqual(result, "Profile updated successfully.")
        self.assertEqual(auth_system.user_profiles["john_doe"]["name"], "Johnny")
        self.assertEqual(auth_system.user_profiles["john_doe"]["email"], "johnny@example.com")

    def test_valid_password(self):
        self.assertTrue(auth_system.is_valid_password("Strong123!"))

    def test_invalid_password(self):
        self.assertFalse(auth_system.is_valid_password("weak"))

    @patch("auth_system.smtplib.SMTP")
    def test_send_reset_email_mocked(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = auth_system.send_reset_email("john_doe")

        self.assertEqual(result, "Password reset email sent.")
        mock_server.sendmail.assert_called_once()

    @patch("auth_system.datetime")
    @patch("auth_system.time.sleep", return_value=None)
    def test_login_sets_last_login(self, mock_sleep, mock_datetime):
        fixed_time = datetime(2026, 4, 5, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time

        auth_system.login("john_doe", "Secure123!")

        self.assertEqual(auth_system.user_profiles["john_doe"]["last_login"], fixed_time)


if __name__ == "__main__":
    unittest.main()