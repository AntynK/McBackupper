from typing import Callable
from datetime import datetime

import flet as ft


class BaseTimePicker(ft.Row):
    MAX_FIRST_VALUE = 23
    MAX_SECOND_VALUE = 59
    MAX_THIRD_VALUE = 59

    def __init__(
        self,
        curr_time: datetime,
        label: str,
        time_factory: Callable,
        first_field_width: int = 50,
        second_field_width: int = 50,
        third_field_width: int = 50,
    ):
        super().__init__(expand=True)

        self.current_time = curr_time
        self.time_factory = time_factory

        self.first_field = ft.TextField(
            width=first_field_width, on_submit=self.check_fields_value
        )
        self.second_field = ft.TextField(
            width=second_field_width,
            on_submit=self.check_fields_value,
        )
        self.third_field = ft.TextField(
            width=third_field_width, on_submit=self.check_fields_value
        )

        self.controls = [
            ft.Text(label),
            self.first_field,
            self.second_field,
            self.third_field,
        ]
        self.update_fields_value()

    def update_fields_value(self):
        raise NotImplementedError("Method 'update_fields_value' must be implemented.")

    def check_fields_value(self, event=None):
        self.current_time = self.time_factory(*self._get_fields_value())

        self.update_fields_value()
        self.update()

    def _get_fields_value(self) -> tuple[int, int, int]:
        first = 1
        second = 1
        third = 1

        str_first = self.first_field.value
        if str_first and str_first.isnumeric():
            first = int(str_first)

        str_second = self.second_field.value
        if str_second and str_second.isnumeric():
            second = int(str_second)

        str_third = self.third_field.value
        if str_third and str_third.isnumeric():
            third = int(str_third)

        return self._validate_date(first, second, third)

    def _validate_date(
        self, first: int, second: int, third: int
    ) -> tuple[int, int, int]:
        if first < 0:
            first = 1
        elif first > self.MAX_FIRST_VALUE:
            first = self.MAX_FIRST_VALUE

        if second < 0:
            second = 1
        elif second > self.MAX_SECOND_VALUE:
            second = self.MAX_SECOND_VALUE

        if third < 0:
            third = 1
        elif third > self.MAX_THIRD_VALUE:
            third = self.MAX_THIRD_VALUE

        return first, second, third
