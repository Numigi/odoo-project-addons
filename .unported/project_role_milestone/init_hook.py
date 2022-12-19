import logging

logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):

    cr.execute(" ALTER TABLE project_assignment DROP CONSTRAINT IF EXISTS project_assignment_project_role_user_uniq")
    logger.info("project_assignment_project_role_user_uniq was successfully dropped")
    cr.execute(" ALTER TABLE project_assignment DROP CONSTRAINT IF EXISTS project_assignment_company_role_user_uniq")
    logger.info("project_assignment_company_role_user_uniq was successfully dropped")


