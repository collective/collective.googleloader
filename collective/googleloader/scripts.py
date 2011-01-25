from zope import component
from zope.site.hooks import getSite

from Products.Five import BrowserView

from collective.googleloader import interfaces
from Products.ResourceRegistries.browser.scripts import ScriptsView

from plone.registry.interfaces import IRegistry, IRecordModifiedEvent

JSAPI_URL = 'https://www.google.com/jsapi?key='

def get_resource_id(api_key):
    return JSAPI_URL+api_key

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
