"""Basic utility functions
"""

import warnings


def is_manuallookup(table, ):
    """check if table is a manuallookup table
    """

    truth = False

    try:
        if (
            (len(table.heading.primary_key) == 1)
            and (len(table.heading.secondary_attributes) == 1)
        ):
            pk = table.heading.primary_key[0]
            sk = table.heading.secondary_attributes[0]

            truth = (
                (sk == 'comments')
                & (pk == table.table_name)
            )
    except AttributeError as e:
        print(f"AttributeErrorWarning for table: {table}")
        warnings.warn(e)

    return truth


def save_join(tables):
    """savely join tables ignoring dependent attributes that match.
    """

    for n, table in enumerate(tables):

        if n == 0:
            joined_table = table
        else:
            dep1 = joined_table.heading.secondary_attributes
            dep2 = table.heading.secondary_attributes
            proj = list(set(dep2) - set(dep1))
            joined_table = joined_table * table.proj(*proj)

    return joined_table
