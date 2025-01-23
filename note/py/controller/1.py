@route('/generic_controller', methods=['POST'], auth="public", website=True)
    def menu_generic_controller_request_submit(self, **kw):
        values = {}
        fields = request.env['ir.model'].sudo().search([('model', '=', kw.get('model'))]).field_id
        for key, val in kw.items():
            field_id = fields.sudo().filtered(lambda r: r.sudo().name == key).sudo()
            if not field_id:
                continue
            if field_id.ttype == 'many2one':
                val = int(val) if val else 0
            values.update({
                key: val
            })
        record = request.env[kw.get('model')].sudo().create(values)
        return request.render("website_form.generic_controller_form",{})


