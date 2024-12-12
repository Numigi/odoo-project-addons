# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestEstimatedHours(TransactionCase):
    def setUp(self):
        super().setUp()
        self.milestone = self.env["project.milestone"].create(
            {"name": "My Milestone", "estimated_hours": 10}
        )
        self.milestone_copy = self.milestone.copy()

    def test_estimated_hours_copy(self):
        assert (
            self.milestone.estimated_hours == self.milestone_copy.estimated_hours == 10
        )
