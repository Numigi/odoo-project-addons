# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models

ARROW_ICON = '<span class="fa fa-long-arrow-right"></span>'


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.message_post_project_budget_change(function="create", vals=vals)
        return res

    @api.multi
    def write(self, vals):
        for record in self:
            old_vals = {
                "project_id": record.project_id and record.project_id.id or None,
                "min_hours": record.min_hours,
                "planned_hours": record.planned_hours,
                "max_hours": record.max_hours,
            }
            super(ProjectTask, record).write(vals)
            record.message_post_project_budget_change(function="write", vals=vals, old_vals=old_vals)

    @api.multi
    def unlink(self):
        for record in self:
            record.message_post_project_budget_change(function="unlink")
            super(ProjectTask, record).unlink()

    @api.multi
    def message_post_project_budget_change(self, function, vals=None, old_vals=None):
        self.ensure_one()
        if vals and not any(["project_id" in vals, "min_hours" in vals, "planned_hours" in vals, "max_hours" in vals]):
            return

        msg = ""

        def generate_msg(task_id, action, min_from, min_to, ideal_from, ideal_to, max_from, max_to, show_always=True):
            message = "Task Template %s %s:" % (task_id, action)
            if show_always or (min_from or min_to):
                message += "<br>• Min %s" % (" ".join([str(min_from), ARROW_ICON, str(min_to)]))
            if show_always or (ideal_from or ideal_to):
                message += "<br>• Ideal %s" % (" ".join([str(ideal_from), ARROW_ICON, str(ideal_to)]))
            if show_always or (max_from or max_to):
                message += "<br>• Max %s" % (" ".join([str(max_from), ARROW_ICON, str(max_to)]))
            return message

        if function == "create" and vals.get("project_id"):
            msg = generate_msg(
                self.id,
                "added",
                0, vals.get("min_hours", 0),
                0, vals.get("planned_hours", 0),
                0, vals.get("max_hours", 0)
            )

        elif function == "write":
            if "project_id" in vals:
                if old_vals["project_id"]:  # post message on removed project
                    msg = generate_msg(
                        self.id,
                        "removed",
                        old_vals["min_hours"], 0,
                        old_vals["planned_hours"], 0,
                        old_vals["max_hours"], 0
                    )
                    self.env["project.project"].browse(old_vals["project_id"]).message_post(body=_(msg))
                if not vals.get("project_id"):
                    return  # project_id is emptied. This case should never happen because it is blocked by a control
            if vals.get("project_id"):
                msg = generate_msg(
                    self.id,
                    "added",
                    0, vals.get("min_hours", old_vals["min_hours"]),
                    0, vals.get("planned_hours", old_vals["planned_hours"]),
                    0, vals.get("max_hours", old_vals["max_hours"]),
                )
            else:
                msg = generate_msg(
                    self.id,
                    "updated",
                    "min_hours" in vals and old_vals["min_hours"], "min_hours" in vals and vals.get("min_hours"),
                    "planned_hours" in vals and old_vals["planned_hours"],
                    "planned_hours" in vals and vals.get("planned_hours"),
                    "max_hours" in vals and old_vals["max_hours"], "max_hours" in vals and vals.get("max_hours"),
                    show_always=False
                )

        elif function == "unlink" and self.project_id:
            msg = generate_msg(
                self.id,
                "removed",
                self.min_hours, 0,
                self.planned_hours, 0,
                self.max_hours, 0,
            )

        self.project_id.message_post(body=_(msg))
