# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
import logging


_logger = logging.getLogger(__name__)


class MeetingMinutesProject(models.Model):
    _name = "meeting.minutes.project"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _inherits = {"meeting.minutes.mixin": "meeting_minute_id"}

    def temporary_fix_recreate_old_tables(self):
        """
        This is a temporary method to fix a broken uninstallation state.
        It recreates empty versions of the old tables so that the
        uninstallation process can complete without a KeyError.
        """
        _logger.info(
            "Executing temporary fix: Recreating empty tables for uninstallation.")

        # We only need tables with a primary key to satisfy the uninstaller.
        # The exact structure doesn't matter.
        tables_to_recreate = [
            "means_communication",
            "meeting_minutes",
            "meeting_minutes_discuss_point",
            "meeting_minutes_signature",
            "meeting_minutes_res_partner_rel",
        ]

        for table_name in tables_to_recreate:
            self.env.cr.execute(
                "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
                (table_name,))
            if not self.env.cr.fetchone():
                _logger.info(f"Recreating empty table: {table_name}")
                # We create a minimal table with just an 'id' column.
                self.env.cr.execute(
                    f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY);")

        _logger.info(
            "Temporary fix completed. You can now try to uninstall the old modules.")
        return True

    def _get_actions_domain(self):
        homework = self.env.ref("meeting_minutes_project.activity_homework")
        domain = [
            ("res_model", "=", "project.task"),
            ("activity_type_id", "=", homework.id),
            ("date_deadline", "<", fields.Date.context_today(self)),
        ]
        return domain

    task_id = fields.Many2one(
        "project.task",
        string="Task",
        ondelete="restrict",
    )
    project_id = fields.Many2one(
        "project.project",
        string="Project",
    )
    meeting_minute_id = fields.Many2one(
        "meeting.minutes.mixin",
        string="Meeting Minute",
        required=True,
        ondelete="cascade",
    )
    discuss_point_ids = fields.One2many(
        "meeting.minutes.discuss.point", "meeting_minutes_id", string="Discussed Points"
    )

    action_ids = fields.Many2many(
        "mail.activity",
        string="Pending Actions",
        domain=lambda self: self._get_actions_domain(),
    )
    homework_ids = fields.One2many(
        "mail.activity",
        "meeting_minutes_id",
        string="Homework",
    )

    def _set_meeting_minutes_name(self, record):
        self.ensure_one()
        self.name = record.display_name

    def _set_document_ref(self, record, model):
        self.ensure_one()
        self.res_id = record.id
        self.res_model = model
        if self.meeting_minute_id:
            self.meeting_minute_id.res_model = model

    def _set_attendees(self, record):
        self.ensure_one()
        # Filter odoobot to avoid displaying it on edit mode then disappear on save
        odoobot_id = self.env.ref("base.partner_root")
        partner_follower_ids = record.message_follower_ids.filtered(
            lambda f: f.partner_id
            and not f.channel_id
            and not f.partner_id.is_company
            and f.partner_id != odoobot_id
        )
        self.partner_ids = [
            (6, 0, [follower.partner_id.id for follower in partner_follower_ids])
        ]

    @api.onchange("task_id")
    def on_change_task_id(self):
        if self.task_id:
            self._set_attendees(self.task_id)
            self.project_id = self.task_id.project_id.id
            self._set_document_ref(self.task_id, "project.task")
            self._set_meeting_minutes_name(self.task_id)

    @api.onchange("project_id")
    def on_change_project_id(self):
        if self.project_id and not self.task_id:
            self._set_attendees(self.project_id)
            self._set_document_ref(self.project_id, "project.project")
            self._set_meeting_minutes_name(self.project_id)

    def _get_activities(self, project_id):
        homework = self.env.ref("meeting_minutes_project.activity_homework")
        domain = [
            ("res_model", "=", "project.task"),
            ("res_id", "in", project_id.task_ids.ids),
            ("activity_type_id", "=", homework.id),
            ("date_deadline", "<", fields.Date.context_today(self)),
        ]
        return self.env["mail.activity"].search(domain)

    @api.model
    def create(self, vals):
        if vals.get("project_id"):
            project_id = self.env["project.project"].browse(vals.get("project_id"))
            activity_ids = self._get_activities(project_id)
            vals["action_ids"] = [(4, activity_id.id) for activity_id in activity_ids]

        res = super(MeetingMinutesProject, self).create(vals)
        if res.task_id:
            res._set_document_ref(res.task_id, "project.task")
        elif res.project_id:
            res._set_document_ref(res.project_id, "project.project")

        return res

    def action_load_pending_action(self):
        self.ensure_one()
        activity_ids = self._get_activities(self.project_id)
        self.action_ids = [(4, activity_id.id) for activity_id in activity_ids]
