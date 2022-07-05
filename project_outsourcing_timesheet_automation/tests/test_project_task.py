# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import OutsourcingCase


class TestProjectTask(OutsourcingCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_timesheet_line_automatically(self):
        self.task.write({"stage_id": self.stage_test.id})
        assert len(self.task.timesheet_ids) == 1
        assert self.task.timesheet_ids.mapped('purchase_order_line_id') in \
               self.task.outsourcing_line_ids

    def test_timesheet_line_when_change_task_stage(self):
        self.task.write({"stage_id": self.stage_done.id})
        assert len(self.task.timesheet_ids) == 1
        assert self.task.timesheet_ids.mapped('purchase_order_line_id') in \
               self.task.outsourcing_line_ids
