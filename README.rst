=================================
DIARIO Python SDK
=================================

|Pypi Version| 

DIARIO bridges a natural gap that antiviruses do not usually match. DIARIO is not intended to replace antiviruses, but to cover the gap with fresh samples: DIARIO is especially good detecting them. DIARIO helps detect fresh malware without compromising your privacy or sharing content.

.. |Pypi Version| image:: https://img.shields.io/pypi/v/diario.svg
   :target: https://pypi.python.org/pypi/diario

Prerequisites
===============

* Python 3 or 2.7+


* A valid account in DIARIO (https://diario.e-paths.com/index.html) in order to get a **APP_ID** and **SECRET_KEY** keys (Registration is FREE).


Installation
============
Install diario package using pip::

    pip install diario


Minimal usage
=============

* Create a DIARIO object with the "Application ID" and "Secret" previously obtained

.. code-block:: python

    from diario import Diario
    api = Diario("APP_ID_HERE", "SECRET_KEY_HERE")



'host' and 'port' default parameters are set to diario-elevenlabs.e-paths.com and 443.


* Call to DIARIO Server to do searches, upload and analyze documents, ...

.. code-block:: python

    response = api.search('23203f9264161714cdb8d2f474b9b641e6a735f8cea4098c40a3cab87439d749')


* After every API call, get DIARIO response data and errors and handle them

.. code-block:: python

    response_data = response.data
    response_error = response.error


REST API specification
======================

* Rest API documentation (https://diario.e-paths.com/api-specification.html).
