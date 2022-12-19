# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    project_managers = env.ref("project.group_project_manager").users
    project_managers.write({"groups_id": [(4, env.ref("project_wip.group_wip_to_cgs").id)]})
