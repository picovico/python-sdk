Getting Started (CLI)
=====================

`picovico-client` is available to use with additional commands and options.

.. code-block:: console

   $ picovico-client --help


Global Option
-------------
    
    `\-\-profile PROFILE`
        For profile to use with commands

Commands
--------
    `configure`
        OPTIONS:
            `\-\-with login/authenticate`:
                Whether you would like to store your authenticate or login information.
            `\-\-log`:
                Whether log should be maintained. [stored in $HOME/.picovico]
    

    `login`
        Login prompt for user
    `authenticate`
        Authenticate with application secret
    'my-profile'
        View Profile
    `project`
        Video project related commands

.. code-block:: console

    $ picovico-client COMMANDS OPTIONS
