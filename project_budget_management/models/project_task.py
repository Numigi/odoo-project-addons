# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.notify_template_task_changed_to_project(_("added"))
        return res

    @api.multi
    def write(self, vals):
        if "project_id" in vals:
            project_updated_template_tasks = self.filtered(
                lambda r: r.project_id.id != vals["project_id"]
            )
            project_updated_template_tasks.notify_template_task_changed_to_project(
                _("removed from project")
            )
        res = super(ProjectTask, self).write(vals)

        if "project_id" in vals:
            project_updated_template_tasks.notify_template_task_changed_to_project(
                _("added")
            )
        elif "min_hours" in vals or "planned_hours" in vals or "max_hours" in vals:
            self.notify_template_task_changed_to_project(_("modified"))
        return res

    @api.multi
    def unlink(self):
        self.notify_template_task_changed_to_project(_("deleted"))
        return super().unlink()

    @api.multi
    def notify_template_task_changed_to_project(self, action):
        message = "<ul><li>%s</li></ul>" % (_("Task Template") + " {} " + action)
        for record in self.filtered(lambda r: r.is_template and r.project_id):
            record.project_id.message_post(body=message.format(record.id))
