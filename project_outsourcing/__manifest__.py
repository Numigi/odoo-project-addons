# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Outsourcing',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Generate outsourcing purchase orders from tasks',
    'depends': [
        'purchase',
        'project_task_analytic_lines',
    ],
    'data': [
        'views/purchase_order.xml',
        'views/supplier_invoice.xml',
        'views/project_outsourcing_smart_button.xml',
        'views/task_outsourcing_tab.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
