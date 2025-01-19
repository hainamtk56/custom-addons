from odoo import models, fields, api


class Document(models.Model):
    _name = 'custom.document'
    _description = 'Custom Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên tài liệu',required=True)

    file = fields.Binary(
        string='File',
        attachment=False
    )
    file_name = fields.Char('Tên tệp')

    @api.model_create_multi
    def create(self, vals_list):
        documents = super().create(vals_list)

        for doc in documents:
            self.env['ir.attachment'].create({
                'name': doc.file_name,
                'datas': doc.file,
                'res_model': 'custom.document',
                'res_id': doc.id,
                'type': 'binary',
            })

        return documents

    @api.model
    def write(self, vals):
        documents = super().write(vals)
        for doc in self:
            if 'file' in vals:
                self.env['ir.attachment'].create({
                    'name': doc.file_name,
                    'datas': doc.file,
                    'res_model': 'custom.document',
                    'res_id': doc.id,
                    'type': 'binary',
                })

        return documents





