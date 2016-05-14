Getting Started (CLI)
=====================

`The official Picovico Python SDK <http://github.com/picovico/python-sdk>`_ comes with a handy command line utility tool ``picovico-client`` to explore the video rendering API. Use it to login to your account, check account settings, create a video, check your videos, browse library etc. 


**Example usages:**

.. code-block:: console

   $ picovico-client --help
   $ picovico-client COMMANDS OPTIONS

Global Options
--------------
``--profile PROFILE``
Profiles are saved in ``$HOME/.picovico/profile.ini``. Use this option to switch among the settings.

``--help`` 
Get quick Help for commands and subcommands

Available Commands
------------------
1. configure
~~~~~~~~~~~~

| a. ``--with login`` 
|     Configure cli profile for email/password based authentication   
|
| b. ``--with authenticate`` 
|     Configure cli profile for app_id, app_secret based authentication
|
| c. ``--log`` 
|     Enable / Disable request logging *(stored inside* ``$HOME/.picovico`` *)*    

| 
2. login
~~~~~~~~
User session is mandatory for all the component commands. Login command prompts for username and password, and is generally used to identify third-party users.

3. logout
~~~~~~~~~
Logs out from any saved session. Resets session saved in file ``$HOME/.picovico/session``    

4. authenticate
~~~~~~~~~~~~~~~
Login with app_id and app_secret. Doesn't prompt for username / password, instead prompts for app_secret.

4. my-profile
~~~~~~~~~~~~~
View details of the account currently logged in.

5. project
~~~~~~~~~~
All actions related to a video project is provided by this command. It requires subcommands for respective action.
Learn more about `The Project Workflow, and subcommands <cli-project-workflow.html>`_
