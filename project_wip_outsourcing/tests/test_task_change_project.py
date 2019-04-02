# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime
from odoo import fields
from odoo.exceptions import ValidationError
from .common import OutsourcingCase


class TestChangeProjectOnTask(OutsourcingCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.new_project = cls.project.copy()

    def test_if_not_po_confirmed__project_changed_on_po(self):
        self.task.sudo(self.project_user).project_id = self.new_project
        assert self.order.project_id == self.new_project

    def test_if_not_po_confirmed__analytic_account_changed_on_po_line(self):
        self.task.sudo(self.project_user).project_id = self.new_project
        assert self.order.order_line.account_analytic_id == self.new_project.analytic_account_id

    def test_if_po_confirmed__project_can_not_be_changed_on_task(self):
        self.order.sudo(self.purchase_user).button_confirm()
        task_sudo = self.task.sudo(self.project_user)
        with pytest.raises(ValidationError):
            task_sudo.project_id = self.new_project
