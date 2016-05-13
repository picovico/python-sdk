Getting Started (CLI)
=====================

`picovico-client` is available to use with additional commands and options.

.. code-block:: console

   $ picovico-client --help


Global Option
-------------
    
    `--profile PROFILE`
        For profile to use with commands
    
Commands
--------
    `configure`
        
        Options:
            --with login/authenticate:
                Whether you would like to store your authenticate or login information.
            
            --log:
                Whether log should be maintained. [stored in $HOME/.picovico]
        
    .. code-block:: console

        $ picovico-client configure -h

