# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        for record in self:
            if 'state' in vals and vals['state'] in \
                    ['purchase', 'done'] and record.task_id:
                outsourcing_po = \
                    record.task_id._check_outsourcing_pol()
                if outsourcing_po:
                    record.task_id._create_timesheet_line(outsourcing_po)
        return res
