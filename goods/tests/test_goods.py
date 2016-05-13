# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase


class test_goods(TransactionCase):

    def test_conversion_unit(self):
        ''' 单位转化，1捆网线12根  '''
        res1 = self.env.ref('goods.cable').conversion_unit(10)
        self.assertEqual(res1, 120)

    def test_anti_conversion_unit(self):
        ''' 单位转化，12根网线1捆  '''
        res2 = self.env.ref('goods.cable').anti_conversion_unit(12)
        self.assertEqual(res2, 1)

    def test_uom(self):
        cable = self.browse_ref('goods.cable')
        uom_pc = self.browse_ref('core.uom_pc')

        cable.uom_id = uom_pc
        cable.onchange_uom()

        self.assertEqual(cable.uos_id, cable.uom_id)

    def test_unlink(self):
        ''' 删除商品其对应属性也删除  '''
        self.env.ref('goods.keyboard').unlink()
        with self.assertRaises(ValueError):
            self.env.ref('goods.attribute_value_white')

    def test_name_search(self):
        '''测试goods的按名字和编号搜索'''
        mouse = self.env.ref('goods.mouse')
        # 使用name来搜索键盘
        result = self.env['goods'].name_search('鼠标')
        real_result = [(mouse.id,
                        mouse.code + '_' + mouse.name)]

        self.assertEqual(result, real_result)

        # 使用code来搜索键盘
        result = self.env['goods'].name_search('001')
        self.assertEqual(result, real_result)
