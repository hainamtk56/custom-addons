# https://claude.ai/chat/b7bce5dc-f936-450f-ac37-db1dbc54fc0c
from datetime import date, datetime, timedelta

from odoo import fields


class MyModel(models.Model):
    _name = 'my.model'

    # Trường date chỉ lưu ngày
    date_field = fields.Date(string='Ngày')

    # Trường datetime lưu cả ngày và giờ
    datetime_field = fields.Datetime(string='Ngày giờ')

    now = datetime.now()

    # Định dạng thời gian theo nhiều cách khác nhau
    formatted_date = now.strftime('%Y-%m-%d')  # Ví dụ: 2024-01-20
    formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')  # Ví dụ: 2024-01-20 15:30:45
    formatted_custom = now.strftime('%d/%m/%Y')  # Ví dụ: 20/01/2024

    # Định dạng với tên tháng, ngày
    full_date = now.strftime('%B %d, %Y')  # Ví dụ: January 20, 2024
    short_date = now.strftime('%b %d, %Y')  # Ví dụ: Jan 20, 2024

    def handle_dates(self):
        # Lấy ngày hiện tại
        today = date.today()

        # Lấy thời gian hiện tại (có cả giờ phút giây)
        now = datetime.now()

        # Lấy thời gian hiện tại theo múi giờ UTC
        utc_now = datetime.utcnow()

        # Thêm/bớt ngày
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        # Thêm/bớt giờ
        next_hour = now + timedelta(hours=1)
        last_hour = now - timedelta(hours=1)

    def convert_dates(self):
        # Chuyển string thành date
        date_str = '2024-01-20'
        date_obj = fields.Date.from_string(date_str)

        # Chuyển date thành string
        date_str_again = fields.Date.to_string(date_obj)

        # Chuyển string thành datetime
        datetime_str = '2024-01-20 15:30:00'
        datetime_obj = fields.Datetime.from_string(datetime_str)

        # Chuyển datetime thành string
        datetime_str_again = fields.Datetime.to_string(datetime_obj)
