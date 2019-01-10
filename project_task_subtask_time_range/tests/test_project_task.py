# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common

from ddt import data, ddt, unpack


@ddt
class TestProjectTaskSubTaskHours(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_no_child = cls.env['project.task'].create({'name': 'Task No Child'})
        cls.task_parent = cls.env['project.task'].create({'name': 'Task Parent'})

        cls.task_child1 = cls.env['project.task'].create({
            'name': 'Task Child 1',
            'parent_id': cls.task_parent.id,
            'min_hours': 0.5,
            'planned_hours': 1.0,
            'max_hours': 2.0
        })
        cls.task_child2 = cls.env['project.task'].create({
            'name': 'Task Child 2',
            'parent_id': cls.task_parent.id,
            'min_hours': 0.5,
            'planned_hours': 1.0,
            'max_hours': 2.0
        })
        cls.task_child3 = cls.env['project.task'].create({
            'name': 'Task Child 3',
            'parent_id': cls.task_parent.id,
            'min_hours': 5,
            'planned_hours': 10,
            'max_hours': 20.0
        })

        cls.task_child4 = cls.env['project.task'].create({
            'name': 'Task Child 4',
            'min_hours': 0.5,
            'planned_hours': 1.0,
            'max_hours': 2.0
        })

    @data('calculated_min_hours', 'calculated_max_hours', 'calculated_planned_hours')
    def test_whenTaskWithNoChild_thenComputedFieldsReturn0(self, field):
        assert 0 == self.task_no_child[field]

    @data(['calculated_min_hours', 6], ['calculated_planned_hours', 12.0], ['calculated_max_hours', 24.0])
    @unpack
    def test_whenTaskWithChild_thenComputedFieldsReturnSumOfChildValues(self, field, expected_value):
        """ Project with a single task assigned to it."""
        assert expected_value == self.task_parent[field]
