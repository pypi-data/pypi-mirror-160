"""some core schema (mostly lookup schema)
"""

import datajoint as dj

from loris.database.table_mixin import ManualLookup
from loris.database.attributes import lookupname


schema = dj.Schema('core')


@schema
class LookupName(ManualLookup, dj.Manual):
    primary_comment = 'identifiable name - e.g. stimulus, xml_file, array'


@schema
class ExtensionLookupName(ManualLookup, dj.Manual):
    primary_comment = 'identifiable name - e.g. prairieview, axograph'


@schema
class DataLookupName(ManualLookup, dj.Manual):
    primary_comment = 'identifiable name - e.g. stimulus, array, movie'


@schema
class FileLookupName(ManualLookup, dj.Manual):
    primary_comment = 'identifiable name - e.g. xml_file, settings'


@schema
class LookupRegex(ManualLookup, dj.Manual):
    primary_comment = 'a regular expression commonly used'


@schema
class IntegerCache(dj.Manual):
    definition = """
    full_table_name : varchar(255)
    attr_name : varchar(255)
    number : int
    ---
    """

    def clear(self):
        from loris import config
        # if already in table do not need to keep in cache
        for entry in self:
            try:
                table = config.get_table(entry['full_table_name'])
                if len(table & {entry['attr_name']: entry['number']}) > 0:
                    (self & entry).delete_quick()
            except Exception:
                pass

    def get_next_number(self, table, attr_name, number):
        # TODO get current user and change table accordingly
        entry = {
            'full_table_name': table.full_table_name, 
            'attr_name': attr_name, 
            'number': number
        }
        restricted_self = self & entry
        if bool(len(restricted_self)):
            return self.get_next_number(table, attr_name, number+1)
        else:
            self.insert1(entry)
            return number



