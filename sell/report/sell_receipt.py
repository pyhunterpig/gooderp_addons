# -*- coding: utf-8 -*-

import odoo.addons.decimal_precision as dp
from odoo import fields, models, api


class sell_receipt(models.TransientModel):
    _name = 'sell.receipt'
    _description = u'销售收款一览表'

    c_category_id = fields.Many2one('core.category', u'客户类别')
    partner_id = fields.Many2one('partner', u'客户')
    staff_id = fields.Many2one('staff', u'销售员')
    type = fields.Char(u'业务类别')
    date = fields.Date(u'单据日期')
    warehouse_id = fields.Many2one('warehouse', u'仓库')
    order_name = fields.Char(u'单据编号')
    sell_amount = fields.Float(u'销售金额', digits=dp.get_precision('Amount'))
    discount_amount = fields.Float(u'优惠金额',
                                   digits=dp.get_precision('Amount'))
    amount = fields.Float(u'优惠后金额', digits=dp.get_precision('Amount'))
    partner_cost = fields.Float(u'客户承担费用', digits=dp.get_precision('Amount'))
    receipt = fields.Float(u'已收款', digits=dp.get_precision('Amount'))
    balance = fields.Float(u'应收款余额', digits=dp.get_precision('Amount'))
    receipt_rate = fields.Float(u'回款率(%)')
    note = fields.Char(u'备注')

    @api.multi
    def view_detail(self):
        '''销售收款一览表查看明细按钮'''
        self.ensure_one()
        order = self.env['sell.delivery'].search([('name', '=', self.order_name)])
        if order:
            if not order.is_return:
                view = self.env.ref('sell.sell_delivery_form')
            else:
                view = self.env.ref('sell.sell_return_form')
            
            return {
                'name': u'销售发货单',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': False,
                'views': [(view.id, 'form')],
                'res_model': 'sell.delivery',
                'type': 'ir.actions.act_window',
                'res_id': order.id,
            }
