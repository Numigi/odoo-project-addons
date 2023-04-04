# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api, fields, _
from datetime import datetime


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    create_subcontractors_time_entries = fields.Boolean(
        "Create Subcontractors Time Entries",
        help="When activated, if the Subcontractor and the Product have "
             "the parameter ‘Subcontracting - Automate Time Entries’ active, "
             "when a task associated with a subcontracting Purchase Order is "
             "updated to this Stage, Subcontractor’s Time Entry is "
             "created automatically"
    )


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _check_outsourcing_pol(self):
        existing_pol = self.timesheet_ids.mapped('purchase_order_line_id')
        outsourcing_pol = self.outsourcing_line_ids.filtered(
                lambda pol: pol.order_id.is_outsourcing and
                pol.state in ['purchase', 'done'] and
                pol.partner_id.subcontracting_auto_time_entries and
                pol.product_id.automate_time_entries and
                pol.id not in existing_pol.ids
        )
        if outsourcing_pol:
            return outsourcing_pol
        return False

    def _create_timesheet_line(self, outsourcing_pol):
        self.ensure_one()
        account_analytic_obj = self.env['account.analytic.line']
        for ol in outsourcing_pol:
            vals = {
                'date_time': datetime.today(),
                'employee_id': ol.partner_id.employee_id.id,
                'name': _('Module Realisation'),
                'unit_amount': ol.product_qty,
                'account_id': self.project_id.analytic_account_id.id,
                'project_id': self.project_id.id,
                'task_id': self.id,
                'purchase_order_line_id': ol.id,
            }
            timesheet = account_analytic_obj.sudo(
                self.env.ref('base.user_root')).create(vals)
            self._add_po_chatter_message(timesheet)

    def _add_po_chatter_message(self, ts):
        self.ensure_one()
        message = '<ul>'
        message += _('<li>User: {} </li>').format(
            self.env.ref('base.user_root').name)
        if ts.employee_id:
            message += _('<li> Employee: {} </li>').format(ts.employee_id.name)
        message += '<li> {} </li>'.format(ts.date_time)
        if ts.task_id:
            message += _('<li> Task: {} </li>').format(ts.task_id.name)
            message += _('<li> Status: {} </li>').format(
                ts.task_id.stage_id.name)
        message += _('<li> A time entry has been automatically created '
                     'for PO line {} <br> - {} </li>').format(
            ts.purchase_order_line_id.order_id.name, ts.name)
        ts.purchase_order_line_id.order_id.message_post(body=message)

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        for record in self:
            if 'stage_id' in vals and self.env['project.task.type'].browse(
                    vals['stage_id']).create_subcontractors_time_entries:
                print('====================stage name', self.env['project.task.type'].browse(
                    vals['stage_id']).name)
                outsourcing_pol = record._check_outsourcing_pol()
                print('====================outsourcing_pol',
                      outsourcing_pol)
                if outsourcing_pol:
                    record._create_timesheet_line(outsourcing_pol)
        return res
