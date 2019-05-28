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
    {"name": "Pommes", "description": "Delicieuses pommes",
    "price": 1.00, "category": "fruit", "image": "pommes.png", "stock": 100},
    {"name": "Kiwis", "description": "Kiwi Sungold BIO",
    "price": 1.00, "category": "fruit", "image": "kiwi.png", "stock": 100},
    {"name": "Citrons", "description": "Citron Primofiori U BIO",
    "price": 1.00, "category": "fruit", "image": "citrons.png", "stock": 100},
    {"name": "Yaourt", "description": "Fromage frais nature au lait pasteurise U BIO",
    "price": 1.00, "category": "frais", "image": "yaourt.png", "stock": 100},
    {"name": "Saumon", "description": "Saumons frais des Fjords de Norvege",
    "price": 1.00, "category": "frais", "image": "saumon.png", "stock": 100},
    {"name": "Sandwich", "description": "Sandwich suedois duo de saumon SODEBO",
    "price": 1.00, "category": "frais", "image": "sodebo.png", "stock": 200},
    {"name": "Liegeois", "description": "Liegeois au chocolat LA FERMIERE",
    "price": 1.00, "category": "frais", "image": "liegeois.png", "stock": 50},
    {"name": "Merguez", "description": "Merguez U 6 pieces",
    "price": 1.00, "category": "frais", "image": "merguez.png", "stock": 100},
    {"name": "Pizza", "description": "Piccolinis flammekueche BUITONI",
    "price": 1.00, "category": "surgele", "image": "pizza.png", "stock": 100},
    {"name": "Feuilletes", "description": "Mini feuilletes a la saucisse",
    "price": 1.00, "category": "surgele", "image": "feuilletes.png", "stock": 100},
    {"name": "Jus de Pomme", "description": "Pue jus refrigere pomme U BIO",
    "price": 1.00, "category": "boisson", "image": "jus.png", "stock": 100},
    {"name": "Jus de Clementine", "description": "Pur jus de Clementine U",
    "price": 1.00, "category": "boisson", "image": "clementine.png", "stock": 100},
    {"name": "Vin", "description": "Buzet AOC Roc de Breyssac",
    "price": 1.00, "category": "boisson", "image": "vin.png", "stock": 100},
    {"name": "fraises MatLou", "description": "Fabriquees avec des colorants d'origine naturelle",
    "price": 1.00, "category": "epicerie", "image": "fraises.png", "stock": 100},
    {"name": "dragibus", "description": "Bonbons Dragibus black surprise",
    "price": 1.00, "category": "epicerie", "image": "dragibus.png", "stock": 100},
    {"name": "Tablette Chocolat", "description": "Tablette de chocolat au lait croustillant",
    "price": 1.00, "category": "epicerie", "image": "chocolat.png", "stock": 100},
    {"name": "Crunch", "description": "Chocolat au lait au riz souffle CRUNCH",
    "price": 1.00, "category": "epicerie", "image": "crunch.png", "stock": 100},
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
