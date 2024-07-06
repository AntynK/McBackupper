from datetime import datetime, time

from data.controls.base_time_picker import BaseTimePicker
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.CONTROLS)

MAX_HOUR = 23
MAX_MINUTE = 59
MAX_SECOND = 59


class TimePicker(BaseTimePicker):
    MAX_FIRST_VALUE = MAX_HOUR
    MAX_SECOND_VALUE = MAX_MINUTE
    MAX_THIRD_VALUE = MAX_SECOND

    def __init__(self, inital_time: datetime):
        super().__init__(inital_time, _("Time:"), time)

        self.current_time = inital_time.time()

    def update_fields_value(self):
        self.first_field.value = str(self.current_time.hour)
        self.second_field.value = str(self.current_time.minute)
        self.third_field.value = str(self.current_time.second)

    def get(self) -> time:
        self.check_fields_value()
        return self.current_time
