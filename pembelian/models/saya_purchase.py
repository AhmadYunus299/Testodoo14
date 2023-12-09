from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class saya_purchase(models.Model):
    _name = 'saya.purchase'

    def func_delete_status_draft(self):
        saya_purchase_obj = self.env['saya.purchase'].search([('status', '=', 'draft')])
        for line in saya_purchase_obj:
            line.unlink()
        return True

    def funct_approved(self):
        if self.status == 'draft':
            if self.name == 'New':
                seq =self.env['ir.sequence'].next_by_code('saya.purchase') or 'New'
                self.name = seq
            self.status = 'approve'

    def funct_set_to_done(self):
        if self.status == 'approve':
            self.status = 'done'

    @api.model
    def create(self, values):
        res = super(saya_purchase, self).create(values)
        for rec in res:
            tanggal_purchase = rec.tanggal
            tanggal_sekarang = date.today()
            if tanggal_purchase < tanggal_sekarang:
                raise ValidationError(_("Tangal Pembelian tidak boleh kurang dari tanggal sekarang"))
            return res
        
    def write(self, values):
        res = super(saya_purchase, self).write(values)
        if 'tanggal' in values:
            tanggal_purchase = self.tanggal
            tanggal_sekarang = date.today()
            if tanggal_purchase < tanggal_sekarang:
                raise ValidationError(_("Tangal Pembelian tidak boleh kurang dari tanggal sekarang"))
        return res


    name = fields.Char(string='Name', default='New')
    tanggal = fields.Date(string='Tanggal')
    status = fields.Selection([('draft', 'Draft'),('approve', 'Approve'),('done', 'Done')], default='draft')
    saya_purchase_ids = fields.One2many('saya.purchase.line', 'saya_purchase_id', string="Saya Purchase Ids")
    brand_ids = fields.Many2many('saya.brand', 'saya_purchase_brand_rel', 'saya_purchase_id', 'brand_id', string="Brand Ids")

class saya_purchase_line(models.Model):
    _name = 'saya.purchase.line'

    @api.onchange('product_id')
    def funct_onchange_product_id(self):
        if self.product_id:
            self.description = 'Desc - ' + self.product_id.name
            # return{}
        # else:
        #     self.description = 'Desc - ' + self.product_id.name
        # return {}
    
    def _fuction_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price

    saya_purchase_id = fields.Many2one('saya.purchase', string="Saya Purchase Id")
    product_id = fields.Many2one('product.product', string="Produk Id")
    quantity = fields.Float(string="Quantity", default=0)
    uom_id = fields.Many2one('uom.uom', string="Satuan")
    description = fields.Char(string="Description")
    price = fields.Float(string="Harga", default=0.0)
    subtotal = fields.Float(string="Sub Total", compute=_fuction_subtotal)


class saya_brand(models.Model):
    _name = 'saya.brand'

    name = fields.Char(string="name")

class saya_purchase_report_wizard(models.TransientModel):
    _name = 'saya.purchase.report.wizard'

    name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

class product_template(models.Model):
    _inherit = 'product.template'
    
    product_description = fields.Char(string="Product Description")
