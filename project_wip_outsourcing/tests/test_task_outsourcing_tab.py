# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import OutsourcingCase


class TestTaskOutsourcingTab(OutsourcingCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.order_2 = cls.order.copy()

    def test_outsourcing_line_ids_contains_lines_from_all_po(self):
        assert self.task.outsourcing_line_ids == (
            self.order.order_line | self.order_2.order_line
        )
