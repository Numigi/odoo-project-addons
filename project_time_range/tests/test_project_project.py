# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common
from odoo.exceptions import ValidationError

from ..models.project_task import ARROW_ICON


class TestProjectWithMinMax(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env['project.project'].create({'name': 'Project A'})

    def test_ifIdealDifferent0_thenMinHasToBeLesserThanIdeal(self):
        with self.assertRaises(ValidationError):
            self.project_a.write({
                'planned_hours': 10,
                'min_hours': 11
            })

    def test_ifIdealDifferent0_theMinCanBeEqualToIdeal(self):
        self.project_a.write({
            'planned_hours': 10,
            'min_hours': 10,
            'max_hours': 11,
        })
        assert self.project_a.min_hours == 10

    def test_ifIdealDifferent0_thenMaxHasToBeGreaterThanIdeal(self):
        with self.assertRaises(ValidationError):
            self.project_a.write({
                'planned_hours': 10,
                'max_hours': 9
            })

    def test_ifIdealDifferent0_theMaxCanBeEqualToIdeal(self):
        self.project_a.write({
            'planned_hours': 10,
            'max_hours': 10
        })
        assert self.project_a.max_hours == 10

    def test_idealCanBeNone(self):
        """ Just checking that the case where planned_hours is None does not
        raise an error."""
        self.project_a.write({
            'planned_hours': None
        })
        assert self.project_a.max_hours == 0
        assert self.project_a.min_hours == 0


class TestProjectBudgetFields(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env["project.project"].create({"name": "Project A"})
        cls.task_a = cls.env["project.task"].create(
            {
                "name": "Task Template A",
                "is_template": True,
                "project_id": cls.project_a.id,
                "min_hours": 1,
                "planned_hours": 2,
                "max_hours": 4,
            }
        )
        cls.task_b = cls.env["project.task"].create(
            {
                "name": "Task Template B",
                "is_template": True,
                "project_id": cls.project_a.id,
                "min_hours": 8,
                "planned_hours": 16,
                "max_hours": 32,
            }
        )

    def test_project_budget_fields_sum(self):
        assert self.project_a.min_hours == 9
        assert self.project_a.planned_hours == 18
        assert self.project_a.max_hours == 36

    def test_project_tracking_message_for_task_template_add(self):
        task_c = self.env["project.task"].create(
            {
                "name": "Task Template C",
                "is_template": True,
                "project_id": self.project_a.id,
                "min_hours": 64,
                "planned_hours": 128,
                "max_hours": 256,
            }
        )
        assert self.project_a.min_hours == 73
        assert self.project_a.planned_hours == 146
        assert self.project_a.max_hours == 292
        mail_message = self._get_last_mail_message(self.project_a.id)
        assert mail_message.body == (
            "<p>Task Template %s added:<br>• Min 0 arrow 64<br>• Ideal 0 arrow 128<br>• Max 0 arrow 256</p>"
            % task_c.id
        ).replace("arrow", ARROW_ICON)

    def test_project_tracking_message_for_task_template_remove(self):
        self.task_b.unlink()
        assert self.project_a.min_hours == 1
        assert self.project_a.planned_hours == 2
        assert self.project_a.max_hours == 4
        mail_message = self._get_last_mail_message(self.project_a.id)
        assert mail_message.body == (
            "<p>Task Template %s removed:<br>• Min 8.0 arrow 0<br>• Ideal 16.0 arrow 0<br>• Max 32.0 arrow 0</p>"
            % self.task_b.id
        ).replace("arrow", ARROW_ICON)

    def test_project_tracking_message_for_task_template_update(self):
        self.task_b.write({"min_hours": 64, "planned_hours": 128, "max_hours": 256})
        assert self.project_a.min_hours == 65
        assert self.project_a.planned_hours == 130
        assert self.project_a.max_hours == 260
        mail_message = self._get_last_mail_message(self.project_a.id)
        assert mail_message.body == (
            "<p>Task Template %s updated:<br>• Min 8.0 arrow 64<br>• Ideal 16.0 arrow 128<br>• Max 32.0 arrow 256</p>"
            % self.task_b.id
        ).replace("arrow", ARROW_ICON)

    def _get_last_mail_message(self, project_id):
        return self.env["mail.message"].search(
            [("model", "=", "project.project"), ("res_id", "=", project_id)],
            order="id desc",
            limit=1
        )
