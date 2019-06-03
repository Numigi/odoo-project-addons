# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.tools.float_utils import float_round
from odoo.exceptions import ValidationError


class CostReportCategory:

    def __init__(self, id_: int, name: str, lines: models.Model, folded: bool):
        """Initialize the report category.

        :param id: the ID of the related product.category record
        :param name: the name of the category
        :param lines: a recordset of Odoo account.analytic.line
        :param folded: whether the category is folded or not
        """
        self.id = id_
        self.name = name
        self.lines = lines
        self.folded = folded
        self.total = float_round(sum(l.amount for l in lines), 2)


class ProjectCostReport(models.TransientModel):

    _name = 'project.cost.report'

    def _get_product_analytic_line_domain(self, project):
        return [
            ('account_id', '=', project.analytic_account_id.id),
            ('product_id.type', 'in', ('product', 'consu')),
        ]

    def _get_product_categories(self, project, report_context):
        """Get the stockable/consumable product categories.

        :param project: the project.project record
        :param report_context: the rendering context
        :rtype: dict
        """
        domain = self._get_product_analytic_line_domain(project)
        lines = self.env['account.analytic.line'].search(domain)

        grouped_lines = {}
        for line in lines:
            category = line.product_id.categ_id
            if category not in grouped_lines:
                grouped_lines[category] = self.env['account.analytic.line']
            grouped_lines[category] |= line

        sorted_categories = sorted(grouped_lines.keys(), key=lambda c: c.name)
        unfolded_category_ids = report_context.get('unfolded_category_ids') or []
        return [
            CostReportCategory(
                id_=c.id,
                name=c.name,
                lines=grouped_lines.get(c),
                folded=c.id not in unfolded_category_ids
            ) for c in sorted_categories
        ]

    def _get_product_total(self, project):
        domain = self._get_product_analytic_line_domain(project)
        result = self.env['account.analytic.line'].read_group(
            domain=domain, fields=['account_id', 'amount'], groupby='account_id')
        return result[0]['amount'] if result else 0

    def _get_rendering_variables(self, project, report_context):
        """Get the variables used for rendering the qweb report.

        :param project: the project.project record
        :param report_context: the rendering context
        :rtype: dict
        """
        return {
            'product_categories': self._get_product_categories(project, report_context),
            'product_total': self._get_product_total(project),
        }

    def _get_html(self, report_context):
        project_id = report_context.get('active_id')

        if not project_id:
            raise ValidationError(_(
                'The cost report was triggered without a project ID in context.'
            ))

        project = self.env['project.project'].browse(project_id)
        rendering_variables = self._get_rendering_variables(project, report_context)
        return self.env.ref('project_cost_report.cost_report_html').render(rendering_variables)

    @api.model
    def get_html(self, report_context):
        """Get the report html given the report context.

        :param report_context: the report context.
        :ptype: report_context: dict
        :rtype: str
        """
        res = self.search([('create_uid', '=', self.env.uid)], order='id desc', limit=1)
        if not res:
            res = self.create({})
        return res._get_html(report_context)
