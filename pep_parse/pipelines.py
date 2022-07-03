import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILENAME = 'status_summary_{now_formatted}.csv'


class PepParsePipeline:
    def __init__(self):
        self.result_dir = BASE_DIR / 'results'
        self.result_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.results = defaultdict(int)

    def process_item(self, item, spider):
        self.results[item['status']] += 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        filename = FILENAME.format(now_formatted=now_formatted)
        file_path = self.result_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows([
                ('Статус', 'Количество'),
                *self.results.items(),
                ('Total', sum(self.results.values()))
            ])
