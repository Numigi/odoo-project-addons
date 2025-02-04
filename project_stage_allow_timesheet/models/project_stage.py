# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectStage(models.Model):

    _inherit = 'project.stage'

    allow_timesheet = fields.Boolean(
        default=True,
    )


class ProjectTaskType(models.Model):

    _inherit = 'project.task.type'

    allow_timesheet = fields.Boolean(
        string="Allow timesheets",
        default=True,
    )
