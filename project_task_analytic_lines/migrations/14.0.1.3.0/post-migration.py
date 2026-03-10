# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Post-migration script to update the project_id on existing analytic lines.
    It uses raw SQL for better performance on large tables.
    """
    if not version:
        return

    _logger.info("Starting the update of project_id on analytic lines...")

    # Set project_id from task_id if available
    cr.execute("""
        UPDATE account_analytic_line aal
        SET project_id = pt.project_id
        FROM project_task pt
        WHERE aal.project_id IS NULL
          AND aal.task_id = pt.id
          AND pt.project_id IS NOT NULL
    """)

    # Set project_id from origin_task_id if task_id did not provide a project
    cr.execute("""
        UPDATE account_analytic_line aal
        SET project_id = pt.project_id
        FROM project_task pt
        WHERE aal.project_id IS NULL
          AND aal.origin_task_id = pt.id
          AND pt.project_id IS NOT NULL
    """)

    _logger.info("Analytic lines successfully updated.")
