Inscribe.ai
===========

-  API wrapper for `Inscribe`_

For more information, please read our `documentation`_.

Breaking Changes
----------------
From v3.0.0 onwards, the following API token formats have been removed:
1. Supplying an `api_key` argument.
2. Supplying an `access_key` and `secret_key`.

From v3.0.0 onwards, you must supply a `secret_token` which is supplied to you on creation of an API token.

Installation
------------

-  ``pip install inscribe``

Usage
-----

.. code:: python

   import inscribe
   import json

   # API Authentication
   api = inscribe.Client(secret_token="YOUR_API_SECRET_TOKEN")

   # Create customer folder
   customer = api.create_customer(name="new")
   customer_id = customer['data']['id']

   # Upload document
   doc_obj = open("YOUR_FILE.pdf", "rb")
   document = api.upload_document(customer_id=customer_id, document=doc_obj)
   document_id = document['result_urls'][0]['document_id']

   # Check document
   result = api.retrieve_document_results(customer_id=customer_id, document_id=document_id)
   print(json.dumps(result, indent=2))

.. _Inscribe: https://inscribe.ai
.. _documentation: https://docs.inscribe.ai/#introduction
