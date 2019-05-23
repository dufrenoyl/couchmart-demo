#!/usr/bin/env - python
from __future__ import print_function

from couchbase.bucket import Bucket
import settings
import random

bucket_name = settings.BUCKET_NAME
user = settings.USERNAME
password = settings.PASSWORD
if settings.AWS:
    node = settings.AWS_NODES[0]
else:
    node = settings.AZURE_NODES[0]

SDK_CLIENT = Bucket('couchbase://{0}/{1}'.format(node, bucket_name),
                    username=user, password=password)

SDK_CLIENT.timeout = 15

LIST_DOC = "ludo.all_the_products"

PRODUCTS = [
    {"name": "fraises Mat & Lou", "description": "Fabriquées avec des colorants d'origine naturelle",
     "price": 1.00, "category": "snacks", "image": "fraises.jpg", "stock": 100},
    {"name": "tartelettes", "description": "Mini tartelettes chocolat au lait coeur fondant",
    "price": 1.00, "category": "snacks", "image": "tartelettes.jpg", "stock": 100},
    {"name": "Pain de Mie", "description": "Pain de Mie sans huile de Palme",
     "price": 1.00, "category": "pain", "image": "pain.jpg", "stock": 100},
    {"name": "Pommes", "description": "Delicieuses pommes",
     "price": 1.00, "category": "fruit", "image": "pommes.jpg", "stock": 100},
    {"name": "Vin", "description": "Buzet AOC Roc de Breyssac",
     "price": 1.00, "category": "boisson", "image": "vin.png", "stock": 100},
    {"name": "Hachis Parmentier", "description": "Prepare en France avec viande d'origine bovine francaise",
     "price": 1.00, "category": "surgele", "image": "hachis.jpg", "stock": 100},
    {"name": "Yaourt", "description": "Avec des morceaux de fruits rouges",
     "price": 1.00, "category": "frais", "image": "yaourt.jpg", "stock": 100},
    {"name": "Saumon", "description": "Saumons frais des Fjords de Norvege",
     "price": 1.00, "category": "frais", "image": "saumon.jpg", "stock": 100},
]


def check_and_create_view():
    design_doc = {
        'views': {
            'by_timestamp': {
                'map': '''
                function(doc, meta) {
                    if (doc.type && doc.type== "order" && doc.ts) {
                        emit(doc.ts, null)
                    }
                    }
                '''
                }
            }
        }

    mgr = SDK_CLIENT.bucket_manager()
    mgr.design_create(settings.DDOC_NAME, design_doc, use_devmode=False)
    res = SDK_CLIENT.query(settings.DDOC_NAME, settings.VIEW_NAME)
    for row in res:
        print (row)


list_doc = {"type": "product-list", "owner": "ludo",
            "name": "List of all products"}


def add_products():
    SDK_CLIENT.upsert(LIST_DOC, list_doc)

    i = 12000
    items = []
    for product in PRODUCTS:
        product_id = "product:" + product['name']
        items.append(product_id)
        product['type'] = "product"
        product['complete'] = False
        product['price'] = round(random.uniform(0.25, 4.99), 2)
        product['createdAt'] = i
        i += 1
        product['product'] = product['name']
        product['productList'] = {"id": LIST_DOC, "owner": "ludovic"}
        SDK_CLIENT.upsert(product_id, product)
    SDK_CLIENT.upsert("items", {"items": items})


if __name__ == '__main__':
    add_products()
    check_and_create_view()
    print("Successfully populated dataset")
