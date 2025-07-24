# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project WIP Batch Closing",
    "version": "14.0.1.4.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "WIP accounting entries from consumed products",
    "depends": [
        "queue_job",
        "queue_job_auto_requeue",
        "project_wip_material"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/project_wip_batch_closing.xml",
        "views/transfer_wip_batch.xml",
    ],
    "installable": True,
}
