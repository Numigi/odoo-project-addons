# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo.tests import common


class TestProject(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env["project.project"].create({"name": "Project A"})
        cls.task_a = cls.env["project.task"].create({
                "name": "Task A",
                "project_id": cls.project_a.id
            })
        cls.env["account.analytic.line"].create({
                "project_id": cls.project_a.id, "task_id": cls.task_a.id,
                "name": "/", "unit_amount": 1})
        cls.timesheet_user_group = cls.env.ref(
            'hr_timesheet.group_hr_timesheet_user')
        cls.restricted_group = cls.env.ref(
            'project_timesheet_time_control_restricted_group.'
            'group_limited_access_launch_timer')
        cls.demo_user = cls.env.ref('base.user_demo')
        cls.restricted_group.users += cls.demo_user
        cls.timesheet_user_group.users += cls.demo_user
        cls.project_a = cls.project_a.sudo(user=cls.demo_user)
        cls.task_a = cls.task_a.sudo(user=cls.demo_user)

    def test_demo_user_has_restricted_access_to_launch_timer(self):
        has_restricted_group = self.demo_user.has_group(
            'project_timesheet_time_control_restricted_group.'
            'group_limited_access_launch_timer')
        self.assertTrue(has_restricted_group,
                        "`demo` user should belong to the restricted "
                        "group before the test")

    def test_restricted_access_to_launch_timer_in_project_form_view(self):
        view = self.project_a.fields_view_get(False, 'form')
        view_arch = etree.fromstring(view.get('arch'))
        field_node = view_arch.xpath("//button[@name='button_start_work']")
        self.assertEquals(field_node[0].attrib.get('invisible'), '1',
                          "The button 'button_start_work' mustn't be found "
                          "in project form view")

    def test_restricted_access_to_launch_timer_in_project_kanban_view(self):
        view = self.project_a.fields_view_get(False, 'kanban')
        view_arch = etree.fromstring(view.get('arch'))
        field_node = view_arch.xpath("//a[@name='button_start_work']")
        self.assertEquals(field_node, [],
                          "The button 'button_start_work' mustn't be found "
                          "in project kanban view")

    def test_restricted_access_to_launch_timer_in_project_list_view(self):
        view = self.project_a.fields_view_get(False, 'tree')
        view_arch = etree.fromstring(view.get('arch'))
        field_node = view_arch.xpath("//button[@name='button_start_work']")
        self.assertEquals(field_node[0].attrib.get('invisible'), '1',
                          "The button 'button_start_work' mustn't be found "
                          "in project list view")

    def test_restricted_access_to_launch_timer_in_task_list_view(self):
        view = self.task_a.fields_view_get(False, 'tree')
        view_arch = etree.fromstring(view.get('arch'))
        field_node = view_arch.xpath("//button[@name='button_start_work']")
        self.assertEquals(field_node[0].attrib.get('invisible'), '1',
                          "The button 'button_start_work' mustn't be found "
                          "in task list view")

    def test_restricted_access_to_launch_timer_in_task_form_view(self):
        view = self.task_a.fields_view_get(False, 'form')
        view_arch = etree.fromstring(view.get('arch'))
        field_node = view_arch.xpath("//button[@name='button_start_work']")
        self.assertEquals(field_node[0].attrib.get('invisible'), '1',
                          "The button 'button_start_work' mustn't be found "
                          "in task form view")

    def test_restricted_access_to_launch_timer_in_task_kanban_view(self):
        view = self.task_a.fields_view_get(False, 'kanban')
        view_arch = etree.fromstring(view.get('arch'))
        field_node = view_arch.xpath('//a[@name="button_start_work"]')
        self.assertNotEquals(field_node, [],
                             "The button 'button_start_work' must be found "
                             "in task kanban view")

