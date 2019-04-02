# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime
from odoo import fields
from odoo.exceptions import ValidationError
from .common import OutsourcingCase


class TestOutsourcingPurchaseOrder(OutsourcingCase):

    def test_if_is_outsourcing__project_is_required(self):
        with pytest.raises(ValidationError):
            self.order.project_id = False

    def test_if_is_outsourcing__task_is_required(self):
        with pytest.raises(ValidationError):
            self.order.task_id = False

    def test_on_purchase_create__project_propagated_to_order_lines(self):
        assert self.order.order_line.account_analytic_id.project_ids == self.project

    def test_on_line_create__project_propagated(self):
        new_line = self.order.order_line.copy({'account_analytic_id': False})
        assert new_line.account_analytic_id.project_ids == self.project

    def test_on_project_changed__project_propagated_to_order_lines(self):
        new_project = self.project.copy()
        new_task = self.task.copy({'project_id': new_project.id})
        self.order.write({
            'project_id': new_project.id,
            'task_id': new_task.id,
        })
        assert self.order.order_line.account_analytic_id.project_ids == new_project
