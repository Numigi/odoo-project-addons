# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _setup_warehouses_consumption_routes(env)


def _setup_warehouses_consumption_routes(env):
    warehouses = env["stock.warehouse"].search([])
    for warehouse in warehouses:
        warehouse._set_project_consu_location(warehouse.company_id.id)
        warehouse._compute_consu_location_id()
        warehouse._create_or_update_consumption_picking_types()
        warehouse._create_or_update_consumption_route()
        warehouse._create_consumption_mto_pull()
