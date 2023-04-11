# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
import pytz
from datetime import datetime
from odoo import api, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class ProjectMilestoneTimeReport(models.AbstractModel):
    _name = "project.milestone.time.report"
    _description = "Milestone Time Report"

    @api.model
    def get_html(self, project_id):
        project = self._get_project(project_id)
        rendering_variables = self.get_rendering_variables(project)
        return self.env.ref(
            "project_milestone_time_report.project_report_report_html"
        )._render(rendering_variables)

    @api.model
    def get_pdf(self, project_id):
        # context = dict(self.env.context)
        project = self._get_project(project_id)
        # base_url = self._get_report_url()
        # rcontext = {
        #     'mode': 'print',
        #     'base_url': base_url,
        # }
        rendering_variables = self.get_rendering_variables(project)
        # rendering_variables.update({"mode": "print", "base_url": base_url})
        # body = self.env["ir.ui.view"]._render_template(
        #     "project_milestone_time_report.project_report_report_pdf",
        #     values=rendering_variables,
        # )
        _logger.info('>>>>>>>>rendering_variables>>>>>>>>>><: %s',
                     rendering_variables)
        # body = self.env['ir.ui.view'].with_context(context)._render_template(
        #     "project_milestone_time_report.project_report_report_pdf",
        #     values=dict(rcontext, lines=rendering_variables,
        #                 report=self, context=self),
        # )
        body = self.env["ir.ui.view"]._render_template(
            "project_milestone_time_report.project_report_report_pdf",
            values=rendering_variables,
        )
        _logger.info('>>>>>>>>body>>>>>>>>>>: %s',
                     body)
        header = self.env["ir.actions.report"]._render_template(
            "web.external_layout", values=rendering_variables
        )
        _logger.info('>>>>>>>>header>>>>>>>>>>: %s',
                     header)
        return self.env["ir.actions.report"]._run_wkhtmltopdf(
            [body],
            header=header,
            landscape=True,
            specific_paperformat_args={
                "data-report-margin-top": 10,
                "data-report-header-spacing": 10,
            },
        )

    @api.model
    def get_filename(self, project_id):
        project = self._get_project(project_id)
        est = pytz.timezone("EST")
        datetime_ = datetime.now(tz=pytz.utc).astimezone(est)
        return "{project}_Rapport des temps_{datetime}.pdf".format(
            project=project.display_name,
            datetime=datetime_.strftime(DATETIME_FORMAT),
        )

    @api.model
    def _get_report_url(self):
        config = self.env["ir.config_parameter"].sudo()
        return config.get_param("report.url") \
            or config.get_param("web.base.url")

    @api.model
    def get_rendering_variables(self, project):
        lines = self._get_lines(project)
        return {
            "report": self,
            "project": project,
            "lines": lines,
        }

    @api.model
    def consumed_hours_clicked(self, project_id):
        action = self._get_analytic_line_action()
        project = self._get_project(project_id)
        action["name"] = _("({project}) - Consumed Hours").format(
            project=project.display_name
        )
        action["context"] = {
            "search_default_project_id": project_id,
            "search_default_not_lump_sum": True,
        }
        return action

    @api.model
    def estimated_hours_clicked(self, project_id):
        action = self._get_milestone_action()
        project = self._get_project(project_id)
        action["name"] = _("({project}) - Milestones").format(
            project=project.display_name
        )
        action["context"] = {
            "search_default_project_id": project_id,
            "search_default_not_lump_sum": True,
        }
        return action

    @api.model
    def total_consumed_hours_clicked(self, project_id):
        action = self._get_analytic_line_action()
        action["name"] = _("Total Consumed Hours")
        action["context"] = {
            "search_default_parent_project_id": project_id,
            "search_default_not_lump_sum": True,
        }
        return action

    @api.model
    def total_estimated_hours_clicked(self, project_id):
        action = self._get_milestone_action()
        action["name"] = _("Milestones")
        action["context"] = {
            "search_default_parent_project_id": project_id,
            "search_default_not_lump_sum": True,
        }
        return action

    @api.model
    def _get_project(self, project_id):
        return self.env["project.project"].browse(project_id)

    def _get_analytic_line_action(self):
        return {
            "res_model": "account.analytic.line",
            "views": [[False, "list"], [False, "form"]],
            "type": "ir.actions.act_window",
            "target": "current",
        }

    def _get_milestone_action(self):
        return {
            "res_model": "project.milestone",
            "views": [[False, "list"], [False, "form"]],
            "type": "ir.actions.act_window",
            "target": "current",
        }

    @api.model
    def _get_lines(self, project):
        lots = project.child_ids.filtered(lambda p: not p.lump_sum)
        projects = (project | lots).sorted("display_name")
        return [self._get_project_line(p) for p in projects]

    @api.model
    def _get_project_line(self, project):
        return {
            "project": project,
            "total_estimated_hours": project.total_estimated_hours,
            "consumed_hours": project.total_spent_hours,
            "budget_remaining":
                project.total_estimated_hours - project.total_spent_hours,
        }
