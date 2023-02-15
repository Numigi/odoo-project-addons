# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common


class TestDefaultTaskStage(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stage_1 = cls.env['project.task.type'].create({'name': 'Stage 1'})
        cls.stage_2 = cls.env['project.task.type'].create({'name': 'Stage 2'})
        cls.project_type = cls.env['project.type'].create({
            'name': 'My Project Type',
            'default_task_stage_ids': [(6, 0, [cls.stage_1.id, cls.stage_2.id])]
        })
        cls.project = cls.env['project.project'].create({'name': 'My Project'})

    def test_onchange_project_type__task_stages_set(self):
        self.project.type_id = self.project_type
        self.project._on_change_project_type_id__set_default_task_stages()
        assert self.project.type_ids == self.stage_1 | self.stage_2
