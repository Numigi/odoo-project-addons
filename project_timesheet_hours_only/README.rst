============================
Project Timesheet Hours Only
============================

.. ![]https://img.shields.io/badge/licence-AGPL--3-blue.png)
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

Context
=======
On mixed projects involving both labor (timesheets) and material tracking, Odoo's standard project dashboard aggregates all analytic lines under the "Recorded Hours" smart button. This leads to inaccurate totals since material consumption quantities (often recorded with negative or distinct values) are mixed with actual work hours.

Description
===========
This module fixes the project's "Recorded Hours" smart button and its corresponding list view to exclusively display and calculate actual labor hours. It filters out material consumption lines by ensuring that only analytic lines linked to a specific task (``task_id != False``) are included.

Usage
=====
1. Navigate to the **Project** app.
2. Open any project that contains both timesheets and material consumption lines.
3. The counter on the **Recorded Hours** smart button now strictly shows the total labor hours.
4. Clicking the smart button will only list actual timesheet entries, excluding material logs.

.. note::
   Material consumption remains fully traceable and searchable via **Project > Reporting > Material** (filtering by project and grouping as needed).

Installation
============
No data migration or historical recalculation is strictly required, as the change applies dynamically to the compute method and window action domain.

Credits
=======

Authors
-------
* Numigi

Maintainers
-----------
This module is maintained by Numigi.
