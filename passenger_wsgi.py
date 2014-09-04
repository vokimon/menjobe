import sys, os

project = 'devsite'
python = 'python3.4'
hexversion = 0x3040000

cwd = os.path.dirname(os.path.abspath(__file__))

sys.path.append(cwd)

#Switch to new python
if sys.hexversion < hexversion : os.execl(cwd+"/env/bin/"+ python, python, *sys.argv)

#sys.path.insert(0,cwd+'/env/bin')
sys.path.insert(0,cwd+'/env/lib/'+python+'/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = project+".settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


def log(msg) :
    with open(os.path.join(cwd,"errors"),'w') as errorfile :
        errorfile.write(msg)

class ErrorMiddleware :
    def __init__(self, app) :
        self.app = app
    def __call__(self, environ, start_response) :
        log("No exceptions")
        try:
            return self.app(environ, start_response)
        except:
            import traceback
            tb = traceback.format_exc()
            log(tb)
            start_response('200 OK', [('Content-type', 'text/plain')])
            return ["Exception trapped\n",tb]

def _application(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ["Hello, world!"]

_application = ErrorMiddleware(application)


