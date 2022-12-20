# -*- coding: utf-8 -*-
# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import SUPERUSER_ID
from odoo.api import Environment

_logger = logging.getLogger(__name__)


def post_init_hook(cr, pool):
    setup_task_id_string(cr)


def setup_task_id_string(cr):
    """Setup the field id_string on all tasks."""
    _logger.info('Setting field id_string on model project.task.')
    env = Environment(cr, SUPERUSER_ID, {})
    for task in env['project.task'].with_context(active_test=False).search([]):
        task.id_string = str(task.id)
