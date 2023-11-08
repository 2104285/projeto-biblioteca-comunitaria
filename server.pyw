from waitress import serve
    
from setup.wsgi import application
    
serve(application, port='8000',url_scheme='https')
