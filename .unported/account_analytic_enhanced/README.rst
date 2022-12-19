Account Analytic Enhanced
=========================

.. contents:: Table of Contents

Technical
---------
Add a new active_toggle boolean field for analytic account, default value is True.
When the Active/Archived button is checked, the field has its value defined with the value of field active given by the button.
Set field active_toggle to True in the function "write" to work around.

Description
-----------

If an analytic account was deactivated manually using button in its form view,
it will stay deactivated using coding write operation if field active_toggle is set to False.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
