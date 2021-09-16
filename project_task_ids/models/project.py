from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    template_task_ids = fields.One2many("project.task")
