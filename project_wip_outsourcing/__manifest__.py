# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project WIP Outsourcing',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Generate WIP journal entries from purchase orders',
    'depends': [
        'project_wip',
        'purchase',
    ],
    'data': [
        'views/outsourcing_purchase_order.xml',
        'views/outsourcing_supplier_invoice.xml',
        'views/project_task_outsourcing_tab.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
