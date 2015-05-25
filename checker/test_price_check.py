import unittest
from checker.price_checker import price_check
import datetime

__author__ = 'toor'


class TestPrice_check(unittest.TestCase):
    def test_price_check(self):
        self.new_price_data = [
            {
                "date_mod": "Mon, 25 May 2015 15:11:29 GMT",
                "discount": 0.0,
                "price": 144,
                "price_per_unit": 144,
                "store_id": "3",
                "user_id": "1155285914"
            },
            {
                "date_mod": "Mon, 25 May 2015 15:15:29 GMT",
                "discount": 0.0,
                "price": 225,
                "price_per_unit": 225,
                "store_id": "1",
                "user_id": "1155285914"
            }
        ]

        self.item = {'unit': 1, 'barcode': 5690541004190, 'name': 'Pepsi 2l',
                     'description': 'matvara, drykkur, gos, pepsi', 'group': 'drykkir',
                     'id': 1, 'vnr': '8728', 'amount': 1, 'checked': True,
                     'stores': [
                         {'user_id': '1155285914', 'discount': 0.0,
                          'date_mod': datetime.datetime(2015, 5, 25, 15, 57, 27, 843554),
                          'price': 133, 'price_per_unit': 133, 'store_id': '1'},
                         {'user_id': '1155285914', 'discount': 0.0,
                          'date_mod': datetime.datetime(2015, 5, 25, 15, 57, 27, 843554),
                          'price': 129, 'price_per_unit': 129, 'store_id': '2'}
                     ],
                     }

        result = price_check(self.new_price_data, self.item)
        self.assertEqual(1, result)

        # TO UNFUCK THE TIMESTAMP!
        for x in self.item['stores']:
            x['date_mod'] = datetime.datetime(2015, 5, 25, 16, 11, 45, 459607)

        self.result_item = {'checked': True, 'stores': [
            {'date_mod': datetime.datetime(2015, 5, 25, 16, 11, 45, 459607), 'user_id': '99', 'discount': 0.0,
             'price': 225, 'price_per_unit': 225, 'store_id': '1'},
            {'date_mod': datetime.datetime(2015, 5, 25, 16, 11, 45, 459607), 'user_id': '1155285914', 'discount': 0.0,
             'price': 129, 'price_per_unit': 129, 'store_id': '2'},
            {'date_mod': datetime.datetime(2015, 5, 25, 16, 11, 45, 459607), 'user_id': '99', 'discount': 0.0,
             'price': 144, 'price_per_unit': 144, 'store_id': '3'}], 'vnr': '8728', 'barcode': 5690541004190, 'unit': 1,
                            'description': 'matvara, drykkur, gos, pepsi', 'amount': 1, 'group': 'drykkir', 'id': 1,
                            'name': 'Pepsi 2l'}
        print(self.item)
        self.assertEqual(self.item, self.result_item)
        self.assertDictEqual(self.item, self.result_item)
        #self.assertEqual(179, result)
        # self.fail()
