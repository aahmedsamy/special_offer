from datetime import datetime, timedelta, date


class Date:

    def calculate_remaining_days(start, end):
        start_year = start.year
        start_month = start.month
        start_day = start.day
        end_date = end
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        days = (date(end_year, end_month, end_day) -
                date(start_year, start_month, start_day)).days
        return days
