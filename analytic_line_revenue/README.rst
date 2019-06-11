Analytic Line Revenue
=====================

.. contents:: Table of Contents

Context
-------
In vanilla Odoo, there is no distinction between analytic lines generated from expenses versus revenues.

The sign of the amount can not be used for this purpose.
For example, a supplier refund would be classified as a revenue.

Summary
-------
This module adds a boolean field `Revenue` on analytic lines.

.. image:: static/description/analytic_line_form.png

When validating a journal entry, if a line has an account of type `Revenue`, the checkbox `Revenue`
will be checked on the analytic lines.

Any other analytic line is a cost by default.

Usage
-----
As member of the group `Sale / User`, I validate a customer invoice.

.. image:: static/description/customer_invoice_form.png

I notice that the generated analytic lines are revenues.

.. image:: static/description/customer_invoice_analytic_lines.png

Filters
-------
In the list of analytic lines, I find 2 new filters `Costs` and `Revenues`.

.. image:: static/description/analytic_line_filters.png

If I check `Costs`, the list view will exclude analytic lines with `Revenue` checked.

.. image:: static/description/analytic_line_costs.png

If I check `Revenues`, the list view will exclude analytic lines with `Revenue` unchecked.

.. image:: static/description/analytic_line_revenues.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
