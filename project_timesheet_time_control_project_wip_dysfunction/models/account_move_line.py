# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_wip_supply_cost.models.account_move_line \
    import AccountMoveLine


def create_analytic_lines(self):
    if self._context.get('default_project_id') or \
            self._context.get('default_task_id'):
        self = self.with_context(default_project_id=False,
                                 default_task_id=False)
    result = super(AccountMoveLine, self).create_analytic_lines()
    shop_supply_lines = self.filtered(lambda l: l.is_shop_supply)
    shop_supply_lines.mapped('analytic_line_ids').write(
        {'is_shop_supply': True})

    return result


AccountMoveLine.create_analytic_lines = create_analytic_lines
