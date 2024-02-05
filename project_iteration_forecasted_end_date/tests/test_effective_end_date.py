# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase
from datetime import datetime, timedelta


class TestForecastedEndDate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.today = datetime.now().date()
        cls.project_type_a = cls.env["project.type"].create({
            "name": "My Project Type A",
            "exclude_forecasted_end_date": False,
        }
        )
        cls.project = cls.env["project.project"].create({
            "name": "My Project",
            "date_start": datetime.now(),
            "date":  cls.today + timedelta(days=365)
        }
        )

        cls.iteration_1 = cls.env["project.project"].create(
            {"name": "Interation  1",
             "parent_id": cls.project.id,
             "date_start": datetime.now().date(),
             "date":  cls.today+timedelta(days=60)
             }
        )

        cls.iteration_2 = cls.env["project.project"].create(
            {"name": "Interation  2",
             "date_start": datetime.now(),
             "parent_id": cls.project.id,
             "project_type_id": cls.project_type_a.id,
             }
        )

    def test_forecasted_end_date(self):
        self.iteration_2.date = self.today + timedelta(days=120)
        assert self.project.forecasted_end_date == self.iteration_2.date

    def test_forecasted_end_date_with_excluded_iteration(self):
        self.project_type_a.exclude_forecasted_end_date = True
        assert self.project.forecasted_end_date == self.iteration_1.date

