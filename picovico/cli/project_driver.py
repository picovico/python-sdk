def get_project_commands():
    project_components = ('music', 'style', 'photo', 'quality', 'text')
    command = {
        'command': 'project', 
        'options': [
                {
                    'name': '--styles',
                    'required': False
                },
                {
                    'name': 'begin',
                    #'required': False,
                    'action': 'store_true'
                },
                {
                    'name': '--quality',
                    'required': False
                },
                {
                    'name': '--name',
                    'required': False
                }
            ],
        #//'action':
        }
    for a in project_components:
        com = {'name': 'add-{}'.format(a)}
        command['options'].append(com)
    return command
