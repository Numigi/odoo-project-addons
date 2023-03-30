# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Invoice(models.Model):
    """Prevent posting an invoice with a task and a project that dont match."""

    _inherit = "account.move"

    def action_invoice_open(self):
        for line in self.mapped("invoice_line_ids"):
            line._check_task_matches_with_project()

        for tax in self.mapped("tax_line_ids"):
            tax._check_task_matchtax_line_idses_with_project()

        return super().action_invoice_open()

    @api.model
    def invoice_line_move_line_get(self):
        """Add the task to move lines generated from invoice lines."""
        result = super().invoice_line_move_line_get()

        for line_vals in result:
            invoice_line_id = line_vals.get("invl_id")
            if invoice_line_id:
                invoice_line = self.env["account.move.line"].browse(
                    invoice_line_id)
                line_vals["task_id"] = invoice_line.task_id.id

        return result

    @api.model
    def tax_line_move_line_get(self):
        """Add the task to move lines generated from invoice taxes."""
        result = super().tax_line_move_line_get()

        for line_vals in result:
            tax_line = self.env["account.tax"].browse(
                line_vals["invoice_tax_line_id"]
            )
            line_vals["task_id"] = tax_line.task_id.id

        return result

    def inv_line_characteristic_hashcode(self, invoice_line):
        """Group account move lines by task.

        The characteristic hash code is used to group account move lines generated
        from invoice lines.

        All fields that can not be aggregated should be added to the hash.
        """
        result = super().inv_line_characteristic_hashcode(invoice_line)
        return "{}-{}".format(result, invoice_line.get("task_id", "False"))

    def _prepare_tax_line_vals(self, line, tax):
        """If the analytic account is propagated to tax lines, propagate the task.

        This ensures that the task is only and always propagated when the
        analytic account is propagated.
        """
        result = super()._prepare_tax_line_vals(line, tax)

        analytic_account_is_propagated = bool(result["account_analytic_id"])
        result["task_id"] = line.task_id.id if analytic_account_is_propagated else False

        return result
