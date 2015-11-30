"""
When the access_key and access_token aren't available
for the curent session
"""
class PicovicoUnauthorizedException(Exception):
     def __init__():
        super(PicovicoUnauthorizedException, self).__init__()


"""
When the response status code is not 200
Something like : 
{
    "error":{

    }
}
"""
class PicovicoAPIResponseException(Exception):

    code = None
    message = None
    
    def __init__():
        super(PicovicoAPIResponseException, self).__init__()
