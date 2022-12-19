# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProject(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.folded_stage = cls.env["project.task.type"].create(
            {"name": "Done", "fold": True}
        )
        cls.project_a = cls.env["project.project"].create({"name": "Project A"})
        cls.task_a = cls.env["project.task"].create(
            {
                "name": "Task A",
                "project_id": cls.project_a.id,
                "min_hours": 1,
                "planned_hours": 2,
                "max_hours": 4,
                "stage_id": cls.folded_stage.id,
            }
        )
        cls.task_b = cls.env["project.task"].create(
            {
                "name": "Task B",
                "project_id": cls.project_a.id,
                "min_hours": 8,
                "planned_hours": 16,
                "max_hours": 32,
                "stage_id": cls.folded_stage.id,
            }
        )

    def test_task_created(self):
        self.env["project.task"].create(
            {
                "name": "Task C",
                "project_id": self.project_a.id,
                "min_hours": 64,
                "planned_hours": 128,
                "max_hours": 256,
            }
        )
        assert self.project_a.min_hours == 73
        assert self.project_a.planned_hours == 146
        assert self.project_a.max_hours == 292

    def test_task_child_excluded(self):
        self.task_b.parent_id = self.task_a
        assert self.project_a.min_hours == 1

    def test_task_unlinked(self):
        self.task_b.unlink()
        assert self.project_a.min_hours == 1

    def test_task_archived(self):
        self.task_b.active = False
        assert self.project_a.min_hours == 1

    def test_task_unarchived(self):
        self.task_b.active = False
        self.task_b.active = True
        assert self.project_a.min_hours == 9

    def test_task_moved(self):
        self.task_b.project_id = self.project_a.copy()
        assert self.project_a.min_hours == 1

    def test_task_updated(self):
        self.task_b.write({"min_hours": 64, "planned_hours": 128, "max_hours": 256})
        assert self.project_a.min_hours == 65
        assert self.project_a.planned_hours == 130
        assert self.project_a.max_hours == 260

    def test_consumed_and_remaining_hours(self):
        self.env["account.analytic.line"].create(
            {"project_id": self.project_a.id, "name": "/", "unit_amount": 1}
        )
        assert self.project_a.consumed_hours == 1
        assert self.project_a.remaining_hours == 17  # 2 + 16 - 1

    def test_consumed_and_remaining_hours__no_analytic_line(self):
        assert self.project_a.consumed_hours == 0
        assert self.project_a.remaining_hours == 18
