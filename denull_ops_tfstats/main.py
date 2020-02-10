import os
import json
import glob
import logging
import argparse

from denull_ops_tfstats.stats import Resource
from denull_ops_tfstats.stats import ResourceStats

def main():
  """ We start here """
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--verbose', help='Be verbose and print debugging info', action="store_true")
  parser.add_argument('--include', type=str, metavar='field=value', nargs='*', default=[], help='Only include resources matching filter')
  parser.add_argument('--exclude', type=str, metavar='field=value', nargs='*', default=[], help='Exclude items with fieldname=fieldvalue')
  parser.add_argument('--recursive', help='Travese the path recursively', action="store_true")
  parser.add_argument('--path', type=str, default=None, help='Terraform state directory with .tfstate files')

  args = parser.parse_args()
  LOG_FORMAT = "%(levelname)s\t%(name)s %(message)s"
  if args.verbose:
    LOG_LEVEL = logging.DEBUG
  else:
    LOG_LEVEL = logging.INFO
  logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

  resource_stats = ResourceStats()
  
  # Set up the resource include filters
  for include in args.include:
    try:
      field_name, field_value = include.split('=')
    except ValueError:
      logging.error("Include filter %s, must be in the name=value format")
      exit(1)
    resource_stats.add_include_filter(field_name, field_value)

  # Set up the resource exclusion filters
  for exclude in args.exclude:
    try:
      field_name, field_value = exclude.split('=')
    except ValueError:
      logging.error("Exclude filter %s, must be in the name=value format")
      exit(1)
    resource_stats.add_exclude_filter(field_name, field_value)

  # Find terraform state files in the path
  if args.path is None:
    logging.error("No search path was specified. Please use the --path argument")
    exit(1)
  if args.recursive:
    filenames = glob.glob(args.path + '/**/*.tfstate', recursive=True)
  else:
    filenames = glob.glob(args.path + '/*.tfstate', recursive=False)

  if len(filenames) == 0:
    logging.error("Could not find any .tfstate files in %s", os.path.abspath(args.path))
    exit(1)

  logging.debug("Found %s state files in %s", args.path, len(filenames))

  for filename in filenames:
    with open(filename, 'r') as f:
      tfstate = json.load(f)
      logging.debug("Loaded Terraform state from %s", filename)
    for r in tfstate.get('resources', []):
      resource = Resource(r)
      resource_stats.add_resource(resource)  
  print(resource_stats.get_stats_table(add_total=True))

if __name__ == '__main__':
  main()