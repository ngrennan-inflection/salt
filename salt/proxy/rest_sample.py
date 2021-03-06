# -*- coding: utf-8 -*-
'''
This is a simple proxy-minion designed to connect to and communicate with
the bottle-based web service contained in https://github.com/salt-contrib/proxyminion_rest_example
'''
from __future__ import absolute_import

# Import python libs
import logging
import salt.utils.http

HAS_REST_EXAMPLE = True

# This must be present or the Salt loader won't load this module
__proxyenabled__ = ['rest_sample']


# Variables are scoped to this module so we can have persistent data
# across calls to fns in here.
GRAINS_CACHE = {}
DETAILS = {}

# Want logging!
log = logging.getLogger(__file__)


# This does nothing, it's here just as an example and to provide a log
# entry when the module is loaded.
def __virtual__():
    '''
    Only return if all the modules are available
    '''
    log.debug('rest_sample proxy __virtual__() called...')
    return True


def init(opts):
    '''
    Every proxy module needs an 'init', though you can
    just put a 'pass' here if it doesn't need to do anything.
    '''
    log.debug('rest_sample proxy init() called...')

    # Save the REST URL
    DETAILS['url'] = opts['proxy']['url']

    # Make sure the REST URL ends with a '/'
    if not DETAILS['url'].endswith('/'):
        DETAILS['url'] += '/'


def grains():
    '''
    Get the grains from the proxied device
    '''
    if not GRAINS_CACHE:
        r = salt.utils.http.query(DETAILS['url']+'info', decode_type='json', decode=True)
        GRAINS_CACHE = r['dict']
    return GRAINS_CACHE


def grains_refresh():
    '''
    Refresh the grains from the proxied device
    '''
    GRAINS_CACHE = {}
    return grains()


def service_start(name):
    '''
    Start a "service" on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'service/start/'+name, decode_type='json', decode=True)
    return r['dict']


def service_stop(name):
    '''
    Stop a "service" on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'service/stop/'+name, decode_type='json', decode=True)
    return r['dict']


def service_restart(name):
    '''
    Restart a "service" on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'service/restart/'+name, decode_type='json', decode=True)
    return r['dict']


def service_list():
    '''
    List "services" on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'service/list', decode_type='json', decode=True)
    return r['dict']


def service_status(name):
    '''
    Check if a service is running on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'service/status/'+name, decode_type='json', decode=True)
    return r['dict']


def package_list():
    '''
    List "packages" installed on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'package/list', decode_type='json', decode=True)
    return r['dict']


def package_install(name, **kwargs):
    '''
    Install a "package" on the REST server
    '''
    cmd = DETAILS['url']+'package/install/'+name
    if 'version' in kwargs:
        cmd += '/'+kwargs['version']
    else:
        cmd += '/1.0'
    r = salt.utils.http.query(cmd, decode_type='json', decode=True)
    return r['dict']


def package_remove(name):

    '''
    Remove a "package" on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'package/remove/'+name, decode_type='json', decode=True)
    return r['dict']


def package_status(name):
    '''
    Check the installation status of a package on the REST server
    '''
    r = salt.utils.http.query(DETAILS['url']+'package/status/'+name, decode_type='json', decode=True)
    return r['dict']


def ping():
    '''
    Is the REST server up?
    '''
    r = salt.utils.http.query(DETAILS['url']+'ping', decode_type='json', decode=True)
    try:
        return r['dict'].get('ret', False)
    except Exception:
        return False


def shutdown(opts):
    '''
    For this proxy shutdown is a no-op
    '''
    log.debug('rest_sample proxy shutdown() called...')
