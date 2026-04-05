import unittest
from unittest.mock import patch, MagicMock
import auth_system


class TestFunctionalAuthSystem(unittest.TestCase):

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

    @patch("auth_system.time.sleep", return_value=None)
    def test_scenario_1_new_user_signup_and_login(self, mock_sleep):
        signup_result = auth_system.signup("alice", "Strong123!")
        login_result = auth_system.login("alice", "Strong123!")

        self.assertEqual(signup_result, "Signup successful.")
        self.assertTrue(login_result)
        self.assertIn("alice", auth_system.user_db)
        self.assertIn("alice", auth_system.user_profiles)

    @patch("auth_system.smtplib.SMTP")
    def test_scenario_2_update_profile_then_reset_password(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        auth_system.signup("bob", "Strong123!")
        update_result = auth_system.update_profile("bob", name="Bobby", email="bob@example.com")
        reset_result = auth_system.send_reset_email("bob")

        self.assertEqual(update_result, "Profile updated successfully.")
        self.assertEqual(reset_result, "Password reset email sent.")
        self.assertEqual(auth_system.user_profiles["bob"]["name"], "Bobby")
        self.assertEqual(auth_system.user_profiles["bob"]["email"], "bob@example.com")

    def test_scenario_3_view_profile_after_multiple_updates(self):
        auth_system.signup("charlie", "Strong123!")
        auth_system.update_profile("charlie", name="Charles")
        auth_system.update_profile("charlie", email="charlie@example.com")

        profile = auth_system.view_profile("charlie")

        self.assertEqual(profile["name"], "Charles")
        self.assertEqual(profile["email"], "charlie@example.com")

    def test_data_consistency_after_operations(self):
        auth_system.signup("david", "Strong123!")
        auth_system.update_profile("david", name="David", email="david@example.com")
        profile = auth_system.view_profile("david")

        self.assertIn("david", auth_system.user_db)
        self.assertIn("david", auth_system.user_profiles)
        self.assertEqual(profile["name"], "David")
        self.assertEqual(profile["email"], "david@example.com")


if __name__ == "__main__":
    unittest.main()