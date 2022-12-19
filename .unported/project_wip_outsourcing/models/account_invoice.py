# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountInvoice(models.Model):
    """Select the WIP account on invoice lines for outsourcing.

    If the invoice line is linked to an outsourcing PO line,
    the WIP account is automatically selected.

    The WIP account is taken from the project type.
    If the project type has no WIP account, the standard account is used.
    """

    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        result = super()._prepare_invoice_line_from_po_line(line)
        if line.is_outsourcing:
            project = line.order_id.project_id
            wip_account = project.project_type_id.wip_account_id
            if wip_account:
                result["account_id"] = wip_account.id
        return result
