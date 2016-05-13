Getting Started (CLI)
=====================

Picovico Python SDK comes with a handy command line utility tool ``picovico-client`` to explore the video rendering API. Use it to login to your account, check account settings, create a video, check your videos, browse library etc. 


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

Available subcommands
+++++++++++++++++++++
    1. begin
        Start a video project. Provide a name, choose a style, music, etc. Loads the project into active session. All other subcommands will work for the project begun at this step.
    
    2. define
        Define contents (assets) for the video project begun earlier.
    
    3. save
        Sends any local project definition to the server.
    
    4. preview
        Sends a preview request for the active project.
    
    5. render
        Sends a render request for the active project.
    
    6. close
        Sends a save request and closes the active project from the console session. Progress remains saved.
    
    7. discard
        Clears the project from session. Doesn't save any progress made to the project definition.

