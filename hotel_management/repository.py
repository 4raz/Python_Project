import csv
import os


class CSVRepository:
    def __init__(self, csv_path, headers, factory):
        self.csv_path = csv_path
        self.headers = list(headers)
        self.factory = factory
        folder = os.path.dirname(self.csv_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(self.csv_path):
            self._write_rows([])

    def list_all(self):
        with open(self.csv_path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return [self.factory(row) for row in reader]

    def save_all(self, items):
        rows = [item.to_dict() for item in items]
        self._write_rows(rows)

    def _write_rows(self, rows):
        with open(self.csv_path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.headers)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
