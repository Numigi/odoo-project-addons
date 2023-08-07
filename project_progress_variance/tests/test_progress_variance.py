# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.tests.common import SavepointCase


class TestCustomerReference(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create(
            {"name": "test_project", "allow_timesheets": True}
        )
        cls.task_1 = cls.env["project.task"].create(
            {"name": "test_task_1", "project_id": cls.project.id}
        )

        cls.task_2 = cls.env["project.task"].create(
            {"name": "test_task_2", "project_id": cls.project.id}
        )

    def test_total_progress(self):
        self.assertEqual(self.project.total_progress, 0)
        self._load_analytic_line_remaining_hours_not_updated()
        self.assertEqual(self.project.total_progress, 47.83)

    def test_total_progress_remaining_hours_updated(self):
        self.assertEqual(self.project.total_progress, 0)
        self._load_analytic_line_with_remaining_hours_updated()
        self.assertEqual(self.project.total_progress, 32.5)

    def test_total_real_progress(self):
        self.assertEqual(self.project.total_real_progress, 0)
        self._load_analytic_line_remaining_hours_not_updated()
        self.assertEqual(self.project.total_real_progress, 47.83)

    def test_total_real_progress_remaining_hours_updated(self):
        self.assertEqual(self.project.total_real_progress, 0)
        self._load_analytic_line_with_remaining_hours_updated()
        self.assertEqual(self.project.total_real_progress, 27.08)

    def test_total_progress_variance(self):
        self.assertEqual(self.project.total_progress_variance, 0)
        self._load_analytic_line_remaining_hours_not_updated()
        self.assertEqual(self.project.total_progress_variance, 0)

    def test_total_progress_variance_remaining_hours_updated(self):
        self.assertEqual(self.project.total_progress_variance, 0)
        self._load_analytic_line_with_remaining_hours_updated()
        self.assertEqual(self.project.total_real_progress, 27.08)
        self.assertEqual(self.project.total_progress, 32.5)
        self.assertEqual(self.project.total_progress_variance, -5.42)

    def _load_analytic_line_remaining_hours_not_updated(self):
        self.task_1.planned_hours = 10
        self.task_2.planned_hours = 13
        self._create_analytic_line(
            datetime(2023, 3, 24, 3), tz="EST", task_id=self.task_1, unit_amount=7
        )
        self._create_analytic_line(
            datetime(2023, 3, 24, 3), tz="EST", task_id=self.task_2, unit_amount=4
        )

    def _load_analytic_line_with_remaining_hours_updated(self):
        self.task_1.planned_hours = 30
        self.task_2.planned_hours = 10
        self._create_analytic_line(
            datetime(2023, 3, 24, 3), tz="EST", task_id=self.task_1, unit_amount=5
        )
        self._create_analytic_line(
            datetime(2023, 3, 24, 3), tz="EST", task_id=self.task_2, unit_amount=8
        )
        self.task_1.remaining_hours = 30
        self.task_2.remaining_hours = 5

    def _create_analytic_line(self, datetime_, tz=None, task_id=False, unit_amount=0):
        self.env["account.analytic.line"].with_context(tz=tz).create(
            {
                "date_time": datetime_,
                "project_id": self.project.id,
                "task_id": task_id.id,
                "name": "Test line",
                "unit_amount": unit_amount,
            }
        )
