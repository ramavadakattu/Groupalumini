from settings import *

DEBUG = True

SESSION_COOKIE_DOMAIN = '.groupalumini2.com'

#Also add DEBUG TOOL BAR in the dev environment
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ('127.0.0.1',)

'''
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
'''

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS':False
}



#local instance
maps_api_key ="ABQIAAAA1-qENYBwsI3vWi4w_b2G8xQptDmXe38Qxvat03uACRGxbee2qxR0yYS4RxdOJcvQKJAh17ghEEay-Q"



