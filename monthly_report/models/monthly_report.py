# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
import calendar


class monthly_report(models.Model):
    _name = 'monthly.report'
    _inherit = ['mail.thread']
    _description = 'monthly.report'


    def send_mail(self):
        template = self.env['mail.template'].browse(self.env.ref('monthly_report.mail_template_monthly_report').id)
        if template:
            accountant_group = self.env.ref('purchase_extension.group_accountant')
            users = accountant_group.users
            for user in users:
                email_values = {
                    'auto_delete': True,
                    'email_to': user.email,
                }
                try:
                    template.sudo().send_mail(1, force_send=True, raise_exception=True, email_values=email_values)
                except Exception as e:
                    print(e)
        else:
            raise UserError("Mail Template not found. Please check the template.")




