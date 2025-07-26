import argparse
import json
from datetime import datetime
from abc import ABC, abstractmethod

import tabulate


class Report(ABC):
    @abstractmethod
    def _create_report(self, files: list[str]) -> None:
        pass

    @abstractmethod
    def print_report(self):
        pass


class ReportUserAgent(Report):  # future report
    def _create_report(self, files: list[str]) -> None:
        pass

    def print_report(self):
        pass


class ReportAverage(Report):
    def __init__(self, files: list[str], date_report: str | None):
        self.handlers: dict[str, dict[str, int | float]] = {}
        self.date_report: str | None = date_report
        self._create_report(files)

    def _create_report(self, files: list[str]) -> None:
        if self.date_report:
            for line in read_files(files):
                if datetime.strptime(line['@timestamp'][0:10], '%Y-%m-%d') == self.date_report:
                    self._counter_handler_avg_time(line['url'], line['response_time'])
        else:
            for line in read_files(files):
                self._counter_handler_avg_time(line['url'], line['response_time'])

    def _counter_handler_avg_time(self, handler: str, response_time: float) -> None:
        if handler not in self.handlers:
            self.handlers.setdefault(handler, {'total': 1})
            self.handlers[handler]['sum_response_time'] = response_time
        else:
            self.handlers[handler]['total'] += 1
            self.handlers[handler]['sum_response_time'] += response_time

    def print_report(self):
        if not self.handlers:
            return []
        headers: list[str] = ['handler', 'total', 'avg_response_time']
        handlers: list[list] = [[i, j['total'], round(j['sum_response_time'] / j['total'], 3)] for i, j in
                                self.handlers.items()]
        handlers_sort: list[list] = sorted(handlers, key=lambda x: x[1], reverse=True)
        print(tabulate.tabulate(handlers_sort, headers=headers))


def processing_parameters(arg_list: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Script for processing log file')
    parser.add_argument('--file', '--list', nargs='+', help='<Required> File path', required=True)
    parser.add_argument(
        '--report',
        type=str,
        choices=['average'],
        help='Choose a report from the available options.',
        required=True
    )
    parser.add_argument('--date', type=lambda s: datetime.strptime(s, '%Y-%d-%m'))
    return parser.parse_args(arg_list)


def selection_report(name_report: str, files: list[str], date_report: str):
    rep = None
    if name_report == 'average':
        rep = ReportAverage(files, date_report)
    return rep


def read_files(files: list[str]):
    for file in files:
        try:
            with (open(file, 'r') as log):
                for line in log.readlines():
                    yield json.loads(line)
        except IOError as e:
            print(f'Файл {file} не найден')


def main(arg_list: list[str] | None = None):
    args: argparse.Namespace = processing_parameters(arg_list)
    report = selection_report(args.report, args.file, args.date)
    report.print_report()


if __name__ == '__main__':
    main()