Project Worksheet
=================
This module allows you to manage field worksheets for project interventions.

A worksheet groups the hours worked on a project over a weekly period. Once completed,
it can be sent to the client through the portal for approval, or approved internally by
a manager. When a worksheet is processed, the corresponding timesheets are generated
automatically and locked.

This module depends on the modules ``project``, ``hr_timesheet`` and
``project_stage_allow_timesheet``.

.. contents:: Table of Contents

Usage
-----

Creating a worksheet
~~~~~~~~~~~~~~~~~~~~~~

From the `Worksheets` menu, create a new worksheet and select a project and a
supervisor. Choose the period (start and end dates); the period must fall within the
same calendar week (Monday to Sunday).

Add worksheet lines with the date, employee, task and number of hours. The date of each
line must be within the worksheet period. The total hours are computed automatically.

.. image:: static/description/worksheet.png

Submitting for approval
~~~~~~~~~~~~~~~~~~~~~~~~~

A worksheet follows this workflow:

- **New**: the worksheet is a draft. It can be edited and is the only state in which it
  can be deleted.
- **Open**: the worksheet is validated internally. Lines and a total of hours greater
  than zero are required. Timesheets are generated.
- **Pending Approval**: the worksheet has been sent to the client for approval.
- **Confirmed**: the worksheet has been approved by the client or by a manager.

When you send a worksheet to the client, an email with a secure portal link is sent. The
client can review the worksheet online and approve it by checking the confirmation box.

A worksheet can also be approved internally by a user in the `Manager` group.

Reminders
~~~~~~~~~

A scheduled action runs once a day and creates a follow-up activity on worksheets that
have been pending for longer than the configured reminder delay.

Configuration
-------------

In `Settings`, under the Project Worksheet section (per company), you can set:

- **Worksheet Approval Delay (Days)**: number of days before a manager can force the
  approval.
- **Worksheet Reminder Delay (Days)**: number of days after sending before a reminder
  activity is created.

Security
--------

Two groups are provided:

- **User**: can create and edit worksheets, and only sees the worksheets for which they
  are the supervisor or the supervisor's manager.
- **Manager**: has full access, including deletion, and sees all worksheets.

Contributors
------------

The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.
