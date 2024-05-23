# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from odoo.tests import Form


class TestProjectChecklist(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # New task
        cls.task = cls.env["project.task"].create({"name": "Test Task"})
        # New project.checklist
        cls.checklist = cls.env["project.checklist"].create(
            {
                "name": "Test Checklist",
                "description": "Test Description",
            }
        )
        # Project.checklist.item
        cls.checklist_item = cls.env["project.checklist.item"].create(
            {
                "checklist_id": cls.checklist.id,
                "name": "Test Checklist Item",
                "description": "Description for Test Checklist Item",
            }
        )
        # assign checklist to task
        cls.task.checklist_id = cls.checklist.id

    def test__01_task_click_done(self):
        task = self.create_task_on_form()
        self.checklist_item = task.checklist_item_ids
        self.checklist_item.click_done()
        self.assertEqual(self.checklist_item.result, "complete")

    def test__02_task_click_cancel(self):
        task = self.create_task_on_form()
        self.checklist_item = task.checklist_item_ids
        self.checklist_item.click_cancel()
        self.assertEqual(self.checklist_item.result, "cancel")

    def test__03_task_onchange_checklist(self):
        task = self.create_task_on_form()
        self.assertEqual(len(task.checklist_item_ids), 1)

    def test__04_make_checklist_item_vals(self):
        vals = self.task._make_checklist_item_vals(self.checklist_item)
        self.assertEqual(vals["name"], "Test Checklist Item")
        self.assertEqual(vals["description"], "Description for Test Checklist Item")
        self.assertEqual(vals["sequence"], 1)  # default value is 1

    def create_task_on_form(self):
        with Form(self.env["project.task"]) as rec:
            rec.name = "Test Task"
            rec.checklist_id = self.checklist
        task = rec.save()
        return task
