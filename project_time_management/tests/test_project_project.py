# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProjectWithMinMax(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env['project.project'].create({'name': 'Project A'})
        analytic_line_pool = cls.env['account.analytic.line']
        task_pool = cls.env['project.task']

        task_a = task_pool.create({
            'name': 'task_a',
            'min_hours': 1.0,
            'max_hours': 4.0,
            'planned_hours': 3.0,
            'project_id': cls.project_a.id,
        })
        analytic_line_pool.create({
            'name': 'line_task_a',
            'account_id': 1,  # use demo account
            'unit_amount': 1.0,
            'task_id': task_a.id,
            'project_id': cls.project_a.id
        })

        cls.project_b = cls.env['project.project'].create({'name': 'Project B'})
        task_b1 = task_pool.create({
            'name': 'task_b1',
            'min_hours': 1.0,
            'max_hours': 4.0,
            'planned_hours': 3.0,
            'project_id': cls.project_b.id,
        })
        analytic_line_pool.create({
            'name': 'line_task_b1',
            'account_id': 1,  # use demo account
            'unit_amount': 1.0,
            'task_id': task_b1.id,
            'project_id': cls.project_b.id
        })
        task_b2 = task_pool.create({
            'name': 'task_b2',
            'min_hours': 2.0,
            'max_hours': 8.0,
            'planned_hours': 6.0,
            'project_id': cls.project_b.id,
        })
        analytic_line_pool.create({
            'name': 'line_task_b2',
            'account_id': 1,  # use demo account
            'unit_amount': 6.0,
            'task_id': task_b2.id,
            'project_id': cls.project_b.id
        })
        # as it is a subtask, should be out of the scope
        task_pool.create({
            'name': 'task_b3',
            'parent_id': task_b2.id,
            'min_hours': 2.0,
            'max_hours': 8.0,
            'planned_hours': 6.0,
            'project_id': cls.project_b.id,
        })

    def test_caseOfSingleTask(self):
        """ Project with a single task assigned to it."""
        assert 1.0 == self.project_a.calculated_min_hours
        assert 4.0 == self.project_a.calculated_max_hours
        assert 3.0 == self.project_a.calculated_planned_hours
        assert 2.0 == self.project_a.calculated_remaining_hours
        assert 1.0 == self.project_a.calculated_effective_hours

    def test_caseMultipleTasks(self):
        """ Project with several tasks assigned to it, with a sub task."""
        assert 3.0 == self.project_b.calculated_min_hours
        assert 12.0 == self.project_b.calculated_max_hours
        assert 9.0 == self.project_b.calculated_planned_hours
        assert 2.0 == self.project_b.calculated_remaining_hours
        assert 7.0 == self.project_b.calculated_effective_hours
