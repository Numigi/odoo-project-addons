# -*- coding: utf-8 -*-
# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_task_id_in_display_name.init_hook import setup_task_id_string


def migrate(cr, version):
    setup_task_id_string(cr)
