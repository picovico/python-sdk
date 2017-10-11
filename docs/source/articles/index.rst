Getting Started with SDK
========================

Picovico Python SDK provides a wrapper functionality to the Picovico RESTlike API. Please find few samples to get started with the SDK.

Basic Workflow
~~~~~~~~~~~~~~
  1. Define API Credentials ``App ID, App Secret, Device ID``
  2. Create API instance with the credentials ``api=PicovicoAPI(id, device_id, secret)``
  3. Authenticate with your account ``api.authenticate(secret)`` //Only if not initiated with secret
  4. Call api `api.authenticated_api(method='get', url='/me')`

Examples
~~~~~~~~
.. toctree::
  :titlesonly:

  sdk/example-hello-world
  sdk/example-sdk-features

