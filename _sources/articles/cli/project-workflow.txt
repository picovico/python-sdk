Project Workflow and Subcommands (CLI)
======================================

All actions related to a video project is provided by this command. It requires subcommands for respective action.

Project Workflow
----------------
Basically, the project workflow begins with an empty project with a project name. The video definition is provided in a JSON object ``assets``. The object holds complete details of the images, text, music and credits. Style and quality properties are specified in the same request.

After the definition, either ``preview`` or ``render`` action is send.

CLI Subcommands
---------------
Project command in CLI works as per project workflow in the API.

    1. begin
        Start a video project. Provide a name, choose a style, music, etc. Loads the project into active session. All other subcommands will work for the project begun at this step.
        
        **Example**
          ``picovico-client project begin --name "Hello World" --style "vanilla"``
    
    2. define
        Define contents (assets) for the video project begun earlier.

        **Example**
          ``picovico-client project define text -title "Hello World" -text "Where am I ?"``
          ``picovico-client project define photo -filename image.jpg -text "This is me"``
    
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



