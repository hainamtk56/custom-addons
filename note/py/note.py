@api.model
def default_get(self, fields):
    # Chạy khi mở form tạo mới, lấy giá trị mặc định cho các trường trong form
    defaults = super(SaleOrderCustom, self).default_get(fields_list)

    # Thiết lập giá trị mặc định cho các trường cụ thể
    if 'date_order' in fields_list:
        defaults['date_order'] = datetime.now()

    if 'user_id' in fields_list:
        defaults['user_id'] = self.env.user.id

    if 'company_id' in fields_list:
        defaults['company_id'] = self.env.company.id

    # Thiết lập giá trị mặc định dựa trên ngữ cảnh (context)
    if 'priority' in fields_list:
        # Lấy giá trị từ context nếu có
        priority = self.env.context.get('default_priority', '1')
        defaults['priority'] = priority

    # Thiết lập giá trị mặc định có điều kiện
    if 'partner_id' in fields_list:
        # Ví dụ: nếu user thuộc nhóm sales manager
        if self.env.user.has_group('sales_team.group_sale_manager'):
            # Lấy partner được chỉ định làm mặc định cho sales manager
            default_partner = self.env['res.partner'].search(
                [('is_company', '=', True)], limit=1)
            defaults['partner_id'] = default_partner.id

    # Thiết lập sequence cho trường name
    if 'name' in fields_list and not defaults.get('name'):
        defaults['name'] = self.env['ir.sequence'].next_by_code(
            'sale.order.custom')

    return defaults


dùng @ api.model_create_multi


def create thay @ api.model


def create


record = self.env['model.name'].browse(record_id)
data = self.env['model.name'].search([]).read(['field1', 'field2'])

self.env['model.name'].browse(ids).read(['field1', 'field2'])

records = self.env['model.name'].sudo().search([('field', '=', value)])

results = self.env['model.name'].search_read(
    domain=[('field', '=', value)],
    fields=['field1', 'field2'],
    limit=10
)

# Không nên
for record in records:
    record.write({'state': 'done'})
# Nên dùng
records.write({'state': 'done'})

# Không nên
total = 0
for line in order.order_line:
    if line.product_id.type == 'service':
        total += line.price_subtotal

# Nên dùng
total = sum(order.order_line.filtered(lambda l: l.product_id.type == 'service').mapped('price_subtotal'))

toán tử child_of trong domain lấy tất cả bản ghi many2one trực tiếp hoặc gián tiếp đến giá trị id
toán tử parent_of lấy tất cả bản ghi one2many trực tiếp hoặc gián tiếp đến giá trị id