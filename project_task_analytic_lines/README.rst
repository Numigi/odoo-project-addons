Project Task Analytic Lines
===========================

.. contents:: Table of Contents

Odoo Context
------------
In vanilla Odoo, analytic lines can not be grouped or filtered by task, except for timesheet lines.

Therefore, if you need to generate a cost report, only the timesheet lines will be shown per task.

Summary
-------
This module adds a `Task` field on supplier invoice lines and journal entries.

The task is propagated:

1. from invoice lines to journal entries
2. from journal entries to analytic lines

Then, the analytic lines can be filtered and grouped by task.

Journal Entries
---------------
As member of the group `Accounting / Billing`, on a draft journal entry, I find a new field `Task`.

.. image:: static/description/journal_entry_task.png

The field is readonly if the analytic account is not filled.

.. image:: static/description/journal_entry_task_readonly.png

If a project is selected, I am able to select a task related to this project.

.. image:: static/description/journal_entry_task_selected.png

I post the journal entry.

.. image:: static/description/journal_entry_posted.png

In the list of analytic lines, I notice that the task was propagated.

.. image:: static/description/journal_entry_analytic_lines.png

Supplier Invoices
-----------------
As member of the group `Accounting / Billing`, on a draft supplier invoice, I find a new field `Task`.

.. image:: static/description/supplier_invoice_form.png

The field is readonly if the analytic account is not filled.

.. image:: static/description/supplier_invoice_task_readonly.png

If a project is selected, I am able to select a task related to this project.

.. image:: static/description/supplier_invoice_task_selected.png

I validate the invoice.

.. image:: static/description/supplier_invoice_validated.png

On the journal entry, I notice that the task was propagated to the expense line.

.. image:: static/description/supplier_invoice_move.png

In the list of analytic lines, I notice that the task was propagated.

.. image:: static/description/supplier_invoice_analytic_lines.png

Taxes Included In Cost
~~~~~~~~~~~~~~~~~~~~~~
The module supports taxes included in the analytic cost.

In the form view of a tax, I check the field "Included in Analytic Cost".

.. image:: static/description/tax_with_analytic.png

On the invoice, when selecting the tax, the task is propagated along with the analytic account.

.. image:: static/description/supplier_invoice_with_tax.png

On the journal entry, the task is propagated from the invoice tax.

.. image:: static/description/supplier_invoice_with_tax_move.png

List Views Filters
------------------

Analytic Lines
~~~~~~~~~~~~~~
In the list of analytic lines, I see a new field `Task`.

..

    A new technical field (origin_task_id) was added because the field task_id
    available in vanilla Odoo could not be used.

    The field task_id is used by Odoo for timesheet lines.
    If task_id was used for any other purpose, some standard functionalities would be broken.

.. image:: static/description/analytic_lines_origin_task_column.png

I am able to search by task:

.. image:: static/description/analytic_lines_search.png

I am able to group by task:

.. image:: static/description/analytic_lines_group.png

Journal Items
~~~~~~~~~~~~~
In the list view of journal items, I see a new field `Task`.

.. image:: static/description/journal_items_task_column.png

I am able to search by task:

.. image:: static/description/journal_items_search.png

I am able to group by task:

.. image:: static/description/journal_items_group.png

Constraints
-----------
Once a task is selected on an invoice or a journal entry, it is not possible to move the task to another project.

Otherwise, when changing the project on the task, a blocking message is displayed.

.. image:: static/description/task_change_project_constraint.png

Limits
------

Purchase Orders
~~~~~~~~~~~~~~~
This module does not define how tasks are propagated from a purchase order to a supplier invoice.

The module `project_wip_outsourcing` inherits this module and adds the business logic related to outsourcing.
For now, outsourcing is the only known case where defining a task on a PO is relevant.

Stockable Products
~~~~~~~~~~~~~~~~~~
An analytic account and a task should not be set on a supplier invoice for stockable products.
The expense for a stockable product is recognized in Odoo at the customer invoice validation.

The module is intended for services (or even consummable products).

However, the module does not constrain on which type of product a task can be used.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
