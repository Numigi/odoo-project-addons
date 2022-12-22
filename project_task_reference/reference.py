# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from typing import Mapping


class TaskReference:

    def __init__(self, values: Mapping[str, str], string: str, format_: str):
        self.task = None
        self._string = string
        self._normalized_string = format_.format(**values)
        self._values = values
        self._task_id = int(values['id']) if 'id' in values else None

    def __str__(self):
        return self._string

    @property
    def string(self):
        return self._string

    @property
    def normalized_string(self):
        return self._normalized_string

    @property
    def values(self):
        return dict(self._values)

    @property
    def task_id(self):
        return self._task_id
