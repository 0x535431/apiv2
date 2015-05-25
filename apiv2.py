from flask import Flask, jsonify, abort
from flask import make_response
from flask import url_for
from flask import request
from flask.ext.login import unicode
from flask.ext.httpauth import HTTPBasicAuth

from checker.price_checker import fuck, price_check

from pymongo import MongoClient
import datetime

app = Flask(__name__, static_url_path="")

items = [
    {
        "id": 1,
        "barcode": 5690541004190,
        "group": "drykkir",
        "name": u'Pepsi 2l',
        "unit": 1,
        "amount": 1,
        "description": u'matvara, drykkur, gos, pepsi',
        "stores": [
            {"store_id": "1", "date_mod": datetime.datetime.utcnow(), "price_per_unit": 133, "price": 133,
             "user_id": "1155285914", "discount": 0.00},
            {"store_id": "2", "date_mod": datetime.datetime.utcnow(), "price_per_unit": 129, "price": 129,
             "user_id": "1155285914", "discount": 0.00}
        ],
        "vnr": "8728",
        "checked": True
    },
    {
        'id': 2,
        'barcode': 2351390003637,
        "group": "mjolkurvorur",
        'name': u'Góðostur 26% sneiðar',
        'unit': 2,
        'amount': 0.363,
        'description': u'matvara, mjolkurvara, ostur, ms',
        'stores': [
            {"store_id": "1", "date_mod": datetime.datetime.utcnow(), "price_per_unit": 1899, "price": 689,
             "user_id": "1155285914", "discount": 0.00},
            {"store_id": "2", "date_mod": datetime.datetime.utcnow(), "price_per_unit": 1899, "price": 689,
             "user_id": "1155285914", "discount": 0.00}
        ],
        "vnr": "8728",
        'checked': False
    },
    {
        'id': 3,
        'barcode': 2351390003637,
        "group": "ávextir",
        'name': u'Bananar',
        'unit': 2,
        'amount': 1.0,
        'description': u'matvara, avextir, bananar',
        'stores': [
            {"store_id": "1", "date_mod": datetime.datetime.utcnow(), "price_per_unit": 414, "price": 414,
             "user_id": "1155285914", "discount": 0.00},
            {"store_id": "2", "date_mod": datetime.datetime.utcnow(), "price_per_unit": 414, "price": 414,
             "user_id": "1155285914", "discount": 0.00}
        ],
        "vnr": "8728",
        'checked': False
    }
]

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'foo':
        return 'bar'
    return None


@auth.error_handler
def unauthorized():
    # the 401 and 403 crap is covered on the blod
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


# The post section
@app.route('/api/v2/item', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        abort(400)
    print(request.json)
    item = {
        'id': items[-1]['id'] + 1,
        'name': request.json['name'],
        'barcode': request.json.get('barcode', ""),
        'description': request.json.get('description', ""),
        'group': request.json.get('group', ""),
        'unit': request.json.get('unit', ""),
        'amount': request.json.get('amount', ""),
        'stores': request.json.get('stores', {}),
        'vnr': request.json.get('vnr', ""),
        'checked': False
    }
    # Set the time of insertion
    for stores in item['stores']:
        stores['date_mod'] = datetime.datetime.utcnow()

    items.append(item)
    return jsonify(make_public_task(item)), 201
    # return jsonify(item), 201


@app.route('/api/v2/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    print(request.json)
    if len(item) == 0:
        abort(404)
    if not request.json:
        print(1)
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        print(2)
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        print(3)
        abort(400)
    if 'checked' in request.json and type(request.json['checked']) is not bool:
        print(4)
        abort(400)
    if 'vnr' in request.json and type(request.json['vnr']) is not unicode:
        print(5)
        abort(400)
    # Why the fuck have this uri?
    if 'uri' in request.json and type(request.json['uri']) is not unicode:
        print(6)
        abort(400)
    if 'amount' in request.json and type(request.json['amount']) is not float:
        if type(request.json['amount']) is not int:
            abort(400)
        print(type(request.json['amount']))
        print(7)
    if 'unit' in request.json and type(request.json['unit']) is not int:
        print(8)
        abort(400)
    if 'barcode' in request.json and type(request.json['barcode']) is not int:
        print(type(request.json['barcode']))
        print(request.json['barcode'])
        print("FUCK!?")
        abort(400)
    if 'group' in request.json and type(request.json['group']) is not unicode:
        print(9)
        abort(400)

    # Set the values
    item[0]['name'] = request.json.get('name', item[0]['name'])
    item[0]['description'] = request.json.get('description', item[0]['description'])
    item[0]['checked'] = request.json.get('checked', item[0]['checked'])
    item[0]['vnr'] = request.json.get('vnr', item[0]['vnr'])
    item[0]['amount'] = request.json.get('amount', item[0]['amount'])
    item[0]['unit'] = request.json.get('unit', item[0]['unit'])
    item[0]['barcode'] = request.json.get('barcode', item[0]['barcode'])
    item[0]['group'] = request.json.get('group', item[0]['group'])
    return jsonify(item[0])


@app.route('/api/v2/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    items.remove(item[0])
    return jsonify({'result': True})


# MONGODB SETUP
# client = MongoClient('localhost', 27017)
# db = client['iceprice']
# collection = db['posts']

# The error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# The test get method
@app.route('/api/v2/item', methods=['GET'])
# @auth.login_required
def get_items():
    return jsonify({'items': [make_public_task(item) for item in items]})
    # return jsonify({'items': items})
    # return jsonify({'item': collection.find_one()})


# The get method Supports coke and pepsi 2L
@app.route('/api/v2/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify(item[0])


def make_public_task(item):
    new_item = {}
    for field in item:
        if field == 'id':
            new_item['uri'] = url_for('get_item', item_id=item['id'], _external=True)
        else:
            new_item[field] = item[field]
    return new_item


# Here we have the Price handlers.
@app.route('/api/v2/price/<int:item_id>', methods=['GET'])
def get_prices(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    # print({'stores': item[0]['stores']})
    # print({'stores': [bob for bob in item[0]['stores']]})
    return jsonify({'stores': item[0]['stores']})
    # return jsonify({'items': [make_public_task(item) for item in items]})


@app.route('/api/v2/price/<int:item_id>', methods=['PUT'])
def update_price(item_id):
    item = [item for item in items if item['id'] == item_id]
    print(item[0])
    print("FOR TEST")
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'stores' in request.json and type(request.json['stores']) != list and len(request.json['stores']) < 1:
        abort(400)
    print(item[0]['stores'])

    if price_check(request.json['stores'], item[0]) == 400:
        abort(400)
    return jsonify(item[0])

# The main runner.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # app.run(debug=True, host='0.0.0.0')
