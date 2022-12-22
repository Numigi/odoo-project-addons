Project Material
================
This module enables to consume material (products) on a task.

.. contents:: Table of Contents

Warehouse Configuration
-----------------------
As member of the group ``Stock / Manager``, I go to the form view of my warehouse.

In the ``Warehouse Configuration`` tab, I see a field ``Consumption``.

.. image:: static/description/warehouse_form.png

I let the default option ``Direct Consumption From Stocks (1 step)``.

One route is created automatically by the system for the material consumption.

.. image:: static/description/consumption_route.png

Task Material Tab
-----------------
As member of the group ``Project / User``, I go to the form view of a task.

I see a ``Material`` containing a table of products to consume for this task.

.. image:: static/description/task_material_tab.png

I can only select stockable or consumable products.

I add the products required for the task, then I click on ``Save``.

.. image:: static/description/task_material_tab_with_products.png

Because I did not fill the field ``Planned Date``, the following error message appears.

.. image:: static/description/task_planned_date_error_message.png

I fill the ``Planned Date`` field, then I click on ``Save``.

.. image:: static/description/task_with_planned_date.png

After saving, a new smart button ``Stock Pickings`` appears.

.. image:: static/description/task_stock_picking_smart_button.png

Consumption Stock Picking
-------------------------
After clicking on the button, I see the form view of a stock picking.

.. image:: static/description/stock_picking_form.png

* The project and task were propagated to the picking.
* The planned date from the task was propagatted to the scheduled date of the picking.

I validate the stock picking.

.. image:: static/description/stock_picking_form_done.png

Back to the task, I notice that the consumed quantities were updated.

.. image:: static/description/task_with_consumed_qty.png

Preparation Step
----------------
Since version ``1.1.0`` of the module, a ``Preparation`` step is introduced to the ``Consumption`` route.

To use this step, as ``Inventory / Manager``, I go to the form view of a warehouse.

I notice a new option ``Prepare the stock before consumption (2 steps)``.

.. image:: static/description/warehouse_form_2_steps.png

I select this option.

A new field ``Preparation Location`` appears.

..

    When selecting the 2 steps options, the preparation location is mandatory.

    However, if the warehouse was never created, no location exist for this warehouse.
    Therefore, the warehouse must be created (saved) before selecting the 2 steps option.

.. image:: static/description/warehouse_form_preparation_location.png

I create a new location for preparations.

.. image:: static/description/preparation_location_form.png

..

    The parent location must be another location under the warehouse.
    The location type must be ``Internal Location``.

Optionaly, you may select an existing stock location of your warehouse.

Preparation Types
~~~~~~~~~~~~~~~~~
When selecting the preparation step, 2 new types of operations are added to the warehouse:

* Preparations
* Preparation Returns

.. image:: static/description/preparation_picking_types.png

Task Material
~~~~~~~~~~~~~
When adding new material lines to a task, 2 pickings are generated:

(1) The preparation picking
(2) The consumption picking

.. image:: static/description/task_2_step_picking_smart_buttons.png

By clicking on ``Preparations``, I am redirected to the form view of the preparation picking.

.. image:: static/description/preparation_picking_form.png

If products are returned from the preparation step, a new smart button is added to show the ``Preparation Return Picking``:

.. image:: static/description/task_return_picking_smart_button.png

By clicking on ``Preparation Returns``, I am redirected to the form view of the return picking.

.. image:: static/description/preparation_return_picking_form.png

Material List View
------------------
Since version ``1.2.0`` of the module, a new list view of all task material is available.

.. image:: static/description/global_material_list_view.png

This list is available from both ``Inventory / Report`` and ``Project / Report`` menus.

It allows to add new material lines or modify the initial quantity on existing lines.

Deleting a Line
~~~~~~~~~~~~~~~
It however does not allow to delete a line.
If you need to delete material, you must go to the form view of the task and delete it.

Changing the Task
~~~~~~~~~~~~~~~~~
The task and project on an existing line are not modifiable.

If you need to change the task of a material line, you may delete it or set its quantity to zero.
Then, recreate it with the proper project and task.

Project Smart Button
~~~~~~~~~~~~~~~~~~~~
From the form view of a project, a smart button allows to access the material related to this project.

.. image:: static/description/project_material_smart_button.png

.. image:: static/description/project_material_list.png

Duplicating A Task
~~~~~~~~~~~~~~~~~~
When duplicating a task, material lines are also duplicated in the new task.

The field ``Planned Date`` is set to ``2099-01-01`` (a date far in the future).

Also, procurements are temporarily blocked.

.. image:: static/description/duplicated_task.png

When changing the project on the form view, the procurements are automatically enabled.

.. image:: static/description/duplicated_task_with_procurement_enabled.png

Otherwise, you may also uncheck the ``Procurement Disabled`` box manually.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
