Getting Started with SDK
========================

Picovico Python SDK provides a wrapper functionality to the Picovico RESTlike API. Please find few samples to get started with the SDK.

Basic Workflow
~~~~~~~~~~~~~~
  1. Define API Credentials ``App ID, App Secret, Device ID``
  2. Create API instance with the credentials ``api=PicovicoAPI(id, secret, device_id)``
  4. Call api `api.authenticated_api(method='get', url='/me')`

Examples
~~~~~~~~
.. toctree::
  :titlesonly:

  sdk/example-hello-world
..  sdk/example-sdk-features

