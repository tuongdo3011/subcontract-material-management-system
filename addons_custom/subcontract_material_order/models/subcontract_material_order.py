from odoo import fields, models, api
from odoo import exceptions

class SubcontractMaterialOrder(models.Model):
    _name = "subcontract.material.order"
    _description = "Phiếu gia công nguyên vật liệu"

    name = fields.Char(string="Số phiếu", readonly=True)
    subcontractor_id = fields.Many2one("res.partner", string="Đơn vị gia công")
    person_in_charge_id = fields.Many2one("res.users",string="Người phụ trách", default=lambda self:self.env.user)
    finished_warehouse_id = fields.Many2one("stock.warehouse", string="Kho thành phẩm")
    raw_material_warehouse_id = fields.Many2one("stock.warehouse", string="Kho nguyên vật liệu", domain=[('is_material_warehouse', '=', 'True')])
    date_order = fields.Date(string="Ngày tạo phiếu", default=fields.Date.today)
    expected_date = fields.Date(string="Ngày dự kiến")
    date_finished = fields.Date(string="Ngày hoàn thành", readonly=True)
    currency_id = fields.Many2one("res.currency", string="Đơn vị tiền")
    amount_total = fields.Monetary(compute="_compute_amount_total", string="Tổng tiền", currency_field="currency_id", store=True)
    reason = fields.Text(string="Lý do từ chối")
    line_ids = fields.One2many("subcontract.material.order.line", "subcontract_material_order_id")
    finished_line_ids = fields.One2many("subcontract.material.finished", "order_id", readonly=True)
    raw_line_ids = fields.One2many("subcontract.material.raw", "order_id")
    history_ids = fields.One2many("subcontract.material.history", "order_id")
    state = fields.Selection(
        selection = [
            ("draft", "Nháp"),
            ("confirmed", "Đơn gia công"),
            ("to_approve_mgr", "Chờ TPMH duyệt"),
            ("to_approve_cfo", "Chờ GĐTC duyệt"),
            ("to_approve_ceo", "Chờ TGĐ duyệt"),
            ("in_progress", "Đang gia công"),
            ("done", "Hoàn thành"), 
            ("rejected", "Từ chối"),
            ("canceled", "Hủy"),
        ],
        default="draft"
    )
    finished_status = fields.Selection(
        selection=[
            ("not_received","Chưa nhập TP"),
            ("partial","Đã nhập một phần"),
            ("done","Đã nhập đủ"),
        ],
        string="Trạng thái nhập TP", default=False, readonly=True
    )
    raw_material_status = fields.Selection(
        selection=[
            ("not_sent","Chưa xuất NVL"),
            ("partial","Đã xuất một phần"),
            ("done","Đã xuất đủ"),
        ],
        string="Trạng thái xuất NVL", default=False, readonly=True
    )

    @api.depends('line_ids.price_subtotal')
    def _compute_amount_total(self):
        """Tự động tính: Tổng tiền = tổng giá trị các đơn hàng trong bảng Chi tiết gia công nguyên vật liệu"""
        for order in self:
            order.amount_total = sum(order.line_ids.mapped('price_subtotal'))
    

    def action_create_order(self):
        """Chuyển trạng thái từ Nháp sang Đơn gia công khi ấn nút Lập đơn"""
        for record in self:
            record.state = "confirmed"

        """Truyền dữ liệu từ tab Chi tiết sang tab Thành phẩm khi ấn nút Lập đơn"""
        finished_data = [(5,0,0)]
        for line in self.line_ids:
            finished_data.append((0, 0, {
                'product_id': line.product_id.id,
                'qty': line.product_uom_qty,
            }))
        self.write({'finished_line_ids': finished_data})

        """Báo lỗi nếu không có dòng Nguyên vật liệu nào"""
        for record in self:
            if not record.raw_line_ids.material_id:
                raise exceptions.UserError("Bạn chưa nhập Nguyên vật liệu")

    def action_approve(self):
        """Chuyển trạng thái từ Đơn gia công sang Chờ TPMH duyệt khi ấn nút Gửi duyệt"""
        for record in self:
            record.state = "to_approve_mgr"
            
    def action_draft(self):
        """Chuyển trạng thái từ Đơn gia công về Nháp khi ấn nút Quay lại nháp"""
        for record in self:
            record.state = "draft"
    
    def action_approve_mgr(self):
        """Tại trạng thái Chờ TPMH duyệt, khi ấn nút Phê duyệt, Chuyển trạng thái sang Chờ GĐTC duyệt nếu tổng tiền > 1000$, nếu không chuyển sang Đang gia công"""
        for record in self:
            if record.amount_total > 1000:
                record.state = "to_approve_cfo"
            else:
                record.state = "in_progress"

    def action_refuse_mgr(self):
        """Hiển thị pop up Lý do từ chối phê duyệt khi ấn nút từ chối trong trạng thái Chờ TPMH duyệt"""
        return {
            'name': 'Lý do từ chối phê duyệt',
            'type': 'ir.actions.act_window',
            'res_model': 'subcontract.material.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }

    def action_approve_cfo(self):
        """Tại trạng thái Chờ CĐTC duyệt, khi ấn nút Phê duyệt, Chuyển trạng thái sang Chờ TGĐ duyệt nếu tổng tiền > 2500$, nếu không chuyển sang Đang gia công"""
        for record in self:
            if record.amount_total > 2500:
                record.state = "to_approve_ceo"
            else:
                record.state = "in_progress"

    def action_refuse_cfo(self):
        """Hiển thị pop up Lý do từ chối phê duyệt khi ấn nút từ chối trong trạng thái Chờ GĐTC duyệt"""
        return {
            'name': 'Lý do từ chối phê duyệt',
            'type': 'ir.actions.act_window',
            'res_model': 'subcontract.material.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }
    
    def action_approve_ceo(self):
        """Tại trạng thái Chờ TGĐ duyệt, khi ấn nút Phê duyệt, Chuyển trạng thái sang Đang gia công,
        đồng thời chuyển Trạng thái nhập TP thành Chưa nhập TP, chuyển Trạng thái xuất NVL thành Chưa xuất NVL"""
        for record in self:
            record.state = "in_progress"
            record.finished_status = "not_received"
            record.raw_material_status = "not_sent"

    def action_refuse_ceo(self):
        """Hiển thị pop up Lý do từ chối phê duyệt khi ấn nút từ chối trong trạng thái Chờ TGĐ duyệt"""
        return {
            'name': 'Lý do từ chối phê duyệt',
            'type': 'ir.actions.act_window',
            'res_model': 'subcontract.material.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }
        
    @api.model_create_multi
    def create(self, vals_list):
        """Tạo sequence cho trường name"""
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('subcontract.material.odrer')
        return super(SubcontractMaterialOrder, self).create(vals)
    
    _sql_constraints = [
        ('check_expected_date', 'CHECK(expected_date >=date_order)', 'Ngày dự kiến không được nhỏ hơn Ngày tạo phiếu')
    ]