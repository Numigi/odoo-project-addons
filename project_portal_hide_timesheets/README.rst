Project Portal Hide Timesheets
==============================
This module completely hides timesheet information from portal users.

Features
--------
* Hides the timesheet lines from the task portal view
* Hides buttons that allow to print or download the timesheet lines
* Removes the `Timesheets` anchor link from the portal navigation
* Hides the `Time Spent` column from the task list view
* Blocks access to the `/my/timesheets` portal route
* Prevents timesheet report generation for portal users

Security
--------
This module provides both template-level (XML) and controller-level (Python) hiding:

* **Python controllers**: Block data at the source - timesheet data is never sent to the template
* **XML templates**: Additional layer to hide any remaining UI elements

Even with web editor access, portal users cannot view timesheet data as it's filtered at the controller level.

*Before installing the module*

.. image:: static/description/timesheets_lines_visible.png

*After installing the module*

.. image:: static/description/timesheets_lines_invisible.png


Contributors
------------
* Numigi (tm) and all its contributors (https://numigi.com/r/home)
