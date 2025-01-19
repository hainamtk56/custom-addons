# -*- coding: utf-8 -*-
# from odoo import http


# class SalesPlan(http.Controller):
#     @http.route('/sales_plan/sales_plan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_plan/sales_plan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_plan.listing', {
#             'root': '/sales_plan/sales_plan',
#             'objects': http.request.env['sales_plan.sales_plan'].search([]),
#         })

#     @http.route('/sales_plan/sales_plan/objects/<model("sales_plan.sales_plan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_plan.object', {
#             'object': obj
#         })

