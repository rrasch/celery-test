import os
import subprocess
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

@app.task
def create_derivatives(rstar_dir, id):
	command = f"{os.environ['HOME']}/work/book-publisher/create-deriv-images.pl -q -r {rstar_dir} {id}"
	print(f"Running {command}")
	p = subprocess.Popen(command,
			shell=True,
			errors='replace',
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT)
	#return iter(p.stdout.readline, b'')
	return iter(p.stdout.readline, '')

# vim: set ts=4:
