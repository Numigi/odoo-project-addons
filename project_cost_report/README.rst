Project Cost Report
===================

.. contents:: Table of Contents

Summary
-------
This module adds a dynamic cost report to the `Project` application.

.. image:: static/description/report_overview.png

Usage
-----
To open the report, go to the form view of a project and click on the smart button `Cost Report`

.. image:: static/description/project_smart_button.png

Header
------
The header of the report contains the following elements:

1. The print date
2. The name of the partner related to the project
3. The project name
4. The project type (see module project_type from the same repository)

.. image:: static/description/report_overview.png

Cost Sections
-------------
The body of the report is divided into 2 tables.

The first table contains the costs of the the project.
The amounts are aggregations based on analytic lines.

.. image:: static/description/report_costs.png

These costs are seperated into the following sections:

* Products
* Time
* Outsourcing

Each section contains subdivisions that can be folded / unfolded to show / hide the details (analytic lines).

.. image:: static/description/report_subdivision_unfold.png

By clicking on the amount of a subdivision, the list of analytic lines related to this amount is displayed.

.. image:: static/description/subdivision_amount_click.png

.. image:: static/description/analytic_line_list.png

By clicking on an analytic line, the form view of the analytic line is opened.

.. image:: static/description/analytic_line_click.png

.. image:: static/description/analytic_line_form.png

Products
~~~~~~~~
This section contains analytic lines with stockable or consumable products.

It is subdivided into product categories.

.. image:: static/description/report_section_products.png

Time
~~~~
This section contains analytic lines from timesheets.

It is subdivided into types of task (see module project_task_type from the same repository).

The first subdivision `Labour` contains every timesheet line from tasks with no type.

.. image:: static/description/report_section_time.png

Outsourcing
~~~~~~~~~~~
This section contains analytic lines with products of type service that are not timesheets.

It contains only one subdivision with the same name.

.. image:: static/description/report_section_outsourcing.png

Unreceived Invoices
-------------------
The report contains a special section named `WAITING FOR INVOICES`.

This section contains a list of purchase orders related to the project
for which the supplier invoice has not been received.

.. image:: static/description/report_unreceived_invoices.png

The amount displayed on each line is computed as follow:

..

    (Ordered Quantity - Invoiced Quantity) * Unit Price

By clicking on the PO number, the form view of the PO is opened.

.. image:: static/description/purchase_order_form.png

Fold / Unfold
-------------
You may fold or unfold every sections of the report by clicking on the
buttons in the control panel of the report.

.. image:: static/description/unfold_button.png

PDF Version
-----------
You may print or doaload a PDF version of the report by clicking on the `PRINT` button
in the control panel of the report.

.. image:: static/description/print_button.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
