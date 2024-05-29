import string
from pprint import pprint
from datetime import datetime


class ErrorHandler:
    def __init__(self):
        self.num_sym_lst = list(string.punctuation + string.digits + " ")
        self.let_sym_lst = list(string.punctuation + string.ascii_letters + " ")
        self.sym_lst = list(string.punctuation)
        self.current_date = datetime.now().date()
        self.days_in_months_leap_year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.days_in_months_leap_year = [(num + 1, self.days_in_months_leap_year[num]) for num in range(12)]

    def detect_invalid_char(self, lst, user_input):
        for char in lst:
            if char in user_input:
                return True

    def detect_invalid_month_day(self, birth_month, birth_day):
        if birth_month < 1 or birth_month > 12:
            return True
        elif birth_day < 1:
            return True

        for month_day in self.days_in_months_leap_year:
            month = month_day[0]
            total_days_in_month = month_day[1]
            if birth_month == month and birth_day > total_days_in_month:
                return True

    def detect_invalid_id_number(self, user_input):
        birth_month = int(user_input[2] + user_input[3])
        birth_day = int(user_input[4] + user_input[5])
        citizenship_status = int(user_input[10])

        if self.detect_invalid_month_day(birth_month, birth_day):
            return True
        elif citizenship_status != 0 and citizenship_status != 1:
            return True

    def detect_if_id_number_exists(self, id_numbers, id_number):
        if id_number in id_numbers:
            return True

    def detect_invalid_date(self, user_input):
        birth_date_lst = [int(data) for data in user_input.split("-")]
        current_date_lst = [int(data) for data in str(self.current_date).split("-")]
        if current_date_lst[0] - birth_date_lst[0] < 18:
            return True
        if self.detect_invalid_month_day(birth_date_lst[1], birth_date_lst[2]):
            return True

    def detect_id_date_match(self, id_no, dob):
        id_number_date = id_no[:6]
        date_of_birth = "".join(dob.split("-"))[2:]

        if id_number_date != date_of_birth:
            return True

