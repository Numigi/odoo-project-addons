import pytest
from odoo.tests import tagged
from odoo.exceptions import ValidationError, AccessError
from project_wip.tests.test_project_wip_to_cgs import TestWIPTrasferToCGS


@tagged('post_install', '-at_install')
class TestWIPMaterialTrasferToCGS(TestWIPTrasferToCGS):

    def test_transfer_move_has_no_analytic_lines(self):
        """Override the inherited test to reflect the updated logic in project_wip_material."""
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.mapped("line_ids.analytic_line_ids")