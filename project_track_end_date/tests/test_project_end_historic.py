# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from odoo.exceptions import UserError

from datetime import date


class TestProjectEndHistoric(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectEndHistoric, cls).setUpClass()

        # Test 'Numigi' project
        cls.project = (
            cls.env["project.project"]
            .with_context({"mail_create_nolog": True})
            .create(
                {
                    "name": "Numigi",
                    "date_start": date(2023, 1, 1),
                    "date": date(2023, 1, 8),
                }
            )
        )

        cls.action_context = {
            "default_initial_date": cls.project.date,
            "default_date": cls.project.date,
            "default_project_id": cls.project.id,
            "default_user_id": cls.env.user.id,
            "default_company_id": cls.env.user.company_id.id,
        }

    def test_action_to_wizard(self):
        action = self.project.action_edit_end_date()

        self.assertEqual(action["context"], self.action_context)

    def update_failed_according_to_stage(self):
        with self.assertRaises(UserError):
            self.project.write({"date": date(2023, 1, 15)})

    def test_update_date_from_wizard(self):
        vals = {
            "reason": "Project postponed",
        }
        res = (
            self.env["edit.date.wizard"].with_context(self.action_context
                                                      ).create(vals)
        )
        res.date = date(2023, 1, 15)
        res.refresh()
        res.action_update_date()
        self.assertEqual(self.project.date, date(2023, 1, 15))
        self.assertEqual(self.project.project_end_history_count, 1)
        self.assertTrue(self.project.project_end_history_ids)
        for history in self.project.project_end_history_ids:
            self.assertEqual(history.week_interval_date, 1)
            self.assertEqual(history.total_week_duration, 2)
        self.assertEqual(self.project.expected_week_duration, 2)
