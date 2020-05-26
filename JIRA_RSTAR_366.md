# JIRA RSTAR-366

Below are some the issues or obstacles with converting our current task queue infrastructure to Celery.

- One of the most time consuming steps is actually learning a new language, in this case, Python.  Even the simplest of tasks can take forever when tracking down a bug.  It took me a minute trying to figure out why one of the modules I had written loaded in the blocking context but not when the task was called asynchronously.  There is also the rabbit hole of going from one programming concept to another which the first the depends on.
- All the functionality of the current infrastructure can't be achieved by inserting an exec() like method call around a publication script.  For example, the book publishing scripts were designed to be run by pointing them at a rstar content directory.  To get them to run with input and output parameters, we needed to dynamically create a pseudo rstar directory structure to emulate the environment the scripts expect.  Another example is that audio encoding doesn't use a script at all and is implemented using the mediainfo gem.  We would need to port a fair amount of code from Ruby to Python.  It's definitely not impossible, but it is tedious.
- Python 3 is not available by default on Centos 6 so I had to download and compile an updated version.  There were issues with my install of 3.8 and openssl 1.0.1 so I downgraded to 3.6.  Some of the build tests may have failed, so those failures will need to be confirmed as harmless.  I chose this method in favor of the version in the Centos Software Collections repository.
- This segues to the issue of the worker hosts running Centos 6 which has a lot of outdated software.   I usually have to rebuild several dependencies just to successfully run the ./configure script.  This might come into play when porting the A/V functionality.
- We will need to create Python 3.6 packages and install on each of the worker hosts.
- The current reporting/status tools and backend that stores the return status, output, original request, and other attributes will need to be re-implemented using one of Celery's many backends.
- We need to rewrite the init scripts and systemd configuration for the workers.
- We would need to replace the logrotate config.
- Rewrite the job injector script.  This is probably the easiest thing because of Python's argparse module.
