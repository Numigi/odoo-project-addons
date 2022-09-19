Project Milestone Dependencies
==============================

.. contents:: Table of Contents

Description
-----------
This module allows to manage Milestone Dependencies.

Overview
--------
As a user who can manage Milestones, I open the form view of a Milestone, I notice a new tab ``Dependencies``.

.. image:: static/description/dependencies_tab_milestone_form.png

I also notice that the field ``Project Tasks`` is moved into a new tab ``Tasks``.

.. image:: static/description/tasks_tab_milestone_form.png

Usage
-----

As a user who can manage Milestones, I go to the form view of a Milestone and I click on ``Add line`` from the ``Dependencies`` tab:

.. image:: static/description/add_milestone_dependencies.png

I notice that the Milestones are filtered on the Project assigned on the current Milestone.

.. image:: static/description/milestones_filtered_by_current_project.png

It is impossible to have recursion on dependencies. If this is the case, a blocking message is displayed.

Example:
~~~~~~~~
- If ``Milestone 1`` depends of ``Milestone 2``

.. image:: static/description/Milestone-2_dependsOf_Milestone-1.png

- When user tries to add ``Milestone 2`` in ``Milestone 1`` dependencies, the blocking message is displayed.

.. image:: static/description/recursion_blocking_message.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
