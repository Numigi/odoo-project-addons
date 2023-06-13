# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api
from odoo.addons.project_wip_supply_cost.models.account_analytic_line \
    import AnalyticLine


@api.multi
def write(self, vals):
    """When updating an analytic line, create / update / delete the wip entry.

    Whether the wip entry must be created / updated / deleted depends
    on which field is written to. This prevents an infinite loop.
    """
    super(AnalyticLine, self).write(vals)

    fields_to_check = self._get_shop_supply_move_dependent_fields()
    if not self.env.context.get('resuming_lines') and \
            fields_to_check.intersection(vals):
        for line in self:
            line.sudo()._create_update_or_reverse_shop_supply_move()

    return True


AnalyticLine.write = write


