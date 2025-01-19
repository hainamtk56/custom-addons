# -*- coding: utf-8 -*-
# from odoo import http


# class MinStockCheck(http.Controller):
#     @http.route('/min_stock_check/min_stock_check', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/min_stock_check/min_stock_check/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('min_stock_check.listing', {
#             'root': '/min_stock_check/min_stock_check',
#             'objects': http.request.env['min_stock_check.min_stock_check'].search([]),
#         })

#     @http.route('/min_stock_check/min_stock_check/objects/<model("min_stock_check.min_stock_check"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('min_stock_check.object', {
#             'object': obj
#         })

