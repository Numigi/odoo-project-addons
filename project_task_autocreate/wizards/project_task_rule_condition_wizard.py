# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class ProjectTaskRuleConditionWizard(models.TransientModel):
    """Task Creation Rule Condition Wizard"""
    _name = 'project.task.rule.condition.wizard'
    _description = __doc__

    _typemap = {
        # odoo field type -> (operator_type, value_type)
        'boolean': ('bool', False),
        'selection': ('selection', 'selection'),
        'integer': ('ord', 'integer'),
        'float': ('ord', 'float'),
        'monetary': ('ord', 'float'),
        'date': ('ord', 'date'),
        'datetime': ('ord', 'datetime'),
        'char': ('str', 'str'),
        'text': ('str', 'str'),
        'html': ('str', 'str'),
        'many2one': ('rel', 'rel_or_str'),
        'many2many': ('rel', 'rel_or_str'),
        'one2many': ('rel', 'rel_or_str'),
    }

    operator_type = fields.Char(
        string='Operator Type',
        compute='_compute_operator_type',
    )
    operator = fields.Char(
        string='Operator',
        compute='_compute_operator',
    )
    value_type = fields.Char(
        string='Value Type',
        compute='_compute_value_type',
    )

    # Type-dependent Operators Fields
    operator_bool = fields.Selection(
        string='Operator',
        selection=[
            ('=', 'is true'),
            ('!=', 'is false'),
        ],
    )
    operator_str = fields.Selection(
        string='Operator',
        selection=[
            ('ilike', 'contains'),
            ('not ilike', 'doesn\'t contain'),
            ('=', 'is equal to'),
            ('!=', 'is not equal to'),
            ('set', 'is set'),
            ('!set', 'is not set'),
        ],
    )
    operator_ord = fields.Selection(
        string='Operator',
        selection=[
            ('=', 'is equal to'),
            ('!=', 'is not equal to'),
            ('<', 'less than'),
            ('<=', 'less than or equal'),
            ('>', 'greater than'),
            ('>=', 'greater than or equal'),
            ('set', 'is set'),
            ('!set', 'is not set'),

        ],
    )
    operator_selection = fields.Selection(
        string='Operator',
        selection=[
            ('=', 'is'),
            ('!=', 'is not'),
            ('set', 'is set'),
            ('!set', 'is not set'),
        ]
    )
    operator_rel = fields.Selection(
        string='Operator',
        selection=[
            ('=', 'is'),
            ('!=', 'is not'),
            ('ilike', 'contains'),
            ('not ilike', 'doesn\'t contain'),
            ('set', 'is set'),
            ('!set', 'is not set'),
        ],
    )

    # Type-dependent Value Fields
    value_integer = fields.Integer(
        string='Value',
    )
    value_float = fields.Float(
        string='Value',
    )
    value_selection = fields.Selection(
        string='Value',
        selection='_selection_value_selection',
    )
    value_str = fields.Char(
        string='Value',
    )
    value_date = fields.Date(
        string='Value',
    )
    value_datetime = fields.Datetime(
        string='Value',
    )
    value_rel = fields.Reference(
        string='Value',
        selection='_selection_value_rel',
    )

    rule_id = fields.Many2one(
        string='Task Creation Rule',
        comodel_name='project.task.rule',
    )
    model_id = fields.Many2one(
        comodel_name='ir.model',
        related='rule_id.model_id',
        readonly=True,
    )
    model = fields.Char(
        related='model_id.model',
        readonly=True,
    )
    field_id = fields.Many2one(
        string='Field',
        comodel_name='ir.model.fields',
        required=True,
        domain=[('ttype', 'in', _typemap.keys())],
    )

    @api.depends('field_id')
    def _compute_operator_type(self):
        for rec in self:
            if rec.field_id:
                rec.operator_type = self._typemap[rec.field_id.ttype][0]
            else:
                rec.operator_type = False

    @api.depends('operator_type', 'operator_bool', 'operator_ord',
                 'operator_str', 'operator_selection', 'operator_rel')
    def _compute_operator(self):
        for rec in self:
            rec.operator = getattr(rec, 'operator_' + rec.operator_type)

    @api.depends('field_id', 'operator', 'operator_type')
    def _compute_value_type(self):
        for rec in self:
            if rec.field_id and rec.operator not in ('set', '!set'):
                value_type = self._typemap[rec.field_id.ttype][1]
                if value_type == 'rel_or_str':
                    if rec.operator in ('=', '!='):
                        rec.value_type = 'rel'
                    else:
                        rec.value_type = 'str'
                else:
                    rec.value_type = value_type
            else:
                rec.value_type = False

    @api.multi
    def _selection_value_selection(self):
        if 'selection_field_id' in self.env.context:
            field = self.env['ir.model.fields'].browse(
                self.env.context['selection_field_id']
            )
            if field.ttype == 'selection':
                model = self.env[field.model]
                return model._fields[field.name].selection
        return []

    @api.multi
    def _selection_value_rel(self):
        if 'selection_field_id' in self.env.context:
            field = self.env['ir.model.fields'].browse(
                self.env.context['selection_field_id']
            )
            if field.relation:
                model = self.env[field.relation]
                return [(model._name, _(model._description) or model._name)]
        return []

    @api.model
    def action_open_wizard(self):
        wizard_view_id = self.env.ref(
            'project_task_autocreate.'
            'view_project_task_rule_condition_wizard_form'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choose Condition Field'),
            'res_model': 'project.task.rule.condition.wizard',
            'view_mode': 'form',
            'views': [(wizard_view_id, 'form')],
            'target': 'new',
        }

    @api.multi
    def action_open_wizard_2(self):
        self.ensure_one()
        wizard_view_id = self.env.ref(
            'project_task_autocreate.'
            'view_project_task_rule_condition_wizard_form_2'
        ).id
        context = dict(self.env.context)
        context.update({'selection_field_id': self.field_id.id})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choose Field Value'),
            'res_model': 'project.task.rule.condition.wizard',
            'view_mode': 'form',
            'views': [(wizard_view_id, 'form')],
            'target': 'new',
            'res_id': self.id,
            'context': context,
        }

    @api.multi
    def submit(self):
        self.ensure_one()
        res_id = self.env.context['active_id']
        field, op, value = self._get_domain_part()
        self.env['project.task.rule.condition'].create({
            'rule_id': res_id,
            'field': field,
            'operator': op,
            'value': repr(value),
            'operator_name': self._get_operator_name(),
            'value_name': self._get_value_name(),
        })

    @api.multi
    def _get_domain_part(self):
        self.ensure_one()
        name = self.field_id.name
        operator = self.operator
        if operator == 'set':
            operator = '!='
            value = False
        elif operator == '!set':
            operator = '='
            value = False
        elif self.operator_type == 'rel' and operator in ('=', '!='):
            value = self.value_rel.id
        elif self.operator_type == 'bool':
            value = True
        else:
            value = getattr(self, 'value_' + self.value_type)
        return (name, operator, value)

    @api.multi
    def _get_operator_name(self):
        self.ensure_one()
        field_name = 'operator_' + self.operator_type
        selection = self._fields[field_name].selection
        return next(t[1] for t in selection if t[0] == self.operator)

    @api.multi
    def _get_value_name(self):
        if self.operator in ('set', '!set') or self.operator_type == 'bool':
            return False
        elif self.operator_type == 'rel' and self.operator in ('=', '!='):
            return self.value_rel.display_name
        else:
            value = getattr(self, 'value_' + self.value_type)
            return repr(value)
