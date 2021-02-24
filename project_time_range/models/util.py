# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import threading
import functools


def time_range_constraint(method):
    @functools.wraps(method)
    def wrapper(self):
        if self._context.get("enable_task_max_hours_constraint") or getattr(
            threading.currentThread(), "testing", False
        ):
            for task in self:
                method(task)

    return wrapper
