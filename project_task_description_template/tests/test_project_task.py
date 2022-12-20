# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestProjectTask(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["project.task.description.template"].create(
            {"name": "My Template", "description": "Lorem Ipsum"}
        )
        cls.task = cls.env["project.task"].create({"name": "My Task"})

    def test_onchange_description_template(self):
        self.task.description_template_id = self.template
        self.task._onchange_description_template()
        assert self.task.description == self.template.description
