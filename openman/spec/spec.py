from apispec import APISpec 
from .operation import Operation
from .plugins import MultiOperationBuilderPlugin

class Spec(object):

    OPENAPI_VERSION = '3.0.0'
    
    def __init__(self, postman_collection):
        self.postman_collection = postman_collection
        self._servers = ['http://localhost']
    
    @property
    def info(self):
        return self.get_info()
    
    @property
    def openapi(self):
        return Spec.OPENAPI_VERSION
    
    @property
    def servers(self):
        return self.get_servers()
    
    def add_servers(self, server):
        if isinstance(server, list):
            self._servers.extend(server)
        else:
            self._servers.append(server)
        return self

    def get_info(self, version='1.0.0'):
        return dict(
            title = self.postman_collection.name,
            description = self.postman_collection.description,
            version = version
        )
    
    def get_servers(self):
        return self._servers
    
    def convert(self, yaml=False, references=True, ignorespec=None, **options):
        spec = APISpec(
            title= self.info.get('title'),
            version= self.info.get('version'),
            openapi_version = self.openapi,
            plugins=[MultiOperationBuilderPlugin(references)],
            **options
        )

        for requestitem in self.postman_collection.get_requestitems():
            spec.path(
                path = requestitem.get_request().path,
                operations = Operation(requestitem, ignorespec=ignorespec).get()
            )
        return spec.to_yaml() if yaml else spec.to_dict()