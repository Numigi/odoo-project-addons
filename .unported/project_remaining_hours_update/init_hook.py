# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from datetime import datetime
from odoo import SUPERUSER_ID, fields
from odoo.api import Environment

_logger = logging.getLogger(__name__)


def _log_current_remaining_hours(cr):
    """Setup the field id_string on all tasks."""
    env = Environment(cr, SUPERUSER_ID, {})
    all_tasks = env['project.task'].search([])
    number_of_tasks = len(all_tasks)
    comment = 'Remaining hours on {}'.format(fields.Date.to_string(datetime.now()))

    for i, task in enumerate(all_tasks):
        _logger.info(
            'Logging current remaning hours on task ID={} ({} of {})'
            .format(task.id, i, number_of_tasks)
        )
        task.update_remaining_hours(
            task.remaining_hours, env.user, comment=comment
        )


def post_init_hook(cr, pool):
    _log_current_remaining_hours(cr)
