# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import ValidationError


class PurchaseOrderWithOutSourcing(models.Model):

    _inherit = 'purchase.order'

    def _check_outsourcing_project_type_has_wip_account(self):
        project_type = self.project_id.project_type_id
        if not project_type.wip_account_id:
            raise ValidationError(_(
                'The project type {} has no WIP account. '
                'The WIP account must be set on the project type before confirming the '
                'outsourcing purchase order.'
            ).format(project_type.display_name))

    def button_confirm(self):
        outsourcing_orders = self.filtered(lambda o: o.is_outsourcing)
        for order in outsourcing_orders:
            order.sudo()._check_outsourcing_project_type_has_wip_account()
        return super().button_confirm()
