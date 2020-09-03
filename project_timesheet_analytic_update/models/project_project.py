# -*- coding: utf-8 -*-
# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _


class ProjectTimesheetAnalyticUpdate(models.Model):
    _inherit = "project.project"

    @api.multi
    def write(self, vals):
        """ Propagate the value of the project's analytic account to the analytic lines of the project."""
        super().write(vals)
        if 'analytic_account_id' in vals:
            timesheets = self.env['account.analytic.line'].sudo().search([('project_id', 'in', self.ids)])
            timesheets.write({"account_id": vals["analytic_account_id"]})
        return True

    @api.onchange("analytic_account_id")
    def _onchange_account_id(self):
        res = {
            "warning": {
                "title": _("Warning!"),
                "message": _(
                    "Please note, you have modified the analytic account. \n"
                    "When saving, the project timelines will be updated with the new analytic "
                    "account < %s >.",
                )
                % self.analytic_account_id.name,
            }
        }
        return res
