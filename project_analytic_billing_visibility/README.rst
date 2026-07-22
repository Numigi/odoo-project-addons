===================================
Project Analytic Billing Visibility
===================================

Context
=======
By default in Odoo, analytic lines linked to an accounting move are hidden from users who do not have accounting access rights.
This module ensures Project Managers have complete and reliable visibility over the costs and revenues of their projects (in the "Costs & Revenues" view) without granting them any access to the accounting application, menus, or financial documents.

Description
===========
This module modifies the existing record rule ``account_analytic_line_rule_billing_user`` to grant read access to users belonging to the ``Project / Administrator`` group.

Usage
=====
1. Assign a user to the ``Project / Administrator`` role.
2. Navigate to a Project.
3. Open the "Costs & Revenues" smart button.
4. The user will be able to see all analytic lines, including those linked to an accounting move (e.g., allocation costs).
5. The user remains unable to open the underlying invoices or access the accounting application.

Credits
=======
* Numigi
* Odoo Community Association (OCA)