# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import OutsourcingCase


class TestProjectTask(OutsourcingCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.order_2 = cls.order.copy()

    def test_outsourcing_line_ids(self):
        self.task.outsourcing_line_ids.refresh()
        assert self.task.outsourcing_line_ids == (
            self.order.order_line | self.order_2.order_line
        )

    def test_outsourcing_po_count(self):
        assert self.task.outsourcing_po_count == 2
