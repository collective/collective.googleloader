from zope import interface
from zope import schema

class IGoogleLoaderLayer(interface.Interface):
    """Browser layer for this add-on"""

class IGoogleLoaderSettings(interface.Interface):
    """Settings of this add-on"""
    
    api_keys = schema.List(title=u"api keys",
                           value_type=schema.ASCIILine(title=u"api key"))
