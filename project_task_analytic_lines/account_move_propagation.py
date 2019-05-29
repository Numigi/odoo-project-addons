# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountMoveLine(models.Model):
    """Propagate the task from journal items to analytic lines."""

    _inherit = 'account.move.line'

    def _prepare_analytic_line(self):
        result = super()._prepare_analytic_line()
        for vals in result:
            line = self.browse(vals['move_id'])
            vals['origin_task_id'] = line.task_id.id
        return result
