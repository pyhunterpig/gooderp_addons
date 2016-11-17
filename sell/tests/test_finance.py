# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError

class test_month_product_cost(TransactionCase):

    def setUp(self):
        super(test_month_product_cost, self).setUp()
        self.period_id = self.env.ref('finance.period_201601')

    def test_generate_issue_cost(self):
        """本月成本结算 相关逻辑的测试"""
        checkout_wizard_row = self.env['checkout.wizard'].create({'date':'2016-01-31','period_id':self.period_id.id})
        with self.assertRaises(UserError):
            checkout_wizard_row.button_checkout()
        # sell_delivery_rows = self.env['sell.delivery'].search([('type','=','others')])
        wh_in_rows = self.env['wh.in'].search([])
        wh_in_rows.write({'date':'2016-01-31 18:00:00'})
        wh_out_rows = self.env['wh.out'].search([('name', '=', self.env.ref('warehouse.wh_out_whout1').name)])
        wh_out_rows.write({'date':'2016-01-31 18:00:00'})
        # wh_internal_rows = self.env['wh.internal'].search([])
        # [sell_delivery_row.sell_delivery_done() for sell_delivery_row in sell_delivery_rows]
        [wh_in_row.approve_order() for wh_in_row in wh_in_rows]
        [wh_out_row.approve_order() for wh_out_row in wh_out_rows]
        # [wh_internal_row.approve_order() for wh_internal_row in wh_internal_rows]
        self.env['month.product.cost'].generate_issue_cost(self.period_id)

