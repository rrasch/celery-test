#!/usr/bin/env python3

from tasks import create_derivatives

rstar_dir = "/content/prod/rstar/content/isaw/awdl"

id = "isaw_awdl_catalog000001"

output = create_derivatives(rstar_dir, id)

for line in output:
	print(line, end='')
	#print(line)

