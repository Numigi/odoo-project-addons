# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProjectTaskWithContrainsOnMinMax(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        testing_context = {
            'enable_task_max_hours_constraint': True,
        }
        cls.task_a = cls.env['project.task'].with_context(**testing_context).create({
            'name': 'Task A',
        })

    def test_defaulValues(self):
        """ Keep in mind the default case to be sure it passes."""
        self.task_a.write({
            'min_hours': 0,
            'planned_hours': 0,
            'max_hours': 0
        })

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

    def test_whenIdealIsZero_thenConstrainsAreStillApplied(self):
        """ Check that we don't omit the case of planned_hours == 0 and we skip only when it is None."""
        with self.assertRaises(ValidationError):
            self.task_a.write({
                'min_hours': 4,
                'planned_hours': 0,
                'max_hours': 2
            })

    def test_negativeNumbersAreNotAllowed(self):
        with self.assertRaises(ValidationError):
            self.task_a.write({
                'min_hours': -10,
                'planned_hours': -2,
                'max_hours': 0
            })
