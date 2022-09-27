# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestRemainingHours(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.milestone = cls.env["project.milestone"].create(
            {"name": "My Milestone",
             "estimated_hours": 10,
             "total_hours": 8}
        )

    def test_remaining_hours_copy(self):
        assert self.milestone.remaining_hours == \
               self.milestone.estimated_hours - self.milestone.total_hours
