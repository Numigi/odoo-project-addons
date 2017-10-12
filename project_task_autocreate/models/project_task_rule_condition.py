# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval


class ProjectTaskRuleCondition(models.Model):
    """Task Creation Rule Condition"""
    _name = 'project.task.rule.condition'
    _description = __doc__

    rule_id = fields.Many2one(
        string='Task Creation Rule',
        comodel_name='project.task.rule',
        ondelete='cascade',
        required=True,
    )
    field = fields.Char(
        string='Field',
        required=True,
    )
    operator = fields.Char(
        string='Operator',
        required=True,
    )
    value = fields.Char(
        string='Value',
        required=True,
    )
    operator_name = fields.Char(
        string='Operator Description',
        required=True,
    )
    value_name = fields.Char(
        string='Value Description',
    )

    @api.model
    def create(self, vals):
        res = super(ProjectTaskRuleCondition, self).create(vals)
        res.rule_id._update_rules()
        return res

    @api.multi
    def write(self, vals):
        res = super(ProjectTaskRuleCondition, self).write(vals)
        self.mapped('rule_id')._update_rules()
        return res

    @api.multi
    def unlink(self):
        rules = self.mapped('rule_id')
        res = super(ProjectTaskRuleCondition, self).unlink()
        rules._update_rules()
        return res

    def name_get(self):
        names = []
        for cond in self:
            field = self.env['ir.model.fields'].search([
                ('name', '=', cond.field),
                ('model', '=', cond.rule_id.model),
            ], limit=1)
            field_name = _(field.field_description)
            name = field_name + ' ' + _(cond.operator_name)
            if cond.value_name:
                name = name + ' ' + cond.value_name
            names.append((cond.id, name))
        return names

    @api.multi
    def get_domain(self, any=False):
        """
        Return domain for zero or more conditions.
        """
        domain = [rec._get_domain_part() for rec in self]
        if any:
            # Domain should look like:
            # [ '|', (...),
            #        '|', (...),
            #             '|', (...), (...)]
            # So we add an OR operator in front of every domain part
            # starting at len(domain)-2
            if len(domain) > 1:
                for i in range(len(domain)-2, -1, -1):
                    domain.insert(i, '|')
        return domain

    @api.multi
    def _get_domain_part(self):
        self.ensure_one()
        return (self.field, self.operator, safe_eval(self.value))
