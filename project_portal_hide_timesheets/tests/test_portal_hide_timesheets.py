# Copyright 2023-today  Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase


class TestPortalHideTimesheets(TransactionCase):
    def test_module_installed(self):
        """Test that the module is properly installed."""
        module = self.env["ir.module.module"].search(
            [("name", "=", "project_portal_hide_timesheets")]
        )
        self.assertEqual(module.state, "installed")
