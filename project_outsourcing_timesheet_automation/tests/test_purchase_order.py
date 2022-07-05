# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import OutsourcingCase


class TestPurchaseOrder(OutsourcingCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_timesheet_line_automatically(self):
        self.po_order_2.write({"state": 'purchase'})
        assert self.po_order_2.order_line in \
               self.task.timesheet_ids.mapped('purchase_order_line_id')
