# JIRA RSTAR-366

Below are some the issues with converting our current task queue infrastructure to Celery and Python.

One of the most time consuming steps is actually learning a new language.  Event the simplest of tasks may take forever when accounting for debugging.  The functionality of the current infrastructure can't be achieved by inserting an exec() like method call around a publication script.  For example, the book publishing scripts were designed to be run by pointing them at a rstar content directory.  To get them to run with input and output parameters, we needed to dynamically create a pseudo rstar directory to emulate the environment the scripts expect.  Another example is that audio encoding doesn't use a script at all.  We would to port significant chunks of code.

Python 3 is not available by default on Centos 6 so I had to download and compile and updated version.  There were issues with my install of 3.8 and openssl 1.0.1 so I downgraded to 3.6.  We will need to create packages and install on each of the worker hosts.

We would need to rewrite the reporting/status tools and implement the backend that stores the return codes and status.

We would need to rewrite the init scripts and systemd configuration for the workers.

We would need to replace the logrotate config.



