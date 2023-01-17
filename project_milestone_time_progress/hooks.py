# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def recompute_progress_hook(cr, registry):
    """ Recompute existing milestones progress """
    _logger.info('Start Recomputing Milestones Progress')
    env = api.Environment(cr, SUPERUSER_ID, {})
    model = env['project.milestone']
    env.add_todo(model._fields['progress'], model.search([]))
    model.recompute()
    _logger.info('End Recomputing Milestones Progress')
