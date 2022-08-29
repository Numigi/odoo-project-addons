Project Milestone Week Duration
===============================

.. contents:: Table of Contents

Description
-----------
This module adds a Duration field to milestone object.
It changes the ``Target Date`` field to ``End Date`` field calculated automatically by ``Start Date`` and ``Duration``

Overview
--------
I open the form view of a milestone, a new field is added ``Duration``.

.. image:: static/description/field_duration_form_view.png

The same field is added to the list view of a milestone.

.. image:: static/description/field_duration_list_view.png

From a project form view with ``Use Milestone`` egal a True, I see the field ``Duration`` added to Milestones Tab lines.

.. image:: static/description/field_duration_milestone_project_form.png

The field ``End Date`` became Readonly and calculated automatically by the system:
1- Select a ``Start Date``;
2- Add a ``Duration`` (number of weeks);
3- The ``End Date`` is calculated automatically.

.. image:: static/description/field_duration_calculation.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com