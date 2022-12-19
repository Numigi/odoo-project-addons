Project Outsourcing Timesheet Automation
========================================

This module allows to generate subcontracting time entries automatically.

.. contents:: Table of Contents

Description
-----------

* The module allows to re-imput the subcontracting times automatically, or not to do so, depending on the article, task status, purchase status and vendor.
* The module adds **Subcontracting** section in product form view and **Subcontracting - Automate Time Entries** checkbox.
* The module adds 2 fields in vendor form view, Purchase section:

    - Subcontracting - Automate Time Entries (checkbox).
    - Employee for Time Entries (required if first field is checked).
  This employee is used to create the timesheet.
* The module allows to manage Subcontracting Automation Datas from the parent company for all associated contacts.
* The module adds new field in task status (**Create Subcontractors Time Entries**).
* When the task passes to a status in which the box **Create Subcontractors Time Entries** is checked, the system verifies following conditions to create time entries automatically:

  - The subcontracting PO is in `Purchase Order` or `Done` status.
  - The PO Vendor has the box **Subcontracting - Automate Time Entries** checked
  - The article selected in the PO has the box **Subcontracting - Automate Time Entries** checked.
  - The PO line has not already generated an automated time entry for this task.


Usage
-----

Create a service type product and go to `Purchase` tab then under the `Subcontracting` Section, check the box **Automate Time Entries**

    .. image:: static/description/product_automate_time_entries_checked.png

In a vendor form view, go to the `Sales & Purchases` tab and under `Purchase` section, check the box **Subcontracting - Automate Time Entries**.
A new field **Employee for Time Entries** is displayed, select an employee.
This employee is used to create the timesheet.

    .. image:: static/description/vendor_auomate_time_entries_checked.png

If a vendor is associated to a company, the Subcontracting Automation Datas are managed on the parent company.

    .. image:: static/description/subcontracting_auto_datas_managed_on_parent_company.png

    .. image:: static/description/parent_company_subcontracting_datas.png

As a user with Extra `Rights / Technical Features`, go to `Project > Configuration > Stages`.
Create a new stage and check **Create Subcontractors Time Entries** box.

    .. image:: static/description/stage_create_subcontracting_time_entries_checked.png

From a task, go to `Outsourcing > Purchase Orders` section, click on `New Po` button to create an outsourcing PO.

    .. image:: static/description/task_create_outsourcing_po.png

Select the vendor and the product previously created. Then confirm the PO.

    .. image:: static/description/created_po.png

Pass the task to `Client Test` status previously created, a new line will be created automatically in `Timesheets` tab.

    .. image:: static/description/task_with_timesheet_created_automatically.png

Create a second PO from the same task with previously created vendor and product. Then confirm the order.
Since the task is already in a status with `create subcontracting time entries` checked, a new timesheet will be created automatically from the PO.

    .. image:: static/description/task_with_timesheet_created_automatically_2.png

A note is added to the PO logs to inform that a time entry has been created automatically for the PO.

    .. image:: static/description/po_chatter_log_note.png


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
