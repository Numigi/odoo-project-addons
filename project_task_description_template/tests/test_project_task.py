# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestProjectTask(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["project.task.description.template"].create(
            {"name": "My Template", "description": "Lorem Ipsum"}
        )
        cls.task = cls.env["project.task"].create({"name": "My Task"})

    def test_onchange_description_template(self):
        with Form(self.task) as task_form:
            task_form.description_template_id = self.template
        assert self.task.description == self.template.description
