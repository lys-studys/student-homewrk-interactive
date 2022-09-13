#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from xmlrpc.server import SimpleXMLRPCServer
from tutorials import config, utils
def main():
    """启动redis后台监听进程"""
#    utils.get_redis_conn()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
            )from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    #server = SimpleXMLRPCServer(("121.40.138.226", 9000), allow_none=True)
    #server.register_function(test)
    #server.serve_forever()
    main()
