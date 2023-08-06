from dlt_metabase_source.metabase_source import MetabaseSource as DataSource
import jsonlines

metabase_creds = dict(url='https://metabase-analytics.scalevector.ai/',
                 user='example@scalevector.ai',
                 password='')

s = DataSource(**metabase_creds)

tables = s.tasks()

"""
print(tables)
tasks is a bunch of generators and table names
{'table_name': 'activity', 'data': <generator object MetabaseSource._get_data at 0x1022ce660>}
{'table_name': 'logs', 'data': <generator object MetabaseSource._get_data at 0x1022cea50>}
{'table_name': 'stats', 'data': <generator object MetabaseSource._get_data at 0x1022ceac0>}
{'table_name': 'cards', 'data': <generator object MetabaseSource._get_data at 0x1022ceba0>}
{'table_name': 'collections', 'data': <generator object MetabaseSource._get_data at 0x1022cec80>}
{'table_name': 'dashboards', 'data': <generator object MetabaseSource._get_data at 0x1022cecf0>}
{'table_name': 'databases', 'data': <generator object MetabaseSource._get_data at 0x1022ced60>}
{'table_name': 'metrics', 'data': <generator object MetabaseSource._get_data at 0x1022cedd0>}
{'table_name': 'pulses', 'data': <generator object MetabaseSource._get_data at 0x1022cee40>}
{'table_name': 'tables', 'data': <generator object MetabaseSource._get_data at 0x1022ceeb0>}
{'table_name': 'segments', 'data': <generator object MetabaseSource._get_data at 0x1022cef20>}
{'table_name': 'users', 'data': <generator object MetabaseSource._get_data at 0x1022cef90>}
{'table_name': 'fields', 'data': <generator object MetabaseSource._get_field_data at 0x1022f1040>}
"""

for table in tables:
    with jsonlines.open(f"{table['table_name']}.jsonl", mode='w') as writer:
        writer.write_all(table['data'])


