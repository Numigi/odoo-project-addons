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

Cost Subdivisions (Categories)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The complete list of subdivision (categories) found in the report is available under ``Project / Configuration``.

.. image:: static/description/cost_category_list.png

Products
~~~~~~~~
This section contains analytic lines with stockable or consumable products.

It is subdivided into cost categories.

.. image:: static/description/report_section_products.png

These cost categories are defined on product categories.

.. image:: static/description/product_category_form.png

..

	The subdivision `Products` is a default category. It includes all products not bound to a specific cost category.

Time
~~~~
This section contains analytic lines from timesheets.

It is subdivided into cost categories.

.. image:: static/description/report_section_time.png

These categories are defined on task types (see module project_task_type from the same repository).

.. image:: static/description/task_type_form.png

..

	The subdivision `Labour` is a default category. It contains all timesheet lines not bound to a specific category.

Employee Column
***************
Since version 1.1.0 of the module, the ``Employee`` is shown in the ``Time`` section.

.. image:: static/description/report_employee_column.png

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

Target / Suggested / Profit
---------------------------
Since the version 1.3.0 of the module, 3 new columns are added to the report.

.. image:: static/description/report_summary_columns.png

These columns show respectively:

* the target sale margin
* the suggested sale price based on the target margin
* the profit based on the suggested sale price

Target Ratios
~~~~~~~~~~~~~
Under each sections (except TIME), the target is a margin ratio.

.. image:: static/description/product_section_target.png

This ratio is defined on the cost category.

.. image:: static/description/product_category_sale_ratio.png

Target Hourly Rate
~~~~~~~~~~~~~~~~~~
Under the TIME section, the target is an hourly rate.

.. image:: static/description/time_section_target.png

This hourly rate is defined on the cost category.

.. image:: static/description/time_category_hourly_rate.png

Since version 1.4.0 of the module, it is also possible to define a target in percentage
(instead of an hourly rate) for time categories.

.. image:: static/description/time_category_percentage_target.png

.. image:: static/description/report_with_time_percentage_target.png

Hide / Show Summary
~~~~~~~~~~~~~~~~~~~
The 3 columns Target / Suggested / Profit can be hidden by clicking on ``HIDE SUMMARY``

.. image:: static/description/hide_summary_button.png

They can be displayed again by clicking on ``SHOW SUMMARY``.

.. image:: static/description/show_summary_button.png

PDF Version
-----------
You may print or doaload a PDF version of the report by clicking on the `PRINT` button
in the control panel of the report.

.. image:: static/description/print_button.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
