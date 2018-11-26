# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProjectTaskWithContrainsOnMinMax(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_a = cls.env['project.task'].create({'name': 'Task A'})

    def test_whenIdealDifferent0_thenMinHasToBeLesserThanIdeal(self):
        with self.assertRaises(ValidationError):
            self.task_a.write({
                'planned_hours': 10,
                'min_hours': 11
            })

    def test_whenIdealDifferent0_theMinCanBeEqualToIdeal(self):
        self.task_a.write({
            'planned_hours': 10,
            'min_hours': 10,
            'max_hours': 11,
        })
        assert self.task_a.min_hours == 10

    def test_whenIdealDifferent0_thenMaxHasToBeGreaterThanIdeal(self):
        with self.assertRaises(ValidationError):
            self.task_a.write({
                'planned_hours': 10,
                'max_hours': 9
            })

    def test_whenIdealDifferent0_theMaxCanBeEqualToIdeal(self):
        self.task_a.write({
            'planned_hours': 10,
            'max_hours': 10
        })
        assert self.task_a.max_hours == 10

    def test_idealCanBeNone(self):
        """ Just checking that the case where planned_hours is None does not
        raise an error."""
        self.task_a.write({
            'planned_hours': None
        })
        assert self.task_a.max_hours == 0
        assert self.task_a.min_hours == 0
