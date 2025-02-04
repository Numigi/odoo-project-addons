# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestReport(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parent_project = cls.env["project.project"].create(
            {"name": "Parent Project"}
        )
        # create a generic Project with 2 milestones
        # and 2 tasks associated to milestones
        cls.folded_stage = cls.env["project.task.type"].create({
            "name": "Done", "fold": True
        })
        cls.lot = cls.env["project.project"].create({
            "name": "Lot",
            "use_milestones": True,
            "parent_id": cls.parent_project.id
        })
        cls.milestone_a = cls.env['project.milestone'].create({
            "name": "Analysis",
            "estimated_hours": 8,
            "project_id": cls.lot.id,
        })
        cls.milestone_b = cls.env['project.milestone'].create({
            "name": "Realization",
            "estimated_hours": 20,
            "project_id": cls.lot.id,
        })
        cls.task_a = cls.env["project.task"].create({
            "name": "Task A",
            "project_id": cls.lot.id,
            "milestone_id": cls.milestone_a.id,
            "planned_hours": 4,
            "stage_id": cls.folded_stage.id,
        })
        cls.task_b = cls.env["project.task"].create({
            "name": "Task B",
            "project_id": cls.lot.id,
            "milestone_id": cls.milestone_b.id,
            "planned_hours": 8,
            "stage_id": cls.folded_stage.id,
        })
        # Add timelines to created tasks
        cls.timesheet_a = cls.env["account.analytic.line"].create({
            "name": "Analyse",
            "project_id": cls.lot.id,
            "task_id": cls.task_a.id,
            "unit_amount": 3,
            "employee_id": 1,
            "date": "2022-06-25",
        })
        cls.timesheet_b = cls.env["account.analytic.line"].create({
            "name": "Conception",
            "project_id": cls.lot.id,
            "task_id": cls.task_b.id,
            "unit_amount": 4,
            "employee_id": 1,
            "date": "2022-06-30",
        })
        cls.report = cls.env["project.milestone.time.report"]

    def test_amounts(self):
        lines = self._get_lines()
        assert len(lines) == 2
        assert lines[1]["project"] == self.lot
        assert lines[1]["consumed_hours"] == self.lot.total_spent_hours
        assert lines[1]["total_estimated_hours"] == \
               self.lot.total_estimated_hours
        assert lines[1]["budget_remaining"] == \
               self.lot.total_estimated_hours - self.lot.total_spent_hours

    def test_consumed_hours_clicked(self):
        res = self.report.consumed_hours_clicked(self.lot.id)
        assert res["context"] == {
            "search_default_project_id": self.lot.id,
            "search_default_not_lump_sum": True,
        }

    def test_estimated_hours_clicked(self):
        res = self.report.estimated_hours_clicked(self.lot.id)
        assert res["context"] == {
            "search_default_project_id": self.lot.id,
            "search_default_not_lump_sum": True,
        }

    def test_total_consumed_hours_clicked(self):
        res = self.report.total_consumed_hours_clicked(self.parent_project.id)
        assert res["context"] == {
            "search_default_parent_project_id": self.parent_project.id,
            "search_default_not_lump_sum": True,
        }

    def test_total_estimated_hours_clicked(self):
        res = self.report.total_estimated_hours_clicked(self.parent_project.id)
        assert res["context"] == {
            "search_default_parent_project_id": self.parent_project.id,
            "search_default_not_lump_sum": True,
        }

    def test_report_from_child_project(self):
        lines = self.report.get_rendering_variables(self.lot)["lines"]
        assert len(lines) == 1

    def test_filename(self):
        filename = self.report.get_filename(self.lot.id)
        assert self.lot.display_name in filename

    def _get_lines(self):
        return self.report.get_rendering_variables(
            self.parent_project)["lines"]
