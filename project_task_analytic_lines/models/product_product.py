# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        """Add the task to move lines generated from invoice lines.

        This method is used by Odoo to convert cash-based accounting into
        accrual accounting.

        Any propagation from invoice lines to account move lines
        must be added here as well.
        """
        result = super()._convert_prepared_anglosaxon_line(line, partner)
        result["task_id"] = line.get("task_id")
        return result
