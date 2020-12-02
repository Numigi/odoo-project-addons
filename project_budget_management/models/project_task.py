# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models

ADDED = "added"
MODIFIED = "modified"
DELETED = "deleted"
REMOVED = "removed"


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.notify_template_task_changed_to_project(ADDED)
        return res

    @api.multi
    def write(self, vals):
        if "project_id" in vals:
            project_updated_template_tasks = self.filtered(
                lambda r: r.project_id.id != vals["project_id"]
            )
            project_updated_template_tasks.notify_template_task_changed_to_project(
                REMOVED
            )
        res = super(ProjectTask, self).write(vals)

        if "project_id" in vals:
            project_updated_template_tasks.notify_template_task_changed_to_project(
                ADDED
            )
        elif "min_hours" in vals or "planned_hours" in vals or "max_hours" in vals:
            self.notify_template_task_changed_to_project(MODIFIED)
        return res

    @api.multi
    def unlink(self):
        self.notify_template_task_changed_to_project(DELETED)
        return super().unlink()

    @api.multi
    def notify_template_task_changed_to_project(self, action):
        message_template = _(
            """
            <b>{action}</b>
            <ul>
                <li>Min: {min}</li>
                <li>Ideal: {ideal}</li>
                <li>Max: {max}</li>
            </ul>
        """
        )
        for record in self.filtered(lambda r: r.is_template and r.project_id):
            project = record.project_id
            message = message_template.format(
                action=self._format_template_task_action(action),
                min=format_float_time(project.min_hours),
                ideal=format_float_time(project.planned_hours),
                max=format_float_time(project.max_hours),
            )
            record.project_id.message_post(body=message)

    def _format_template_task_action(self, action):
        if action == ADDED:
            message = _("Task template #{} added")
        elif action == MODIFIED:
            message = _("Task template #{} modified")
        elif action == REMOVED:
            message = _("Task template #{} removed from the project")
        else:
            message = _("Task template #{} deleted")
        return message.format(self.id)


def format_float_time(value):
    """Format a float into an hh:mm representation.

    Extracted from odoo/addons/base/models/ir_qweb_fields.py
    """
    hours, minutes = divmod(abs(value) * 60, 60)
    minutes = round(minutes)
    if minutes == 60:
        minutes = 0
        hours += 1
    if value < 0:
        return "-%02d:%02d" % (hours, minutes)
    return "%02d:%02d" % (hours, minutes)
