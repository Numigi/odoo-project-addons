# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountInvoice(models.Model):
    """Select the task and analytic account on invoice lines for outsourcing."""

    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        result = super()._prepare_invoice_line_from_po_line(line)
        if line.is_outsourcing:
            project = line.order_id.project_id
            result["account_analytic_id"] = project.analytic_account_id.id
            result["task_id"] = line.order_id.task_id.id
        return result
