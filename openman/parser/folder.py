import re
from ..errors import FolderParserException, RequestParserException
from ..utils import is_folder, is_request
from .requestitem import RequestItem

class Folder(object):
    
    def __init__(self, folder=None):
        if (folder is None) \
            or (not isinstance(folder, dict) \
                or (not is_folder(folder))):
            raise FolderParserException('Not a valid folder')
        self.folder = folder
    
    @classmethod
    def parse(cls, folder=None):
        return cls(folder)
    
    @property
    def summary(self):
        return self.get_summary()
    
    @property
    def description(self):
        return self.get_description()
    
    def get_summary(self):
        return self.folder.get('name')
    
    def get_description(self):
        return self.folder.get('description')
    
    def get_requestitems(self, folder=None):
        request_items = []
        folder =  folder or self.folder['item']
        for item in folder:
            if is_folder(item):
                request_items.extend(self.get_requestitems(item.get('item')))
            try:
                request_items.append(RequestItem(item))
            except RequestParserException:
                continue
        return request_items