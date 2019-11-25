import re
from ..errors import CollectionParserException
from ..utils import is_collection, is_folder, is_requestitem
from .folder import  Folder
from .requestitem import RequestItem

class Collection(object):
    
    def __init__(self, collection=None):
        if (collection is None) \
            or (not isinstance(collection, dict) \
                or (not is_collection(collection))):
            raise CollectionParserException('Not a valid collection')
        self.collection = collection
    
    @classmethod
    def parse(cls, collection=None):
        return cls(collection)
    
    @property
    def version(self):
        return self.get_version()
    
    @property
    def name(self):
        return self.get_name()
    
    @property
    def description(self):
        return self.get_description()
    
    def get_version(self):
        search = re.search(
            '^http[s].\\/\\/.*\\/(.*)\\/collection\\.json',
            self.collection['info']['schema'])
        if search and search.group(1):
            return  search.group(1)
        return None
    
    def get_name(self, default='TODO: API Specification'):
        return self.collection['info'].get('name', default)
    
    def get_description(self, default='TODO: API Specification description'):
        return self.collection['info'].get('description', default)
    
    def get_requestitems(self):
        items = []
        for item in self.collection['item']:
            if is_requestitem(item):
                items.append(RequestItem(item))
            elif is_folder(item):
                folder = Folder(item)
                items.extend(folder.get_requestitems())
        return items
    
    def get_folders(self):
        folders = []
        for item in self.collection['item']:
            if is_folder(item):
                folders.append(Folder(item))
        return folders
    
    # def validateSchema(self):
    #     schemaVer = self.schemaVersion.replace('v', '')
    #     schemaPath = os.path.realpath(
    #         os.path.join(os.getcwd(), os.path.dirname(__file__), '..'))
    #     with open(f'{schemaPath}/schema/{schemaVer}.json') as f:
    #         try:
    #             schema = json.load(f)
    #         except Exception:
    #             return True
    #     if schema:
    #         jsonschema.validate(instance=self.pmcollection, schema=schema)