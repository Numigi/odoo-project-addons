# © 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class Project(models.Model):
    _inherit = "project.project"

    def _create_wip_to_cgs_account_move(self, wip_line):
        res = super()._create_wip_to_cgs_account_move(wip_line)
        if res:
            res.no_analytic_lines = False
        return res
