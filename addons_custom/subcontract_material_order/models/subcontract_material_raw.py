from odoo import models, fields, api

class SubcontractMaterialRaw(models.Model):
    _name = "subcontract.material.raw"
    _description = "Nguyên vật liệu"

    order_id = fields.Many2one("subcontract.material.order")
    product_domain_ids = fields.Many2many("product.product", compute="_compute_product_domain_ids")
    product_id = fields.Many2one("product.product", string="Sản phẩm")
    material_id = fields.Many2one("product.product", string="Nguyên vật liệu")
    qty_needed = fields.Float(string="Số lượng cần")
    qty_issued = fields.Float(string="Số lượng xuất", readonly=True)
    qty_returned = fields.Float(string="Số lượng nhận lại", readonly=True)

    @api.depends("order_id.line_ids.product_id")
    def _compute_product_domain_ids(self):
        for record in self:
            if record.order_id:
                record.product_domain_ids = record.order_id.line_ids.mapped('product_id')
            else:
                record.product_domain_ids = False

    _sql_constraints = [
        ('strictly_positive_qty_needed', 'CHECK(qty_needed > 0)', 'Số lượng cần phải lớn hơn 0'),
    ]
