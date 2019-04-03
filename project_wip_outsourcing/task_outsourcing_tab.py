# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    """Add the fields contained in the outsourcing tab on the task."""

    _inherit = 'project.task'

    outsourcing_po_ids = fields.One2many(
        'purchase.order',
        'task_id',
        'Outsourcing Purchase Orders',
    )

    outsourcing_line_ids = fields.One2many(
        related='outsourcing_po_ids.order_line',
        string='Outsourcing Purchase Lines',
    )


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.onchange('task_id')
    def _onchange_task_set_project(self):
        """Set the project if different from the task.

        If the PO is created from a task, the task_id will be propagated
        with active_id context variable.

        In this case, the task is filled before the project.
        """
        if self.is_outsourcing and self.task_id.project_id != self.project_id:
            self.project_id = self.task_id.project_id
