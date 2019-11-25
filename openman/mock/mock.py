import connexion
import os
from .fakemock_resolver import FakerMockResolver

class Mock(object):

    def __init__(self, spec, spec_dir='openapi/'):
        self.app = connexion.FlaskApp(__name__, specification_dir=spec_dir)
        self.app.app.url_map.strict_slashes = False
        self.spec =  spec
    
    def start(self, resolver=FakerMockResolver, port=8080, **kwargs): 
        self.app.add_api(self.spec, resolver=resolver('api'))
        self.app.run(port=port, **kwargs)