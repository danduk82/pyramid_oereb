
import logging
import json

log = logging.getLogger('JSON')

def log_response(wrapped):
    def wrapper(context, request):
        response = wrapped(context, request)
#        import ipdb; ipdb.set_trace()
        ret_dict = _serialize_response(response)
        ret_dict.update(_serialize_request(request))
        log.info(json.dumps(ret_dict))
        return response
    return wrapper


def _serialize_response(response):
    x = {}
    x['status']=response.status
    x['headers']=dict(response.headers)
    x['extras']= response.extras if hasattr(response,'extras') else None
    return {'response': x}

def _serialize_request(request):
    x = {}
    x['headers']=dict(request.headers)
    x['traversed']=str(request.traversed)
    x['parameters']=dict(request.GET)
    x['path']=str(request.path)
    x['view_name']=str(request.view_name)
    return {'request': x}


class OerebStats(dict):
    def __init__(self, 
                 service=None,
                 output_format=None,
                 params=None):
        super(OerebStats,self).__init__(service=service,
                                        output_format=output_format,
                                        params=params)
        self.itemlist = super(OerebStats,self).keys()
    def __setitem__(self, key, value):
         # TODO: what should happen to the order if
         #       the key is already in the dict       
        self.itemlist.append(key)
        super(OerebStats,self).__setitem__(key, value)
    def __iter__(self):
        return iter(self.itemlist)
    def keys(self):
        return self.itemlist
    def values(self):
        return [self[key] for key in self]  
    def itervalues(self):
        return (self[key] for key in self)
