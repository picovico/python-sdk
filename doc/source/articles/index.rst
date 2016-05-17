Getting Started with SDK
========================

Picovico Python SDK provides a wrapper functionality to the Picovico RESTlike API. Please find few samples to get started with the SDK.

Basic Workflow
~~~~~~~~~~~~~~
  1. Define API Credentials ``App ID, App Secret, Device ID``
  2. Create API instance with the credentials ``api=PicovicoAPI(id, device_id)``
  3. Authenticate with your account ``api.authenticate(secret)``
  4. Project Workflow (To Create a video)
    a. Begin a project
    b. Define the video (Add slides, music, style, etc)
    c. Preview the project if required
    d. Render the video
  5. Explore other features

Examples
~~~~~~~~
.. toctree::
  :titlesonly:

  sdk/example-hello-world
  sdk/example-sdk-features