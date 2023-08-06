
from dlt_metabase_source.helpers import extract_data_and_prepare_schema, load_data
from dlt_metabase_source.metabase_source import MetabaseSource as DataSource
from dlt_metabase_source.metabase_mock_source import MetabaseMockSource as MockDataSource



# A pipeline is a collection of
# - Source data
# - Source metadata (Schema)
# - Destination mapping

# When we develop a pipeline, DLT helps us infers the Schema
# DLT's extract function reads source data and creates a schema file
# see method "extract_data_and_prepare_schema"

# Once the file is created, we might want to inspect it and manually curate it.
# In this example, i was unhappy with excessive unpacking,
# so I deleted the tables from the schema and added a max unnest level
# normalizers:
#  json:
#    config:
#      max_nesting: 1

# I also adjusted the write disposition for each table

# When running the extract again, the modified schema is read, and appended with
# the metadata generated according to the new normaliser instruction
# Our schema now contains less tables than the original

# Finally, once we are happy with the schema, we can just load the data according to it.

def load(url='https://metabase-analytics.scalevector.com/',
         user='example1@scalevector.ai',
         password='',
         # for target credentials, pass a client_secrets.json or a credential json suitable for your db type.
         target_credentials={},
         #default tables, remove some if you do not want all of them
         tables=['activity', 'logs', 'stats', 'cards', 'collections', 'dashboards', 'databases', 'metrics', 'pulses', 'tables', 'segments', 'users', 'fields'],
         schema_name = 'metabase',
         mock_data = False):

    if mock_data:
        source = MockDataSource(url='', user='', password='')
    else:
        source = DataSource(url=url, user=user, password=password)

    tables_to_load = [t for t in source.tasks() if t['table_name'] in tables]

    pipeline = None
    for table in tables_to_load:
        # we read the file "schema.yml" if it exists, if not we create it from data
        # if update_schema=True then we create/update the schema
        # if update_schema=false then we only read/use internal schema without outputting it.
        # When updated, the schema is not overwritten but extended, so most changes you make, persist.

        # The default table writing disposition is "append" so you might want to modify that first.

        #update_schema=True in development mode. False when we are satisfied and want to keep it set.
        pipeline = extract_data_and_prepare_schema(pipeline,
                                        table['data'],
                                        #target creds will be moved to load
                                        credentials=target_credentials,
                                        table_name=table['table_name'],
                                        schema_file='schema',
                                        update_schema=False)

        # Now that the schema is prepared, we can load based on it

    load_data(pipeline, credentials = target_credentials,
                  dataset_prefix='dlt',
                  dataset_name='metabase')

    print(f"loaded {','.join(tables)}")


if __name__ == "__main__":

    load(url='ht',
         user='e.ai',
         password='',
         # for target credentials, pass a client_secrets.json or a credential json suitable for your db type.
         target_credentials={"type": "service_account",
                  "project_id": "zinc-mantra-353207",
                  "private_key_id": "ffff",
                  "private_key": "ffff",
                  "client_email": "data-load-tool@zinc-mantra-353207.iam.gserviceaccount.com",
                  "client_id": "100909481823688180493"},
         # default tables, remove some if you do not want all of them
         tables=['activity', 'logs', 'stats', 'cards', 'collections', 'dashboards', 'databases', 'metrics', 'pulses',
                 'tables', 'segments', 'users', 'fields'],
         schema_name='metabase',
         mock_data=True)



