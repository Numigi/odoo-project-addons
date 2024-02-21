Project Material Direct Consumption
===================================
This module enables to consume products for a project directly from a stock picking.

.. contents:: Table of Contents

Context
-------
The module ``project_material`` allows to consume products on a task.
Then a stock picking is created and linked to the task.
This mecanism works similarly to a sales order.

However, sometimes, it is convenient to consume material without going to the whole process.

Module Design
-------------
Instead of adding a line of material on the task, which creates a stock picking,
this module allows to do the opposite.

When validated, a stock picking (of type ``Direct Consumption``) generates a material line on the task.

This material is separated into a distinct list inside the form view of a task.

.. image:: static/description/task_form_direct_consumption_list.png

Configuration
-------------
To use this module, a picking type (``Direct Consumption``) must be defined manually for each warehouse.

As member of ``Inventory / Administrator``, I create a new picking type from ``Inventory / Configuration / Operations Types``.
I select ``Consumption`` as type of operation and I check the box ``Direct Consumption``.

.. image:: static/description/picking_type_form_direct_consumption.png

As source location, I select the main stock location of my warehouse.
Make sure that you have ``Manage Multiple Stock Locations`` access.

As destination location, I select ``Virtual Locations / Production``.

.. image:: static/description/picking_type_form_locations.png

Usage
-----
As member of ``Inventory / User``, I create a new picking.

I select the type of operation ``Direct Consumption``.

I select my project and my task.

I select my product, the quantity and validate the picking.

.. image:: static/description/picking_form.png

.. image:: static/description/picking_form_done.png

In the form view of my task, I notice that the product was added to the list of consumed material.

.. image:: static/description/task_form_with_consumed_material.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)


More information
----------------
* Meet us at https://bit.ly/numigi-com
