Project Invocing Profile
========================
This module allows users to be able to know the typology of projects :
- Analyze and break down time spent by type of project
- Identify the times to be re-invoiced and under what structure, both for customers and for inter-company invoicing.

Usage
-----
*Configuration*
As a user of the Administration / Configuration group, from the Technical menu, I find the submenu: Technical / Parameters.
Then after activating in the user profile form view, in the Other section: `Project invoicing profile`.
Now, I can have view the new submenu : `Technical / Parameters / Project invoicing profile`.

When I click on the menu entry, I arrive at a non-editable list which offers the Name field.

If I click on the [Create] button, I arrive at a form view allowing me to create, modify and delete records.
The form view displays the following fields:
- Name
- Description

There is no possibility of archiving. 
This is to prevent data from being archived even though it is defined on projects, tasks and timesheets. 
If the administrator wishes to change the data, he will either have to modify an existing record, 
or modify by batch editing to reassign the values ​​to the projects before deleting a billing profile.

It is impossible for a user to delete data if it is set on a record linked via a many2one field.

*Access right*
A new access group is created `Project invoicing profile`.

A new extended security rule is added through the module, and restricts the modification of the field on the project form to the 'Project billing profiles' group only.

*Use case*
As a user of the `Project invoicing profile` group, from the project form, in the tab:

From the list of tasks and timelines, I can group by `Invoicing profile`. 
The task and timeline field is a related field, based on the project. 
It is not editable or visible in list and form views. 
It is simply stored in the database and available for group, filter, or export.


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
