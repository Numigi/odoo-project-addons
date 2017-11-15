# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import datetime
import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProjectTaskTemplate(models.Model):
    """Task Template"""
    _name = 'project.task.template'
    _inherit = 'project.task'
    _description = __doc__

    name = fields.Char(
        string='Task Template',
        translate=True,
        help=(
            "You can use object references in the task title, for example:\n"
            "SO {object.name} has just been confirmed."
        )
    )
    description = fields.Html(
        translate=True,
        help=(
            "You can use object references in the task description\n"
            "for example:\n"
            "Sale order {object.name} for partner {object.partner_id.name}\n"
            "has just been confirmed."
        )
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        default=False,
        required=False,
    )
    model_id = fields.Many2one(
        string='Model',
        comodel_name='ir.model',
    )
    model = fields.Char(
        related='model_id.model',
        readonly=True,
    )
    rule_ids = fields.Many2many(
        string='Task Creation Rules',
        comodel_name='project.task.rule',
        relation='project_task_autocreate_rules_rel',
    )

    # 'Relative' fields allow using a field on the object from which the
    # the task is created instead of a fixed value,
    # for example object.partner_id for the relative partner_id.
    use_relative_partner_id = fields.Boolean(
        string='Use Relative Customer?',
        default=False,
    )
    relative_partner_id = fields.Char(
        string='Relative Customer',
    )
    use_relative_project_id = fields.Boolean(
        string='Use Relative Project?',
        default=False,
    )
    relative_project_id = fields.Char(
        string='Relative Project',
    )
    use_relative_user_id = fields.Boolean(
        string='Use Relative Assigned To?',
        default=False,
    )
    relative_user_id = fields.Char(
        string='Relative Assigned To',
    )
    use_relative_deadline = fields.Boolean(
        string='Use Relative Deadline?',
        default=False,
    )
    relative_deadline = fields.Char(
        string='Relative Deadline',
        help=(
            'Reference to a date field on the related object, like '
            'object.delivery_date.\nUse "today" to '
            'set a deadline relative to the task creation day.'
        ),
    )
    relative_deadline_delta = fields.Integer(
        string='Relative Deadline Delta',
    )
    relative_deadline_units = fields.Selection(
        selection=[
            ('days', 'days'),
            ('weeks', 'weeks'),
        ],
    )
    relative_deadline_op = fields.Selection(
        selection=[
            ('before', 'before'),
            ('after', 'after'),
        ],
        default='after',
    )
    trigger_record_id = fields.Integer(
        string='Trigger Task Creation For Record',
        help='Writing to this field triggers the creation of a task linked to '
             'the record with the given ID. For system use only.',
        groups='base.group_no_one',
        readonly=True,
    )

    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.rule_ids = False

    @api.constrains(
        'model_id',
        'relative_project_id',
        'use_relative_project_id',
    )
    def _check_relative_project_id(self):
        for rec in self:
            if not rec.use_relative_project_id:
                continue
            relstr = rec.relative_project_id
            rec._check_relative_field_rel(relstr, 'Project', 'project.project')

    @api.constrains(
        'model_id',
        'relative_partner_id',
        'use_relative_partner_id',
    )
    def _check_relative_partner_id(self):
        for rec in self:
            if not rec.use_relative_partner_id:
                continue
            relstr = rec.relative_partner_id
            rec._check_relative_field_rel(relstr, 'Partner', 'res.partner')

    @api.constrains(
        'model_id',
        'relative_user_id',
        'use_relative_user_id',
    )
    def _check_relative_user_id(self):
        for rec in self:
            if not rec.use_relative_user_id:
                continue
            relstr = rec.relative_user_id
            rec._check_relative_field_rel(relstr, 'Assigned To', 'res.users')

    @api.constrains(
        'model_id', 'use_relative_deadline',
        'relative_deadline', 'relative_deadline_op',
        'relative_deadline_units', 'relative_deadline_delta',
    )
    def _check_relative_deadline(self):
        for rec in self:
            if not rec.use_relative_deadline:
                continue
            if not all([rec.relative_deadline_op,
                        rec.relative_deadline_units,
                        rec.relative_deadline_delta]):
                raise ValidationError(_(
                    "All fields of the relative deadline must be set."
                ))
            relstr = rec.relative_deadline
            if relstr != 'today':
                rec._check_relative_field(relstr, 'Deadline', 'date')

    @api.constrains('model_id', 'rule_ids')
    def _check_model_id(self):
        for rec in self:
            if rec.rule_ids and not rec.model_id:
                raise ValidationError(_(
                    "Templates with rules must have a model set."
                ))

    @api.multi
    def write(self, vals):
        # Update records before creating tasks
        res = super(ProjectTaskTemplate, self).write(vals)
        if 'trigger_record_id' in vals:
            rec_id = vals['trigger_record_id']
            models = set(self.mapped('model'))
            if len(models) > 1:
                raise UserError(_(
                    "Task creation cannot be triggered for multiple templates "
                    "with different models at the same time."
                ))
            rec = self.env[models.pop()].browse(rec_id)
            self.create_tasks_from_records(rec)
        return res

    @api.multi
    @api.returns('project.task')
    def create_task(self):
        """
        Create a task from the template.
        """
        tasks = self.env['project.task']
        for template in self:
            tasks |= tasks.create(
                template.get_task_vals()
            )
        return tasks

    @api.multi
    @api.returns('project.task')
    def create_tasks_from_records(self, records):
        """
        Create a task from the template for each record in records.
        """
        tasks = self.env['project.task']
        for template in self:
            if records._name != template.model:
                raise UserError(_(
                    "The template '%(template)s' can only be used with "
                    "%(expected_model)s, not with %(model)s."
                ) % {
                    'template': template.name,
                    'expected_model': template.model,
                    'model': records._name,
                })
            for rec in records:
                tasks |= tasks.create(
                    template.get_task_vals(rec)
                )
        return tasks

    @api.multi
    def action_create_task(self):
        self.ensure_one()
        if self.model_id:
            raise UserError(_(
                'A task cannot be created from this template unless it is '
                'linked to a particular %(model)s.'
            ) % {
                'model': self.model_id.name,
            })
        task = self.create_task()
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.task',
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': task.id,
        }

    @api.multi
    def get_task_vals(self, record=None):
        self.ensure_one()
        """
        Return vals to copy from templates to created tasks.
        Extend or override this to change which fields are copied.

        record is the record attached to the template,
        of type template.model, if there is one.
        """
        description = self.description
        if description:
            description = description.format(object=record)
        vals = {
            'name': self.name.format(object=record),
            'description': description,
            'sequence': self.sequence,
            'priority': self.priority,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'date_deadline': self._get_deadline(record),
            'user_id': self._get_user_id(record).id,
            'partner_id': self._get_partner_id(record).id,
            'project_id': self._get_project_id(record).id,
        }
        if record:
            vals['origin_id'] = '%s,%d' % (record._name, record.id)
        return vals

    @api.model
    def _get_relative_value(self, relstr, record):
        fields = relstr.split('.')[1:]
        value = record
        while value and fields:
            value = getattr(value, fields.pop(0))
        return value or False

    @api.multi
    def _get_partner_id(self, record=None):
        self.ensure_one()
        if self.use_relative_partner_id and record:
            return self._get_relative_value(self.relative_partner_id, record)
        else:
            return self.partner_id

    @api.multi
    def _get_user_id(self, record=None):
        self.ensure_one()
        if self.use_relative_user_id and record:
            return self._get_relative_value(self.relative_user_id, record)
        else:
            return self.user_id

    @api.multi
    def _get_project_id(self, record=None):
        self.ensure_one()
        if self.use_relative_project_id and record:
            return self._get_relative_value(self.relative_project_id, record)
        else:
            return self.project_id

    @api.multi
    def _get_deadline(self, record=None):
        self.ensure_one()
        if self.use_relative_deadline:
            if self.relative_deadline == 'today':
                base = fields.Date.today()
            else:
                base = self._get_relative_value(self.relative_deadline, record)
            if base:
                base_dt = fields.Date.from_string(base)
                delta = datetime.timedelta(**{
                    self.relative_deadline_units: self.relative_deadline_delta
                })
                if self.relative_deadline_op == 'before':
                    dt = base_dt - delta
                else:
                    dt = base_dt + delta
                return fields.Date.to_string(dt)
            else:
                return ''
        else:
            return self.date_deadline

    @api.multi
    def _check_relative_field(self, relstr, name, ttype):
        re_relstr = re.compile(r'object(.[A-Za-z][A-Za-z0-9_]*)$')
        self.ensure_one()
        if not self.model_id:
            raise ValidationError(_(
                "Object references cannot be used on templates without a "
                "model set. Please choose a model or uncheck 'Use Relative "
                "%(field_name)s?'."
            ) % {'field_name': name})
        if not relstr:
            raise ValidationError(_(
                "The field %(field)s is required."
            ) % {'field': name})

        domain = [
            ('model', '=', self.model),
            ('ttype', '=', ttype)
        ]
        field_names = self.env['ir.model.fields'].search(domain).mapped('name')
        if not re_relstr.match(relstr):
            raise ValidationError(_(
                "The reference for field %(field_name)s has the wrong format. "
                "Expected a reference to a %(field_type)s field, like:"
                "\n%(examples)s"
            ) % {
                'field_name': name,
                'field_type': ttype,
                'examples': '\n'.join(['object.%s' % n for n in field_names])
            })

        field = relstr.split('.')[1]
        if field not in field_names:
            raise ValidationError(_(
                "Error on field %(field_name)s: %(field)s is not a "
                "%(field_type)s field on %(model)s. You may use one of the "
                "following fields for %(field_name)s: \n %(examples)s"
            ) % {
                'field': field,
                'field_name': name,
                'model': self.model,
                'field_type': ttype,
                'examples': '\n'.join(field_names),
            })

    @api.multi
    def _check_relative_field_rel(self, relstr, name, relation):
        re_relstr = re.compile(r'object(.[A-Za-z][A-Za-z0-9_]*)*$')
        self.ensure_one()
        if not self.model_id:
            raise ValidationError(_(
                "Object references cannot be used on templates without a "
                "model set. Please choose a model or uncheck 'Use Relative "
                "%(field_name)s?'."
            ) % {'field_name': name})

        domain = [
            ('model', '=', self.model),
            ('relation', '=', relation)
        ]
        if not relstr:
            raise ValidationError(_(
                "The field %(field)s is required."
            ) % {'field': name})

        field_names = self.env['ir.model.fields'].search(domain).mapped('name')
        if not re_relstr.match(relstr):
            raise ValidationError(_(
                "The reference for %(field_name)s has the wrong format.\n"
                "Expected a reference to a %(field_type)s field, like:"
                "\n%(examples)s"
            ) % {
                'field_name': name,
                'field_type': relation,
                'examples': '\n'.join(['object.%s' % n for n in field_names])
            })

        model = self.model
        fields = relstr.strip('{}').split('.')[1:]
        while fields and model:
            field_name = fields.pop(0)
            model_obj = self.env[model]
            if field_name not in model_obj._fields:
                raise ValidationError(_(
                    "%(field)s is not a valid field on model %(model)s."
                ) % {
                    'field': field_name,
                    'model': model,
                })
            model = model_obj._fields[field_name].comodel_name
        if model != relation:
            raise ValidationError(_(
                "%(relstr)s is not a field of type %(field_type)s.\n"
                "Expected a reference to a %(field_type)s field, like:"
                "\n%(examples)s"
            ) % {
                'relstr': relstr,
                'field_name': name,
                'field_type': relation,
                'examples': '\n'.join(
                    ['object.%s' % n for n in field_names])
              })
