from odoo import fields, models


class ProjectWipBatchClosing(models.TransientModel):
    """
    Transient model for batch closing of project WIP.
    """

    _name = "project.wip.batch.closing"
    _description = "Project Transfer WIP To CGS Batch"

    state = fields.Selection(
        [
            ("date_step", "Select Closing Date"),
            ("project_step", "Select Project"),
            ("processing_step", "Processing"),
        ],
        string="Status",
        readonly=True,
        required=True,
        default="date_step",
    )

    date_cutoff = fields.Date("Cut Off Date", required=True)
    project_ids = fields.One2many("project.wip.transfer", "batch_closing_id")

    def action_select_date(self):
        """
        Action to select the cut-off date and populate projects.
        """
        domain = [
            ("company_id", "=", self.env.company.id),
            ("type_id.wip_account_id", "!=", False),
            ("type_id.cgs_journal_id", "!=", False),
            ("type_id.cgs_account_id", "!=", False),
        ]

        project_ids = self.env["project.project"].search(domain)
        record_values = []
        for project in project_ids:
            costs_to_transfer = sum(
                line.balance for line in project._get_posted_unreconciled_wip_lines()
            )
            if costs_to_transfer != 0:
                vals = {
                    "project_id": project.id,
                    "costs_to_transfer": costs_to_transfer,
                }
                record_values.append((0, 0, vals))

        self.write({"project_ids": record_values})
        self.state = "project_step"

        return {
            "type": "ir.actions.act_window",
            "name": "Transfer WIP to CGS",
            "res_model": "project.wip.batch.closing",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def action_select_project(self):
        """
        Action to select projects for processing.
        """
        self.state = "processing_step"
        return {
            "type": "ir.actions.act_window",
            "name": "Transfer WIP to CGS",
            "res_model": "project.wip.batch.closing",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def action_processing(self):
        """
        Initiates the processing of WIP to CGS transfer for selected projects.
        """
        # eta = datetime.now() + timedelta(minutes=15)
        for line in self.project_ids.filtered(lambda x: x.to_process):
            line.project_id.with_delay(priority=1).action_wip_to_cgs(self.date_cutoff)

    def action_select_all(self):
        """
        Selects all projects for processing.
        """
        self.project_ids.write({"to_process": True})
        return {
            "name": "__",
            "view_mode": "form",
            "view_id": False,
            "res_model": self._name,
            "domain": [],
            "context": dict(self._context, active_ids=self.ids),
            "type": "ir.actions.act_window",
            "target": "new",
            "res_id": self.id,
        }

    def action_deselect_all(self):
        """
        Deselects all projects for processing.
        """
        self.project_ids.write({"to_process": False})
        return {
            "name": "__",
            "view_mode": "form",
            "view_id": False,
            "res_model": self._name,
            "domain": [],
            "context": dict(self._context, active_ids=self.ids),
            "type": "ir.actions.act_window",
            "target": "new",
            "res_id": self.id,
        }


class ProjectWipTransferWizard(models.TransientModel):
    """
    Wizard for project WIP transfer, inherited for batch closing.
    """

    _inherit = "project.wip.transfer"

    batch_closing_id = fields.Many2one("project.wip.batch.closing", "Batch closing")
    to_process = fields.Boolean(default=True)
