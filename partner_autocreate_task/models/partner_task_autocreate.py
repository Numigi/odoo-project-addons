# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


_intervalTypes = {
    'work_days': lambda interval: relativedelta(days=interval),
    'days': lambda interval: relativedelta(days=interval),
    'hours': lambda interval: relativedelta(hours=interval),
    'weeks': lambda interval: relativedelta(days=7*interval),
    'months': lambda interval: relativedelta(months=interval),
    'years': lambda interval: relativedelta(years=interval),
}


class PartnerTaskAutoCreate(models.Model):
    """Partner Task Auto Create"""

    _name = 'partner.task.autocreate'
    _description = __doc__
    _rec_name = 'task_id'

    @api.depends('last_created', 'interval_number', 'interval_type')
    def _compute_nextcall(self):
        """
        Compute the nextcall value.
        """
        for rec in self:
            next_call = fields.Datetime.now()
            if rec.last_created:
                last = fields.Datetime.from_string(rec.last_created)
                next_call = last + (
                    _intervalTypes[rec.interval_type](rec.interval_number)
                )
            rec.update({
                'nextcall': next_call
            })

    task_id = fields.Many2one(
        string='Task Template',
        comodel_name='project.task.template',
    )
    interval_number = fields.Integer(
        default=1,
        string='Interval',
        help="Repeat every x."
    )
    interval_type = fields.Selection(
        [('hours', 'Hours'),
         ('work_days', 'Work Days'),
         ('days', 'Days'),
         ('weeks', 'Weeks'),
         ('months', 'Months'),
         ('years', 'Years'),
         ],
        string='Interval Unit',
        default='months'
    )
    last_created = fields.Datetime(
        string='Last Created',
        readonly=True,
        help="Last planned execution date for this job.",
    )
    nextcall = fields.Datetime(
        string='Next Execution Date',
        store=True, readonly=True, compute='_compute_nextcall',
        help="Next planned execution date for this job."
    )
    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
    )

    @api.model
    def create_tasks(self):
        lines = self.search(
            [('nextcall', '<=', fields.Datetime.now())])
        for line in lines:
            line.last_created = fields.Datetime.now()
            task_obj = self.env['project.task']
            task_obj |= task_obj.create(
                line.task_id.get_task_vals()
            )
