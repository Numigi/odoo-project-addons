# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectType(models.Model):
    """Add the salary account to project types."""

    _inherit = 'project.type'

    shop_supply_journal_id = fields.Many2one(
        'account.journal',
        'Shop Supply Journal',
        company_dependent=True,
        help='Journal used for reporting shop supply entries.',
    )

    shop_supply_account_id = fields.Many2one(
        'account.account',
        'Shop Supply Account',
        company_dependent=True,
        help='Account used as counter-part (usually the credit part) in shop supply entries.',
    )

    shop_supply_rate = fields.Float(
        'Shop Supply Rate',
        default=0,
        company_dependent=True,
        help='The rate to apply for shop supply entries.',
    )

    @api.constrains('shop_supply_account_id', 'shop_supply_journal_id', 'wip_account_id')
    def _check_required_fields_for_shop_supply(self):
        project_types_with_shop_supply = self.filtered(lambda t: t.shop_supply_account_id)
        for project_type in project_types_with_shop_supply:
            if not project_type.wip_account_id:
                raise ValidationError(_(
                    'If the shop supply account is filled for a project type, '
                    'the work in progress account must be filled as well.'
                ))

            if not project_type.shop_supply_journal_id:
                raise ValidationError(_(
                    'If the shop supply account is filled for a project type, '
                    'the salary journal must be filled as well.'
                ))
