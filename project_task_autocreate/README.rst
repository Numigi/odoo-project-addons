.. image:: https://img.shields.io/badge/License-LGPLv3-blue.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

===============================================================
Automated Task Creation - Rule-based task creation on any model
===============================================================

This module implements configurable, rule-based creation of tasks.
The tasks are created from templates, which support python-style formatting
in selected fields to access fields on the source record.
The creation rules are tied to events (write, delete, create or status changes)
on chosen models.
Creation rules can be configured to have any number of conditions (filters).


Usage
=====

For example, let's say we want to automatically create a task whenever a
sale order for a total of more than $10,000 is confirmed.

- Rules are configured in Project / Configuration / Task Creation Rules. Create
  a rule for the Sale Order model, on status Sale Order.

- Add the condition that the Total is greater than $10,000.

- Task templates are configured in Project / Configuration / Task Templates.
  Create a task template tied to our new rule with a title, description, etc.

- For example, give it the title 'Verify Large Sale Order {object.name}'.
  Python formatting can be used in template titles and descriptions to access
  record fields - the active record is available as 'object'.

Now, whenever a Quotation for a total greater than $10,000 is confirmed,
a task will be created.


Configuration
=============

To modify which fields are copied from templates to tasks, the method
`get_fields_to_copy` on `project.task.template` can be overriden or extended.

To modify which models can be tied to task templates, the method
`get_model_selection` on `project.task.template` can be overriden or extended.


Contributors
------------
* Jérome Boisvert-Chouinard (jerome.boisvertchouinard@savoirfairelinux.com)


More information
----------------
* Module developed and tested with Odoo version 10.0
* For questions, please contact our support services
(support@savoirfairelinux.com)
