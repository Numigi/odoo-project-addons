Project Enhanced
================

.. contents:: Table of Contents

Dependencies
------------

See Readme of module https://github.com/Numigi/odoo-account-addons/tree/12.0/account_analytic_enhanced

Technical
---------

Add a new active_toggle boolean field for projects and tasks, default value is True.
When the Active/Archived button is checked, the field has its value defined with the value of field active given by the button.
Set field active_toggle to True in the function "write" to work around.

Description
-----------

If a project was deactivated manually using button in its form view,
it will stay deactivated using coding write operation (field active_toggle in this case is set to False).
Same thing for a task

If a project is activated, so are the associated tasks, if the tasks have not been manually deactivated using the button in its form view.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
