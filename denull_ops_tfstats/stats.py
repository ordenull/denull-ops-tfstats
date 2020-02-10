import logging
from prettytable import PrettyTable

class Resource:
  """
  Wraps a terraform resource
  """

  def __init__(self, resource_dict: dict):
    self.data = resource_dict

  @property
  def mode(self):
    return self.data['mode']

  @property
  def type(self):
    return self.data['type']

  @property
  def name(self):
    return self.data['name']

  @property
  def instances(self):
    return self.data.get('instances', [])

  @property
  def raw(self):
    return self.data

  def __str__(self):
    return "{}.{}.{}".format(self.mode, self.type, self.name)

  def __repr__(self):
    return "{}.{}.{}".format(self.mode, self.type, self.name)


class ResourceStats:
  """
  Keeps track of resource stats
  """

  def __init__(self):
    self.table = {}
    self.total_count = 0
    self._include_filters = []
    self._exclude_filters = []

  def add_resource(self, resource: Resource):
    """ Count a resource if it passes the filters """
    resource = self.filter_resource(resource)
    if resource is None:
      # Resource has been excluded by the filter
      return
    count = len(resource.instances)
    if count == 0:
      # This resource is a reference
      return
    if resource.type not in self.table:
      self.table[resource.type] = 0
    self.table[resource.type] += count
    self.total_count += count

  def filter_resource(self, resource: Resource):
    """
    Filters out resources that are not interesting to us.
    Returns None if it has been excluded.
    """
    # To be considered, the resource must match all include filters if any are specified
    if len(self._include_filters) > 0:
      matched_include = False
      for filtr in self._include_filters:
        if resource.raw[filtr['name']] == filtr['value']:
          matched_include = True
          break
      if not matched_include:
        logging.debug("Excluding: %s because it didn't match any include filter", resource)
        return None

    # To be considered, the resource must not match any of the exclude filters
    for filtr in self._exclude_filters:
      if resource.raw[filtr['name']] == filtr['value']:
        logging.debug("Excluding %s: %s=%s", resource, filtr['name'], resource.raw[filtr['name']])
        return None

    # Passed all of the filters
    return resource

  def add_include_filter(self, field_name, field_value):
    self._include_filters.append({
      'name': field_name,
      'value': field_value,
    })

  def add_exclude_filter(self, field_name, field_value):
    self._exclude_filters.append({
      'name': field_name,
      'value': field_value,
    })

  def get_stats_table(self, add_total=False):
    t = PrettyTable(['Type', 'Count'])
    t.align['Type'] = "l"
    t.align['Count'] = "l"
    resource_types = sorted(self.table.keys())
    for resource_type in resource_types:
      t.add_row([resource_type, self.table[resource_type]])
    if add_total:
      t.add_row(['Total', self.total_count])
    return t