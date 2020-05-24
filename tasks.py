from argparse import Namespace
from celery import Celery
import importlib
import logging
import os
import re
import sys

sys.path.append(os.getcwd())

app = Celery('tasks')
app.config_from_object('celeryconfig')

class TaskError(Exception):
    """ Raised when task fails """
    pass

def get_class_name(name):
    return "".join(map(str.capitalize, re.split('[_-]', name)))

@app.task
def do_task(args_dict):
    args = Namespace(**args_dict)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    module_name, method_name = args.service.split(":")
    logging.debug("module name: %s", module_name)
    logging.debug("method name: %s", method_name)
    class_name = get_class_name(module_name)
    logging.debug("class name: %s", class_name)
    logging.debug("python sys.path: %s", sys.path)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    obj = cls(args)
    method = getattr(obj, method_name)
    result = method()
    logging.debug("result: %s", result)
    if not result["success"]:
        raise TaskError("Task failed")

