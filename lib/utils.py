'''
    Picovico: Utils library
'''

def is_local_file(file_path):
    prefix = file_path[0:7].lower()

    if prefix == "http://" or prefix == "https:/":
        return False
    else:
        return True