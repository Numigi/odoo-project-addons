# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import InvoiceCase


class TestTaskPropagationOnTimesheet(InvoiceCase):

    def test_on_post__origin_task_propagated_to_analytic_lines(self):
        self._validate_invoice()
        line = self.invoice.mapped('invoice_line_ids.analytic_line_ids')
        assert line.origin_task_id == self.task
