#!/usr/bin/env python3

import argparse
import logging
from tasks import do_task

parser = argparse.ArgumentParser(
    description="Add jobs with celery")
parser.add_argument("identifier",  nargs="*",
    help="Identifier")
parser.add_argument("-i", "--input-path",
    help="Input path")
parser.add_argument("-o", "--output-path",
    help="Output path")
parser.add_argument("-r", "--rstar-dir",
    help="RStar directory")
parser.add_argument("-s", "--service", required=True,
    help="Service, e.g. book:create_derivatives")
parser.add_argument("-e", "--extra-args", default="",
    help="Extra arguments")
parser.add_argument("-d", "---debug", action="store_true",
    help="Enable debugging messages")
args = parser.parse_args()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)

args_dict = vars(args)

logging.debug(args_dict)

#do_task(args_dict)
do_task.delay(args_dict)

