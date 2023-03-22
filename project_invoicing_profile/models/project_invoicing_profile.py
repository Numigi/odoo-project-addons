# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectInvoiceProfile(models.Model):

    _name = "project.invoice.profile"

    name = fields.Char(string='Name', required=True)
    note = fields.Text(string='Description')


class Project(models.Model):

    _inherit = "project.project"

    invoicing_profile_id = fields.Many2one("project.invoice.profile", string="Invoicing profile", ondelete="restrict")


class ProjectTask(models.Model):

    _inherit = "project.task"

    invoicing_profile_id = fields.Many2one(
        related="project_id.invoicing_profile_id", string="Invoicing profile", store=True)


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    invoicing_profile_id = fields.Many2one(
        related="task_id.invoicing_profile_id", string="Invoicing profile", store=True)


