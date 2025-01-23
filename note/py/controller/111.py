from datetime import datetime
# from odoo.tools import date_utils
from odoo import fields


dt = datetime(2023, 5, 15, 14, 30)  # 15/5/2023, 14:30
result = fields.Date.end_of(dt, "hour")
# result = date_utils.end_of(dt, "hour")
print(result)  # Output: 2023-05-15 14:59:59.999999
