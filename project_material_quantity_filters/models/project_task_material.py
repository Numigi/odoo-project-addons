# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.tools import float_compare


class TaskMaterialLine(models.Model):

    _inherit = 'project.task.material'

    prepared_versus_initial = fields.Boolean(
        compute="_compute_prepared_versus_initial",
        store=True,
        compute_sudo=True,
    )

    consumed_versus_prepared = fields.Boolean(
        compute="_compute_consumed_versus_prepared",
        store=True,
        compute_sudo=True,
    )

    consumed_versus_initial = fields.Boolean(
        compute="_compute_consumed_versus_initial",
        store=True,
        compute_sudo=True,
    )

    @api.depends('prepared_qty', 'initial_qty')
    def _compute_prepared_versus_initial(self):
        for line in self:
            line.prepared_versus_initial = float_compare(
                line.prepared_qty, line.initial_qty, 2
            ) != 0

    @api.depends('consumed_qty', 'prepared_qty')
    def _compute_consumed_versus_prepared(self):
        for line in self:
            line.consumed_versus_prepared = float_compare(
                line.consumed_qty, line.prepared_qty, 2
            ) != 0

    @api.depends('consumed_qty', 'initial_qty')
    def _compute_consumed_versus_initial(self):
        for line in self:
            line.consumed_versus_initial = float_compare(
                line.consumed_qty, line.initial_qty, 2
            ) != 0
