import jsonlines
from typing import Iterator

from dlt.common import json
from dlt.common.typing import DictStrAny, StrOrBytesPath

from os import listdir
from os.path import isfile, join
import os

current_path = os.path.dirname(os.path.abspath(__file__))
data_folder_path = join(current_path, 'sample_data')
metabase_files = [join(data_folder_path, f) for f in listdir(data_folder_path) if isfile(join(data_folder_path, f)) ]


class MetabaseMockSource:

        """  A list of tables that can be passed to get_table_rows() to get an interator of rows

            Metabase publishes logs to a buffer that keeps a running window.
            depending on how many events are generated in your instance,
            you might want to schedule a read every few minutes or every few days.

            They are set to "append-only" mode, so deduplication will be done by you by your optimal cost scenario
        """
        event_window_tables = ['activity', 'logs']

        """ returns a list of available tasks (to get data sets).
            pass them to get_endpoint_rows() to get an iterator of rows.
            These are stateful and should be replaced
        """
        stateful_tables = ['stats', 'cards', 'collections', 'dashboards', 'databases',
                           'metrics', 'pulses', 'tables', 'segments', 'users', 'fields']

        def __init__(self, url: str, user: str, password: str) -> None:
            pass

        def get_file_names(self):
            current_path = os.path.dirname(os.path.abspath(__file__))
            data_folder_path = join(current_path, 'sample_data')
            files = [join(data_folder_path, f) for f in listdir(data_folder_path) if isfile(join(data_folder_path, f))]
            return files

        def get_table_rows(self, tablename: StrOrBytesPath) -> Iterator[DictStrAny]:
            current_path = os.path.dirname(os.path.abspath(__file__))
            data_folder_path = os.path.join(current_path, 'sample_data')
            file_path = os.path.join(data_folder_path, f'{tablename}')
            with open(file_path, "r", encoding="utf-8") as f:
                yield from jsonlines.Reader(f, loads=json.loads)

        def tasks(self):
            files = self.get_file_names()
            tsks = [dict(table_name = os.path.basename(f.replace('.jsonl', '')),
                         data = self.get_table_rows(os.path.basename(f)))
                    for f in files]

            return tsks