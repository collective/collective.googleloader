from zope import component
from zope import interface
from zope.site.hooks import getSite

from plone.app.layout.viewlets.common import ViewletBase

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from collective.googleloader import interfaces
from Products.ResourceRegistries.browser.scripts import ScriptsView

from plone.registry.interfaces import IRegistry, IRecordModifiedEvent

BASE = {'inline':False,
        'conditionalcomment':'',
        'src':''}
JSAPI = BASE.copy()
JSAPI['src'] = 'https://www.google.com/jsapi?key='

def get_resource_id(api_key):
    return 'https://www.google.com/jsapi?key='+api_key

@component.adapter(interfaces.IGoogleLoaderSettings, IRecordModifiedEvent)
def handleRegistryModified(settings, event):
    #FIRST: remove old resource
    oldjsapi = None
    if event.record.fieldName == 'api_keys':
        unregisterJSAPI(event.oldValue)
        registerJSAPI(settings.api_keys)

def unregisterJSAPI(api_keys):
    site = getSite()
    jsregistry = site.portal_javascripts
    if type(api_keys) is not dict:
        api_keys = get_api_keys(raw=api_keys)

    for host in api_keys:
        resource_id = get_resource_id(api_keys[host])
        jsregistry.unregisterResource(resource_id)

def registerJSAPI(api_keys):
    site = getSite()
    jsregistry = site.portal_javascripts
    if type(api_keys) is not dict:
        api_keys = get_api_keys(raw=api_keys)

    base_kwargs = {'expression':"python: context.restrictedTraverse('@@plone_portal_state').portal_url().startswith('%s')",
              'enabled':True,
              'cookable':True,
              'cacheable':True,
              'conditionalcomment':'',
              'authenticated':False,
              'inline':False,
              'compression':None}
    for host in api_keys:
        resource_id = get_resource_id(api_keys[host])
        kwargs = base_kwargs.copy()
        kwargs['expression'] = kwargs['expression']%host
        jsregistry.registerScript(resource_id, **kwargs)
        jsregistry.moveResourceToTop(resource_id)

def get_api_keys(raw=None):
    """Return api keys as dict"""
    if raw is not None:
        api_keys = raw
    else:
        registry = component.getUtility(IRegistry).forInterface(interfaces.IGoogleLoaderSettings)
        api_keys = registry.api_keys
    res = {}

    for value in api_keys:
        value = value.split("|")
        if len(value) == 2:
            res[value[0].strip()] = value[1].strip()

    return res

#class ScriptsView(ScriptsView):
#    """The google libraries viewlet
#    
#    should render the include of jsapi with key and the google.load calls
#    """
#
#    def scripts(self):
#        """The super version of this view is the one responsible to cook
#        javascript resources. This version first include google libraries
#        and then append the plone resources
#        """
#
#        result = []
#        api_key = self.api_key()
#
#        if api_key:
#            data = JSAPI.copy()
#            data['src'] += self.api_key
#            result.append(data)
#
#        result.extend(super(ScriptsView,self).scripts())
#
#        return result
#
#    def registry(self):
#        return component.getUtility(IRegistry).forInterface(interfaces.IGoogleLoaderSettings)
#
#    def api_key(self):
#        host = self.request.get('SERVER_URL')
#        api_keys = self.api_keys()
#        if host in api_keys:
#            return api_keys[host]
#
#    def api_keys(self):
#        registry = self.registry()
#        api_keys = registry.api_keys
#        res = {}
#
#        for value in keys:
#            value = value.split("|")
#            if len(value) == 2:
#                res[value[0].strip()] = value[1].strip()
#
#        return res

class LoaderScript(BrowserView):
    """generate javascript loader script"""

    def __call__(self, *args, **kwargs):
        return self.loader_script()

    def loader_script(self):
        registry = component.getUtility(IRegistry).forInterface(interfaces.IGoogleLoaderSettings)
        return str(registry.loader_script)
