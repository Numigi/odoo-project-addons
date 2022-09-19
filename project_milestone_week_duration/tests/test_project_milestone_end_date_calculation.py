# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase
from odoo import fields


class TestProjectMilestoneTimeKPI(SavepointCase):

    def test_project_milestone_end_date_calculation(self):
        milestone = self.env['project.milestone'].create({
            "name": "Test End Date Calculation",
            "start_date": fields.Date.from_string("2022-08-01"),
            "duration": 4.5,
        })
        milestone.onchange_date_start_duration()
        assert milestone.target_date == fields.Date.from_string("2022-09-01")

