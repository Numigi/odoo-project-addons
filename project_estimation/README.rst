Project Estimation
==================
This module defines an ``Estimation`` mode on projects.

.. contents:: Table of Contents

Smart Button
------------
A smart button is added on projects.

When a project is in ``Estimation`` mode, the button is blue.

.. image:: static/description/project_smart_button_blue.png

Otherwise, the button is gray.

.. image:: static/description/project_smart_button_blue.png

When I click on the button, a confirmation wizard is opened.
This wizard allows to either enter or exit the estimation mode.

.. image:: static/description/estimation_mode_exit_wizard.png

.. image:: static/description/estimation_mode_enter_wizard.png

Kanban View
-----------
In kanban view of projects, a blue badge is added on projects in estimation mode.

.. image:: static/description/project_kanban.png

Configuration
-------------
By default, when creating or duplicating a project, the new project is NOT in estimation mode.

This prevents the module from breaking unit tests on other modules.
The estimation mode can be used to alter behavior on projects
(see module project_estimation_material).

It you desire new projects to be created in estimation mode by default, you may
define the following system parameter:

..

	project_estimation_mode_active_default = True

.. image:: static/description/system_parameter.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
