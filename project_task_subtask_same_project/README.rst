Project Task Subtask Same Project  
=================================  
Ensure that subtasks always belong to the same project as their parent task.  

Starting from **Odoo v16**, a new feature allows subtasks to belong to one project  
while being displayed under a different project using the `display_project_id` field.  

This module **disables this behavior**, ensuring that tasks and their subtasks  
are always under the same project **both in data and display**.  

- **Subtasks remain in the same project as their parent task.**  
- When attempting to assign a subtask to a task from a different project,  
  an **error message** is displayed.  

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_task_subtask_same_project/static/description/subtask_in_different_project.png  

- In the subtask form view, the **display_project** field is **readonly**.  
- The value is automatically propagated from the parent task.  
- When changing the **project** on a parent task, both the `project_id`  
  and `display_project_id` fields are automatically updated on all its subtasks. 

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_task_subtask_same_project/static/description/subtask_project_readonly.png  

Contributors  
------------  
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)  
