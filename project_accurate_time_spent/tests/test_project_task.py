# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestProjectTask(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.project = cls.env['project.project'].create({'name': 'My Project'})
        cls.task = cls.env['project.task'].create({
            'project_id': cls.project.id,
            'name': 'Task 1',
            'planned_hours': 20,
            'max_hours': 20,
        })
        cls.sub_task_1 = cls.env['project.task'].create({
            'project_id': cls.project.id,
            'parent_id': cls.task.id,
            'name': 'Sub-task 1',
            'planned_hours': 5,
            'max_hours': 5,
        })
        cls.sub_task_2 = cls.env['project.task'].create({
            'project_id': cls.project.id,
            'parent_id': cls.task.id,
            'name': 'Sub-task 2',
            'planned_hours': 10,
            'max_hours': 10,
        })

    def _add_timesheet_line(self, task, hours):
        self.env['account.analytic.line'].create({
            'name': '/',
            'user_id': self.env.ref('base.user_demo').id,
            'task_id': task.id,
            'project_id': self.project.id,
            'unit_amount': hours,
        })

    def test_ifNoTimeSpent_thenTotalHoursSpentIsZero(self):
        self.assertEqual(self.task.total_hours_spent, 0)

    def test_ifTimeSpentOnSubTask_thenTimeSpentIsReflectedOnTask(self):
        self._add_timesheet_line(self.sub_task_1, 3)
        self.assertEqual(self.task.children_hours, 3)
        self.assertEqual(self.task.effective_hours, 0)
        self.assertEqual(self.task.total_hours_spent, 3)
        self.assertEqual(self.task.remaining_hours, 17)

    def test_ifTimeSpentOnTask_thenTimeSpentIsReflectedOnTask(self):
        self._add_timesheet_line(self.task, 3)
        self.assertEqual(self.task.children_hours, 0)
        self.assertEqual(self.task.effective_hours, 3)
        self.assertEqual(self.task.total_hours_spent, 3)
        self.assertEqual(self.task.remaining_hours, 17)

    def test_ifTimeSpentOn2SubTasks_thenTimeSpentIsReflectedOnTask(self):
        self._add_timesheet_line(self.sub_task_1, 3)
        self._add_timesheet_line(self.sub_task_2, 6)
        self.assertEqual(self.task.children_hours, 9)
        self.assertEqual(self.task.effective_hours, 0)
        self.assertEqual(self.task.total_hours_spent, 9)
        self.assertEqual(self.task.remaining_hours, 11)

    def test_ifTimeSpentOnSubTasksAndOnTask_thenTimeSpentIsReflectedOnTask(self):
        self._add_timesheet_line(self.sub_task_1, 3)
        self._add_timesheet_line(self.task, 6)
        self.assertEqual(self.task.children_hours, 3)
        self.assertEqual(self.task.effective_hours, 6)
        self.assertEqual(self.task.total_hours_spent, 9)
        self.assertEqual(self.task.remaining_hours, 11)

    def test_ifTimeSpentOnSubTasks_thenProgressIsUpdatedOnTask(self):
        self.assertEqual(self.task.progress, 0)
        self._add_timesheet_line(self.sub_task_2, 10)
        self.assertEqual(self.task.progress, 50)  # 100 * time_spent (10) / estimated (20)

    def test_ifTimeSpentOnTaskAndSubTasks_thenProgressIsUpdatedOnTask(self):
        self.assertEqual(self.task.progress, 0)
        self._add_timesheet_line(self.task, 5)
        self._add_timesheet_line(self.sub_task_2, 10)
        self.assertEqual(self.task.progress, 75)  # 100 * time_spent (5 + 10) / estimated (20)

    def test_ifTaskIsArchived_thenProgressIs100(self):
        self.assertEqual(self.task.progress, 0)
        self.task.stage_id = self.env['project.task.type'].search([('fold', '=', True)], limit=1)
        self.assertEqual(self.task.progress, 100)

    def test_ifTaskIsDon_thenProgressIs100(self):
        self.assertEqual(self.task.progress, 0)
        self.task.stage_id = self.env['project.task.type'].search([('fold', '=', True)], limit=1)
        self.assertEqual(self.task.progress, 100)
