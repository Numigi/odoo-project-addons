Project Milestone Timeline Color
================================

This module displays milestones in the color assigned to the milestone type.

.. contents:: Table of Contents

Context
-------
The module `project_milestone_type <https://github.com/Numigi/odoo-project-addons/tree/12.0/project_milestone_type>`_
allows to define ``Types`` for a Project Milestone.


Configuration
--------
As a member of the group ``Projects / Manager``, I go to the Form View of Milestone Types.

I see that a new ``HTML Color`` field is available and that it has the following default value : ``#FFFFFF``.

.. image:: static/description/field_html_color_form_view.png

When I click in the field, I see that I can select a color thanks to the ``Widget Color``.

.. image:: static/description/widget_color.png

From the Milestone Types List View, I see that the new ``HTML Color`` field is available and that a preview of the color is also displayed.

.. image:: static/description/field_html_color_list_view.png


Usage
--------

As a user who can view milestones, I go to the Milestones Timeline View.

I see that the milestones are displayed in the color assigned to the type of the milestone.

.. image:: static/description/milestones_timeline_colors.png


If `no color is defined` on the type of milestone associated to the milestone,
the milestone is displayed in white (#FFFFFF) in the ``Timeline View``.

In case `the milestone is not associated with a milestone type` or if `the milestone is associated with an inactive milestone type`,
the milestone is displayed in white (#FFFFFF) in the ``Timeline View``.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
