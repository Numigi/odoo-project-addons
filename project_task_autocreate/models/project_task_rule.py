# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class ProjectTaskRule(models.Model):
    """Task Creation Rule"""
    _name = 'project.task.rule'
    _description = __doc__

    _sql_constraints = [
        ('uniq_name', 'unique(name)', _('Task rule names must be unique.')),
    ]

    active = fields.Boolean(
        string='Active',
        default=True,
    )
    name = fields.Char(
        string='Description',
        required=True,
        translate=True,
    )
    model_id = fields.Many2one(
        string='Model',
        comodel_name='ir.model',
        required=True,
        help="The model to which the rule applies."
    )
    model = fields.Char(
        related='model_id.model',
        readonly=True,
    )
    rule_type = fields.Selection(
        string='Rule Type',
        selection=[
            ('all', 'All conditions must be met (AND)'),
            ('any', 'At least one condition must be met (OR)')
        ],
        default='all',
        required=True,
    )
    template_ids = fields.Many2many(
        string='Task Templates',
        comodel_name='project.task.template',
        relation='project_task_autocreate_rules_rel',
    )
    condition_ids = fields.One2many(
        string='Conditions',
        comodel_name='project.task.rule.condition',
        inverse_name='rule_id',
    )
    use_domain = fields.Boolean(
        string='Use Custom Domain?',
        default=False,
    )
    domain = fields.Char(
        string='Domain',
        default='[]',
    )

    on_create = fields.Boolean(
        string="On Creation?",
        help="If checked, the rule will be applied when a record of the "
             "selected model is created.",
    )
    on_create_rule_id = fields.Many2one(
        string='On Create Rule',
        comodel_name='base.action.rule',
        ondelete='set null',
        readonly=True,
        groups='base.group_no_one',
    )
    on_write = fields.Boolean(
        string='On Update?',
        help="If checked, the rule will be applied when a record of the "
             "selected model is updated.",
    )
    on_write_rule_id = fields.Many2one(
        string='On Write Rule',
        comodel_name='base.action.rule',
        ondelete='set null',
        readonly=True,
        groups='base.group_no_one',
    )
    on_unlink = fields.Boolean(
        string="On Deletion?",
        help="If checked, the rule will be applied when a record of the "
             "selected model is deleted.",
    )
    on_unlink_rule_id = fields.Many2one(
        string='On Delete Rule',
        comodel_name='base.action.rule',
        ondelete='set null',
        readonly=True,
        groups='base.group_no_one',

    )
    on_state = fields.Boolean(
        string="On Status Change?",
        help="If checked, the rule will be applied when a record of the "
             "selected model changes status.",
    )
    state = fields.Char(
        string='Trigger Status',
        help='The rule will be applied when a record enters this status.'
    )
    state_from = fields.Char(
        string='Trigger Origin Status',
        help='The rule will be applied when a record leaves this status.'
    )
    on_state_rule_id = fields.Many2one(
        string='On State Rule',
        comodel_name='base.action.rule',
        ondelete='set null',
        readonly=True,
        groups='base.group_no_one',
    )

    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.condition_ids = False
        self.template_ids = False

    @api.constrains('domain')
    def _check_domain(self):
        try:
            domain = safe_eval(self.domain)
            self.env[self.model].search(domain)
        except Exception as e:
            raise ValidationError(_(
                'Error in domain expression: %s' % e.message
            ))

    @api.constrains('on_state', 'state', 'state_from')
    def _check_state(self):
        for rule in self.filtered(lambda r: r.on_state):
            model = self.env[rule.model]
            fields = model._fields
            if 'state' not in fields:
                raise ValidationError(_(
                    "This model cannot have an On Status rule since it does "
                    "not have a status field."
                ))
            if not (rule.state or rule.state_from):
                raise ValidationError(_(
                    "At least one of the 'From' or 'To' trigger status must "
                    "be set."
                ))
            state_field = self.env[rule.model]._fields['state']
            if state_field.type == 'selection':
                valid_states = [s[0] for s in state_field.selection]
                states = [rule.state, rule.state_from]
                for state in states:
                    if state not in valid_states:
                        raise ValidationError(_(
                            "%(state)s is not a valid status on %(model)s. "
                            "Valid statuses are:\n%(list_valid)s"
                        ) % {
                            'state': rule.state,
                            'model': rule.model,
                            'list_valid': '\n'.join(
                                ['%s (%s)' % s for s in state_field.selection])
                        })

    @api.model
    def create(self, vals):
        res = super(ProjectTaskRule, self).create(vals)
        res._update_rules()
        res._update_rules_active()
        return res

    @api.multi
    def write(self, vals):
        res = super(ProjectTaskRule, self).write(vals)
        dont_require_rules_update = {
            'active',
            # Necessary to prevent recursion
            'on_create_rule_id',
            'on_unlink_rule_id',
            'on_state_rule_id',
            'on_write_rule_id',
            # ------------------------------
        }
        if set(vals.keys()) - dont_require_rules_update:
            self._update_rules()
        if 'active' in vals.keys():
            self._update_rules_active()
        return res

    @api.multi
    def unlink(self):
        self._unlink_rules()
        return super(ProjectTaskRule, self).unlink()

    @api.multi
    def action_open_condition_wizard(self):
        self.ensure_one()
        wizard = self.env['project.task.rule.condition.wizard']
        return wizard.action_open_wizard()

    @api.multi
    def _get_domain(self):
        """
        Get filter domain from task rule conditions or custom domain.
        """
        self.ensure_one()
        if self.use_domain:
            return safe_eval(self.domain)
        else:
            return self.condition_ids.get_domain(any=(self.rule_type == 'any'))

    @api.multi
    def _get_on_state_domain(self):
        """
        Get filter domain for on state rule.
        """
        self.ensure_one()
        if self.state:
            domain = [('state', '=', self.state)]
        else:
            domain = [('state', '!=', self.state_from)]
        return domain + self._get_domain()

    @api.multi
    def _get_on_state_pre_domain(self):
        """
        Get pre-filter domain for on state rule.
        """
        self.ensure_one()
        if self.state_from:
            domain = [('state', '=', self.state_from)]
        else:
            domain = [('state', '!=', self.state)]
        return domain

    @api.multi
    def _create_rule(self, kind):
        self.ensure_one()
        rule_name = self.name + ' (%s)' % kind

        # Create filters
        filter_obj = self.env['ir.filters']
        if kind == 'on_state':
            filter_id = filter_obj.create({
                'name': 'Filter for rule "%s"' % rule_name,
                'model_id': self.model,  # Selection field, not Many2one
                'domain': repr(self._get_on_state_domain()),
            }).id
            pre_filter_id = filter_obj.create({
                'name': 'Pre-filter for rule "%s"' % rule_name,
                'model_id': self.model,  # Selection field, not Many2one
                'domain': repr(self._get_on_state_pre_domain()),
            }).id
        else:
            filter_id = filter_obj.create({
                'name': 'Filter for rule "%s"' % rule_name,
                'model_id': self.model,  # Selection field, not Many2one
                'domain': repr(self._get_domain()),
            }).id
            pre_filter_id = False

        # Create actions
        trigger_field = self.env['ir.model.fields'].search([
            ('model', '=', 'project.task.template'),
            ('name', '=', 'trigger_record_id'),
        ], limit=1)
        template_model = self.env['ir.model'].search([
            ('model', '=', 'project.task.template')
        ], limit=1)
        # The server actions write to the 'trigger_record_id' field of
        # the task templates. It is a special field which triggers
        # the creation of a task from the template.
        actions = self.env['ir.actions.server']
        lines_obj = self.env['ir.server.object.lines']
        for template in self.template_ids:
            action = actions.create({
                'type': 'ir.actions.server',
                'name': ('Create task from template "%(tmpl)s" (%(rule)s)' % {
                    'tmpl': template.name,
                    'rule': rule_name,
                }),
                'model_id': self.model_id.id,
                'state': 'object_write',
                'condition': 'True',
                'use_write': 'other',
                'ref_object': 'project.task.template,' + str(template.id),
                'crud_model_id': template_model.id,
            })
            lines_obj.create({
                'server_id': action.id,
                'col1': trigger_field.id,
                'type': 'equation',
                'value': 'record.id',
            })
            actions |= action

        # Create action rule
        return self.env['base.action.rule'].create({
            'name': 'Rule for "%s"' % rule_name,
            'model_id': self.model_id.id,
            'kind': 'on_write' if kind == 'on_state' else kind,
            'filter_id': filter_id,
            'filter_pre_id': pre_filter_id,
            'server_action_ids': [(4, rec.id) for rec in actions],
        })

    @api.multi
    def _update_rules(self):
        # This is not the most efficient way but rules are rarely changed
        # and it is much simpler than trying to manage state changes
        self = self.sudo()
        self._unlink_rules()
        for rule in self:
            if rule.on_create:
                rule.on_create_rule_id = rule._create_rule('on_create')
            if rule.on_write:
                rule.on_write_rule_id = rule._create_rule('on_write')
            if rule.on_unlink:
                rule.on_unlink_rule_id = rule._create_rule('on_unlink')
            if rule.on_state:
                rule.on_state_rule_id = rule._create_rule('on_state')

    @api.multi
    def _update_rules_active(self):
        self = self.sudo()
        for task_rule in self:
            task_rule = task_rule
            rules = (
                task_rule.mapped('on_state_rule_id') |
                task_rule.mapped('on_create_rule_id') |
                task_rule.mapped('on_write_rule_id') |
                task_rule.mapped('on_unlink_rule_id')
            )
            rules.write({
                'active': task_rule.active,
            })

    @api.multi
    def _unlink_rules(self):
        # Delete actions, filters and rules
        self = self.sudo()
        rules = (
            self.mapped('on_state_rule_id') |
            self.mapped('on_create_rule_id') |
            self.mapped('on_write_rule_id') |
            self.mapped('on_unlink_rule_id')
        )
        if rules:
            filters = (
                rules.mapped('filter_id') |
                rules.mapped('filter_pre_id')
            )
            actions = rules.mapped('server_action_ids')
            rules.unlink()
            actions.unlink()
            filters.unlink()
