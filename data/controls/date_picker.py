from datetime import datetime, date

from data.controls.base_time_picker import BaseTimePicker

MAX_YEAR = 9999
MAX_MONTH = 12
MAX_DAY = 31


class DatePicker(BaseTimePicker):
    MAX_FIRST_VALUE = MAX_YEAR
    MAX_SECOND_VALUE = MAX_MONTH
    MAX_THIRD_VALUE = MAX_DAY

    def __init__(self, inital_time: datetime):
        super().__init__(inital_time, "Date:", self._time_factory, first_field_width=70)

        self.current_time = inital_time.date()

    def update_fields_value(self):
        self.first_field.value = str(self.current_time.year)
        self.second_field.value = str(self.current_time.month)
        self.third_field.value = str(self.current_time.day)

    def _time_factory(self, year: int, month: int, day: int):
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1
            self.second_field.value = str(day)

        return self._time_factory(year, month, day)

    def get(self) -> date:
        self.check_fields_value()
        return self.current_time
    