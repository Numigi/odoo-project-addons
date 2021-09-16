from odoo import models, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.onchange("project_id")
    def _onchange_project_id(self):
        for project in self.env["project.project"]:
            tasks = self.env["project.task"].search(
                [
                    ("project_id", "=", project.id),
                    ("is_template", "=", True),
                ]
            )
            project.template_task_ids = tasks
