# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _get_values_for_invisible_template_fields(self):
        vals = super()._get_values_for_invisible_template_fields()
        vals["date_planned"] = False
        return vals
