# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    project_consu_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Project Consumption Location",
        domain="[('usage', '=', 'production'), ('company_id', '=', id)]",
        help="Dedicated production location for project material consumptions "
             "to avoid overlapping with standard manufacturing routes.",
    )

    def write(self, vals):
        """
        When the project consumption location is manually changed on the company,
        force the update of all related warehouse routes and picking types.
        """
        res = super(ResCompany, self).write(vals)

        # Check if the user manually changed the project location
        if "project_consu_location_id" in vals:
            # Find all warehouses belonging to the updated companies
            warehouses = self.env["stock.warehouse"].search([
                ("company_id", "in", self.ids)
            ])

            for warehouse in warehouses:
                # Force the recomputation of the location on the warehouse
                # to ensure the new value is used before updating routes
                warehouse._compute_consu_location_id()

                # Regenerate all picking types and routes with the new location
                warehouse.sudo()._create_or_update_consumption_picking_types()
                warehouse.sudo()._create_or_update_consumption_route()
                warehouse.sudo()._create_or_update_consumption_mto_pull()

        return res
