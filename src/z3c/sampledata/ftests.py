import unittest

from zope import interface

import zope.event
from zope.lifecycleevent import ObjectCreatedEvent

from zope.app.testing import functional
from zope.pluggableauth import PluggableAuthentication
from zope.app.authentication.principalfolder import PrincipalFolder
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.authentication.interfaces import IAuthentication


functional.defineLayer('TestLayer', 'ftesting.zcml')


class IPrincipalDataSource(interface.Interface):
    pass

def principalDataFactory(object):
     return [{'login':'jukart', 'password':'trakuj'},
             {'login':'srichter', 'password':'rethcirs'}]


# XXX This setup seems to be not necessary as tests run fine without it.
def setUp(test):
    site = functional.getRootFolder()
    sm = site.getSiteManager()
    default = sm['default']
    if not 'pau' in default:
        pau = PluggableAuthentication()
        zope.event.notify(ObjectCreatedEvent(pau))
        default['pau'] = pau
        sm.registerUtility(pau, IAuthentication)
    else:
        pau=default['pau']
    # we can do this always
    pau.credentialsPlugins = ('Session Credentials', )
    pfNames = (u'members',)
    pau.authenticatorPlugins = pfNames
    for name in pfNames:
        if name in pau:
            continue
        pf = PrincipalFolder(name +'.')
        zope.event.notify(ObjectCreatedEvent(pf))
        default['pau'][name] = pf
        sm.registerUtility(pf, IAuthenticatorPlugin, name)


def test_suite():
    suite = unittest.TestSuite()
    suites = (
        functional.FunctionalDocFileSuite('browser/README.txt',
                                          setUp = setUp,
                                         ),
        )
    for s in suites:
        s.layer=TestLayer
        suite.addTest(s)
    return suite
