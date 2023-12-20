# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data
from .common import TaskMaterialCase


@ddt
class TestOpenPickingsFromTaskCase(TaskMaterialCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse.consu_steps = "two_steps"

    def _create_one_procurement(self):
        self._create_material_line()

    def _create_two_procurements(self):
        # Create a first procurement
        self._create_material_line()

        # Cancel the pickings
        pickings = self.env["stock.picking"].search(
            [
                ("group_id", "=", self.task.procurement_group_id.id),
            ]
        )
        pickings.action_cancel()

        # Adding a new line creates a second procurement
        self._create_material_line()

    @data("preparation", "consumption")
    def test_if_one_picking__open_form_view(self, picking_type):
        self._create_one_procurement()
        self.env.user.write({"groups_id": [(4, self.env.ref("base.group_system").id)]})
        method = getattr(
            self.task, "open_{}_picking_view_from_task".format(picking_type)
        )
        result = method()
        assert result.get("res_id")
        assert not result.get("domain")

    @data("preparation", "consumption")
    def test_if_two_pickings__open_list_view(self, picking_type):
        self._create_two_procurements()
        self.env.user.write({"groups_id": [(4, self.env.ref("base.group_system").id)]})
        method = getattr(
            self.task, "open_{}_picking_view_from_task".format(picking_type)
        )
        result = method()
        assert not result.get("res_id")
        assert result.get("domain")
