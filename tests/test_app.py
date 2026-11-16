from concurrent.futures import ThreadPoolExecutor
import unittest

from fastapi import HTTPException

from src import app as activities_app


class ActivityWaitlistTests(unittest.TestCase):
    def setUp(self):
        self.original_activities = activities_app.activities
        activities_app.activities = {
            "Club": {
                "max_participants": 1,
                "participants": ["confirmed@example.com"],
                "waitlist": [],
            }
        }

    def tearDown(self):
        activities_app.activities = self.original_activities

    def test_full_activity_signup_joins_waitlist_and_rejects_duplicate(self):
        result = activities_app.signup_for_activity("Club", "waiting@example.com")

        self.assertEqual(result["status"], "waitlisted")
        self.assertEqual(
            activities_app.activities["Club"]["waitlist"],
            ["waiting@example.com"],
        )
        with self.assertRaises(HTTPException) as error:
            activities_app.signup_for_activity("Club", "waiting@example.com")
        self.assertEqual(error.exception.status_code, 400)
        with self.assertRaises(HTTPException) as error:
            activities_app.signup_for_activity("Club", "confirmed@example.com")
        self.assertEqual(error.exception.status_code, 400)

    def test_unregister_promotes_first_waitlisted_student(self):
        activities_app.activities["Club"]["waitlist"] = [
            "first@example.com",
            "second@example.com",
        ]

        result = activities_app.unregister_from_activity(
            "Club", "confirmed@example.com"
        )

        self.assertIn("first@example.com", result["message"])
        self.assertEqual(
            activities_app.activities["Club"]["participants"],
            ["first@example.com"],
        )
        self.assertEqual(
            activities_app.activities["Club"]["waitlist"],
            ["second@example.com"],
        )

    def test_unregister_waitlisted_student_does_not_change_confirmed_roster(self):
        activities_app.activities["Club"]["waitlist"] = ["waiting@example.com"]

        activities_app.unregister_from_activity("Club", "waiting@example.com")

        self.assertEqual(
            activities_app.activities["Club"]["participants"],
            ["confirmed@example.com"],
        )
        self.assertEqual(activities_app.activities["Club"]["waitlist"], [])

    def test_concurrent_signups_do_not_exceed_capacity(self):
        activities_app.activities["Club"]["participants"] = []
        emails = [f"student{index}@example.com" for index in range(20)]

        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(
                executor.map(
                    lambda email: activities_app.signup_for_activity("Club", email),
                    emails,
                )
            )

        activity = activities_app.activities["Club"]
        self.assertEqual(len(activity["participants"]), 1)
        self.assertEqual(len(activity["waitlist"]), 19)
        self.assertEqual(
            sum(result["status"] == "confirmed" for result in results),
            1,
        )
