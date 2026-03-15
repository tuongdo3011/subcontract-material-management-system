from odoo import models, fields, api

class SubcontractMaterialOrderLine(models.Model):
    _name = "subcontract.material.order.line"
    _description = "Chi tiết gia công nguyên vật liệu"
    
    subcontract_material_order_id = fields.Many2one("subcontract.material.order", string="Phiếu gia công")
    service_id = fields.Many2one("product.product", string="Dịch vụ gia công", domain=[('purchase_ok', '=', 'True'),('type', '=', 'service')])
    product_id = fields.Many2one("product.product", string="Sản phẩm", domain=[('is_subcontract_material', '=', 'True')])
    product_uom_id = fields.Many2one("uom.uom", string="Đơn vị tính")
    product_uom_qty = fields.Float(string="Số lượng")
    currency_id = fields.Many2one(related="subcontract_material_order_id.currency_id", string="Đơn vị tiền", store=True)
    price_unit = fields.Monetary(string="Đơn giá", currency_field="currency_id")
    price_subtotal = fields.Monetary(compute="_compute_price_subtotal", string="Thành tiền", currency_field="currency_id", store=True, readonly=True)

    @api.onchange('service_id')
    def _onchange_price_unit(self):
        if self.service_id:
            self.price_unit = self.service_id.standard_price

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for record in self:
            record.price_subtotal = record.price_unit * record.product_uom_qty