# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.osv.expression import AND
from odoo.tools.float_utils import float_round
from odoo.addons.project_cost_report.report import CostReportCategory


class ProjectCostReportWithShopSupply(models.TransientModel):

    _inherit = 'project.cost.report'

    def _get_empty_shop_supply_category_label(self):
        """Get the label to display on the unique shop supply category.

        :rtype: str
        """
        return _('Shop Supply')

    def _get_shop_supply_analytic_line_domain(self, project):
        """Get the search domain to query shop supply analytic lines.

        :param project: the project.project record
        :rtype: list
        """
        return [
            ('account_id', '=', project.analytic_account_id.id),
            ('is_shop_supply', '=', True),
        ]

    def _get_shop_supply_categories(self, project, report_context):
        """Get the SHOP SUPPLY sections.

        Outsourcing has only one category (False).

        :param project: the project.project record
        :param report_context: the rendering context
        :rtype: dict
        """
        domain = self._get_shop_supply_analytic_line_domain(project)
        unfolded_categories = report_context.get('unfolded_categories') or {}
        unfolded_shop_supply_categories = unfolded_categories.get('shop_supply') or []
        result = []
        lines = self.env['account.analytic.line'].search(domain)
        if lines:
            empty_category = CostReportCategory(
                id_=False,
                name=self._get_empty_shop_supply_category_label(),
                lines=lines,
                folded=False not in unfolded_shop_supply_categories
            )
            result.append(empty_category)
        return result

    def _get_shop_supply_total(self, project):
        """Get the total amount for the OUTSOURCING section.

        :param project: the project.project record
        :rtype: float
        """
        domain = self._get_shop_supply_analytic_line_domain(project)
        result = self.env['account.analytic.line'].read_group(
            domain=domain, fields=['account_id', 'amount'], groupby='account_id')
        amount = result[0]['amount'] if result else 0
        return float_round(-amount, 2)

    def _get_rendering_variables(self, project, report_context):
        """Add the variables related to the OUTSOURCING section."""
        res = super()._get_rendering_variables(project, report_context)
        shop_supply_total = self._get_shop_supply_total(project)
        res.update({
            'shop_supply_categories': self._get_shop_supply_categories(project, report_context),
            'shop_supply_total': shop_supply_total,
            'total_cost': float_round(res['total_cost'] + shop_supply_total, 2)
        })
        return res

    @api.model
    def get_foldable_categories(self, project_id):
        """Add shop supply categories to foldable categories.

        The SHOP SUPPLY section has only one category (the empty category).
        """
        res = super().get_foldable_categories(project_id)
        res['shop_supply'] = [False]
        return res

    def _get_product_analytic_line_domain(self, project):
        """Isolate the shop supply from product domain."""
        domain = super()._get_product_analytic_line_domain(project)
        return AND((domain, [('is_shop_supply', '=', False)]))

    def _get_time_analytic_line_domain(self, project):
        """Isolate the shop supply from time domain."""
        domain = super()._get_time_analytic_line_domain(project)
        return AND((domain, [('is_shop_supply', '=', False)]))

    def _get_outsourcing_analytic_line_domain(self, project):
        """Isolate the shop supply from outsourcing domain."""
        domain = super()._get_outsourcing_analytic_line_domain(project)
        return AND((domain, [('is_shop_supply', '=', False)]))
