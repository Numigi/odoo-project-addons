# Project Task Invoicing

This modules adds a widget to generate invoices from the project form.

In the form of a project, a new tab 'Invoice Preparation' is added.
This tab contains the tasks related to the project and for each task, the list
of expense analytic lines related to it.

A button allows to generate an invoice from the selected expense lines.

## How to bind an analytic line to a task

The field task_id allows an analytic line to appear as an invoiceable line under this task.
However, this module does not prescribe how nor when this field is filled.
This must be implemented in another module specific to business logic.

## Partner To Invoice

The field Partner To Invoice is added. This field defines which partner should be used
when generating the invoice. Different lines on the same task may be invoiced to different
partners. In such case, one invoice is created per partner.

## Timesheet Entries

Timesheet entries appear in the widget as soon as the timesheet is confirmed by the manager.

In order to add the task_id field to the weekly timesheet widget, you may refer to
the OCA module hr_timesheet_task: https://github.com/OCA/hr-timesheet

## Known issues / Roadmap

This module is incompatible with timesheet_grid (from Odoo Enterprise modules).
The reason is that timesheet_grid has a very different behavior from the community
timesheet widget (module hr_timesheet_sheet).

Contributors
------------
* David Dufresne (david.dufresne@savoirfairelinux.com)

More information
----------------
* Module developed and tested with Odoo version 10.0
* For questions, please contact our support services
(support@savoirfairelinux.com)
