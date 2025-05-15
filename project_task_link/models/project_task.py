# Copyright 2022-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from urllib.parse import urljoin

from odoo import api, fields, models
from odoo.addons.project_task_link.tools.utils import get_html_with_task_links


class ProjectTask(models.Model):
    _inherit = "project.task"

    description_portal = fields.Html(
        string="Description (Portal)",
        compute="_compute_description_portal",
    )

    @api.depends("description")
    def _compute_description_portal(self):
        """
        Compute the portal-safe description by replacing any backend task links
        with their corresponding portal URLs.
        """
        for task in self:
            html = task.description or ""
            task.description_portal = task._replace_task_links(html)

    def write(self, vals):
        if vals.get("description"):
            vals["description"] = get_html_with_task_links(
                self.env, vals["description"]
            )
        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get("description"):
            vals["description"] = get_html_with_task_links(
                self.env, vals["description"]
            )
        return super().create(vals)

    def get_base_url(self):
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url")

    def get_portal_access_url(self):
        """
        Return the full URL to access this task in the portal.
        """
        self.ensure_one()
        if not self.access_url:
            self._compute_access_url()
        base = self.get_base_url().rstrip("/")
        return urljoin(base, self.access_url or "")

    def get_form_view_access_url(self):
        """
        Return the full URL to access this task's form view in the backend.
        """
        self.ensure_one()
        base = self.get_base_url().rstrip("/")
        action = self.env.ref(
            "project.act_project_project_2_project_task_all", raise_if_not_found=False
        )
        if not action:
            return ""
        path = (
            f"/web#id={self.id}&model=project.task&view_type=form"
            f"&action={action.id}&active_id={self.project_id.id}"
        )
        return urljoin(base, path)

    def _replace_task_links(self, html):
        """
        Replace all backend task links (absolute or relative) with portal URLs.
        """
        pattern = (
            r"(?:https?://[^/]+)?"
            r"/web#id=(\d+)"
            r"(?:&|&amp;)"
            r"model=project\.task"
            r'(?:&|&amp;)[^"\']*'
        )

        def repl(match):
            task_id = int(match.group(1))
            task = self.env["project.task"].browse(task_id)
            return task.exists() and task.get_portal_access_url() or match.group(0)

        return re.sub(pattern, repl, html)
