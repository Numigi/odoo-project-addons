# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase
from odoo import fields


class TestProjectMilestoneTimelineDynamic(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectMilestoneTimelineDynamic, cls).setUpClass()

        cls.milestone_abc = cls.env['project.milestone'].create({
            "name": "ABC",
            "start_date": "2022-08-01",
            "target_date": "2022-09-30",
        })
        cls.milestone_zzz = cls.env['project.milestone'].create({
            "name": "ZZZ",
            "start_date": "2022-09-01",
            "target_date": "2022-09-15",
        })

        cls.milestone_1 = cls.env['project.milestone'].create({
            "name": "1",
            "start_date": "2022-07-01",
            "target_date": "2022-08-30",
        })
        cls.milestone_2 = cls.env['project.milestone'].create({
            "name": "2",
            "start_date": "2022-08-01",
            "target_date": "2022-09-30",
        })
        cls.milestone_3 = cls.env['project.milestone'].create({
            "name": "3",
            "start_date": "2022-10-01",
            "target_date": "2022-12-30",
            "child_ids": [(4, cls.milestone_1.id), (4, cls.milestone_2.id)]
        })

    def test_update_start_date_end_date_after_adding_dependence(self):
        """ Test update milestone start date and
        end date after adding a new dependence """
        self.milestone_abc.write({
            'child_ids': [(4, self.milestone_zzz.id)]
        })
        assert self.milestone_abc.start_date == \
               fields.Date.from_string("2022-09-16")
        assert self.milestone_abc.target_date == \
               fields.Date.from_string("2022-11-15")

    def test_update_start_date_end_date_after_after_updating_dependence(self):
        """ Test update milestone start date and
                end date after updating milestone dates in dependence """
        self.milestone_1.write({
           'target_date': "2022-09-15"
        })

        # Milestone 3 mustn't change
        assert self.milestone_3.start_date == \
               fields.Date.from_string("2022-10-01")
        assert self.milestone_3.target_date == \
               fields.Date.from_string("2022-12-30")

        self.milestone_1.write({
            'target_date': "2022-10-15"
        })
        # Date start and Date end of Milestone 3 must change
        assert self.milestone_3.start_date == \
               fields.Date.from_string("2022-10-16")
        assert self.milestone_3.target_date == \
               fields.Date.from_string("2023-01-14")

        self.milestone_2.write({
            'start_date': "2022-09-01",
            'target_date': "2022-10-30"
        })

        # Date start and Date end of Milestone 3 must change
        assert self.milestone_3.start_date == \
               fields.Date.from_string("2022-10-31")
        assert self.milestone_3.target_date == \
               fields.Date.from_string("2023-01-29")
