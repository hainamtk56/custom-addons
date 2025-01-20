from datetime import timedelta, date

from odoo import models, fields
from odoo.tools import float_compare


class Product(models.Model):
    _inherit = 'product.product'

    def _get_required_quantity_by_date(self, check_date):
        self.ensure_one()
        last_day_to_check = date.today() + timedelta(days=self.min_stock_qty_day)
        domain_do = [
            ('product_id', '=', self.id),
            ('picking_id.state', 'not in', ['done', 'cancel']),
            ('picking_code', '=', 'outgoing'),
            ('picking_id.scheduled_date', '>', check_date),
            ('picking_id.scheduled_date', '<=', last_day_to_check),
        ]
        domain_mo = [
            ('product_id', '=', self.id),
            ('raw_material_production_id.state', '!=', 'cancel'),
            ('raw_material_production_id.date_start', '>', check_date),
            ('raw_material_production_id.date_start', '<=', last_day_to_check),
        ]
        do_moves_qty = sum(self.env['stock.move'].search(domain_do).mapped('product_uom_qty'))
        mo_moves_qty = sum(self.env['stock.move'].search(domain_mo).mapped('product_uom_qty'))
        total_qty = do_moves_qty + mo_moves_qty

        return total_qty

    def _check_minimum_stock(self):
        today = fields.Date.today()
        products = self.search([('min_stock_qty_day', '>', 0)])
        for product in products:
            required_qty = product._get_required_quantity_by_date(today)
            on_hand_qty = product.qty_available
            if float_compare(on_hand_qty, required_qty, precision_rounding=product.uom_id.rounding) < 0:
                product._create_stock_warning_activity(
                    today,
                    required_qty,
                    on_hand_qty
                )
            else:
                product._mark_done_stock_activities(today)

        # dùng for để test
        # check_days = product.min_stock_qty_day
        #     for day in range(check_days):
        #         check_date = today + timedelta(days=day)
        #         required_qty = product._get_required_quantity_by_date(check_date)
        #
        #         on_hand_qty = product.qty_available
        #
        #         if float_compare(on_hand_qty, required_qty, precision_rounding=product.uom_id.rounding) < 0:
        #             product._create_stock_warning_activity(
        #                 check_date,
        #                 required_qty,
        #                 on_hand_qty
        #             )
        #         else:
        #             product._mark_done_stock_activities(check_date)


    def _create_stock_warning_activity(self, check_date, required_qty, on_hand_qty):
        self.ensure_one()
        activity_type_id = self.env.ref('mail.mail_activity_data_warning').id

        note = f"""
                    <p>The product's minimum stock level does not meet the requirements on {check_date.strftime('%d/%m/%Y')}:</p>
                    <ul>
                        <li>Required: {required_qty} {self.uom_id.name}</li>
                        <li>Available quantity: {on_hand_qty} {self.uom_id.name}</li>
                        <li>Additional quantity needed: {required_qty - on_hand_qty} {self.uom_id.name}</li>
                    </ul>
                """

        existing_activities = self.env['mail.activity'].search([
            ('res_id', '=', self.id),
            ('res_model', '=', 'product.product'),
            ('res_model_id', '=', self.env.ref('product.model_product_product').id),
            ('activity_type_id', '=', activity_type_id),
            ('date_deadline', '=', check_date)
        ])
        existing_activities.unlink()  # xóa activities trong chatter, ở discuss không bị xóa

        # Create new activity
        self.env['mail.activity'].create({
            'activity_type_id': activity_type_id,
            'note': note,
            'res_id': self.id,  # id bản ghi
            'res_model': 'product.product',  # tên kỹ thuật model
            'res_model_id': self.env.ref('product.model_product_product').id,  # id model
            'user_id': self.product_tmpl_id.responsible_id.id or self.env.user.id,  # assign to
            'date_deadline': check_date,
        })

    def _mark_done_stock_activities(self, check_date):
        activities = self.env['mail.activity'].search([
            ('res_id', '=', self.id),
            ('res_model', '=', 'product.product'),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_warning').id),
            ('date_deadline', '=', check_date)
        ])
        for activity in activities:
            activity.action_done()
