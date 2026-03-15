from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_subcontract_material = fields.Boolean("Là NVL gia công")