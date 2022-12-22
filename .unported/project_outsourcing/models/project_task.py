# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    """Propagate the project to outsourcing PO when changed on a task.

    When changing the project on a task, the project is propagated to the PO.

    If any PO is already confirmed, the change can not be done.
    This prevents the case of an invoice accounted with the wrong analytic account.
    """

    _inherit = "project.task"

    outsourcing_po_ids = fields.One2many(
        "purchase.order",
        "task_id",
        "Outsourcing Purchase Orders",
        groups="purchase.group_purchase_user",
    )

    outsourcing_line_ids = fields.Many2many(
        "purchase.order.line",
        compute="_compute_outsourcing_line_ids",
        string="Outsourcing Purchase Lines",
        groups="purchase.group_purchase_user",
    )

    outsourcing_po_count = fields.Integer(
        compute="_compute_outsourcing_po_count", groups="purchase.group_purchase_user"
    )

    def _compute_outsourcing_po_count(self):
        for task in self:
            task.outsourcing_po_count = self.env["purchase.order"].search(
                [("task_id", "=", task.id), ("state", "!=", "cancel")], count=True
            )

    def _compute_outsourcing_line_ids(self):
        for task in self:
            task.outsourcing_line_ids = task.mapped("outsourcing_po_ids.order_line")

    def _check_no_confirmed_outsourcing_to_update(self):
        confirmed_orders = self.outsourcing_po_ids.filtered(
            lambda o: o.state in ("purchase", "done")
        )
        orders_to_update = confirmed_orders.filtered(
            lambda o: o.project_id != self.project_id
        )
        if orders_to_update:
            raise ValidationError(
                _(
                    "The project can not be changed on the task {task}. "
                    "The task is linked to the following confirmed outsourcing "
                    "purchase orders: {orders}"
                ).format(
                    task=self.display_name,
                    orders=", ".join(orders_to_update.mapped("display_name")),
                )
            )

    def _propagate_project_to_outsourcing_orders(self):
        orders_to_update = self.outsourcing_po_ids.filtered(
            lambda o: o.project_id != self.project_id
        )
        orders_to_update.write({"project_id": self.project_id.id})
        orders_to_update.order_line.write(
            {"account_analytic_id": self.project_id.analytic_account_id.id}
        )

    @api.multi
    def write(self, vals):
        super().write(vals)
        if "project_id" in vals:
            for task in self:
                task.sudo()._check_no_confirmed_outsourcing_to_update()
                task.sudo()._propagate_project_to_outsourcing_orders()
        return True
