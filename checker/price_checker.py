__author__ = 'toor'

from flask.ext.login import unicode
import datetime
def fuck():
    print("FUCK")


def price_check(new_price_data, item):
    '''
    Check the prices for bullshit.
    :param new_price_data:
    :param old_price_data:
    :return: 400 = failed, 1 = good job
    '''

    for store_data in new_price_data:
        if 'store_id' in store_data and type(store_data['store_id']) is not unicode:
            return 400
        if 'price_per_unit' in store_data and type(store_data['price_per_unit']) is not int:
            return 400
        if 'price' in store_data and type(store_data['price']) is not int:
            return 400
        if 'user_id' in store_data and type(store_data['user_id']) is not unicode:
            return 400
        # print("store_id ", new_store['store_id'])
        for store in item['stores']:
            if store['store_id'] == store_data['store_id']:
                print("FOUND ONE")
                if store['price_per_unit'] == store_data['price_per_unit'] or store['price'] == store_data['price']:
                    print("SAME PRICE")
                else:
                    print("PRICE NOT THE SAME")
                    # TODO: ADD SOME FUNCTION TO DEAL WITH WEIGHT AND SHIT.
                    if item['unit'] == 1:
                        store['price'] = store_data['price_per_unit']
                        store['price_per_unit'] = store_data['price_per_unit']
                    else:
                        store['price_per_unit'] = store_data['price_per_unit']
                        store['price'] = store_data['price']
                    store['date_mod'] = datetime.datetime.utcnow()
                    # TODO: get the id part working
                    store['user_id'] = '99'
                break
            else:
                continue
        else:
            print(store_data['store_id'], " NO STORE WITH THIS")
            new_store_data = {"store_id": store_data['store_id'],
                              "discount": store_data['discount'],
                              "user_id": "99",
                              "price": store_data['price'],
                              "price_per_unit": store_data['price_per_unit'],
                              "date_mod": datetime.datetime.utcnow()}
            print(new_store_data)
            assert isinstance(item['stores'], list)
            item['stores'].append(new_store_data)
    return 1