Project Task Reference Extract
==============================
This is a technical module. It has no functional use on its own.

It allows to extract a reference to a task from a string.

.. contents:: Table of Contents

Basic Usage
-----------
The module adds a method ``_search_references_from_text`` on ``project.task``.

This method takes a string and returns a list of TaskReference (a python class defined in the module).

.. code-block:: python

    from odoo.addons.project_task_reference.reference import TaskReference

    some_text = "ta#123 Some commit message"
    reference = env['project.task']._search_references_from_text(some_text)[0]
    assert isinstance(reference, TaskReference)
    assert reference.task == env['project.task'].browse(123)
    assert reference.string == "ta#123"
    assert reference.normalized_string == "TA#123"

The reference(s) can be located anywhere in the given text.

The method is at some point tolerant to variations in the format of the reference inside the given text.

* It is insensitive to lower case.
* The ``#`` is optional.

Thefore ``ta123`` would be recognized.

Advanced Setup
--------------
By default, the system uses the following regex to parse the references:

..

    [tT][aA]#?(?P<id>\d+)

This means that the strings ``TA#123``, ``ta#123``, ``TA123`` or ``ta123``
will generate a reference that point to the task with ID=123.

Then, the following python format is used to render the reference in a normalized form:

..

    TA#{id}

The reference will always be formatted ``TA#123``.

This can be tweeked by defining 2 system parameters:

* ``project_task_reference.regex``: the REGEX used to parse the reference.
* ``project_task_reference.format``: the python format to use for formatting the reference.

For example, let's suppose the format for our links must be: ``[ST#123]``.
The system parameters could be as follow:

* ``project_task_reference.regex``: ``\[?[sS][tT]#?(?P<id>\d+)\]?``
* ``project_task_reference.format``: ``[ST#{id}]``

The regex must contain a parameter ``(?P<id>\d+)`` (the database ID of the task).

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
