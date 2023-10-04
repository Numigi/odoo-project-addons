# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import models, fields,api


class ProjectParentRequired(models.Model):
    _inherit = "project.project"
    @api.constrains("parent_id")
    def _check_cannot_change_parent_while_existing_timesheet(self):
        """ do nothing """
