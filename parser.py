# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from datetime import datetime
#from concurrent.futures import ThreadPoolExecutor

from pyArango.connection import Connection


MONTHS = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}


def log1(l):
    return {
        'ip': l.split(' ')[0],
        'date': l.split('[')[1].split(']')[0],
        'method': l.split('"')[1].split(' ')[0],
        'path': l.split(' ')[6],
        'status': l.split(' ')[8],
        'agent': l.split('"')[5]
    }


def parse_date(l):
    d = datetime.strptime(l['date'], '%d/%b/%Y:%H:%M:%S %z')
    l['date'] = d
    return l


def parse_date_speed(l):
    dt = l['date']
    date = dt[7:11], MONTHS[dt[3:6]], dt[:2], dt[12:14], dt[15:17], dt[18:20]
    date = [int(dt) for dt in date]
    l['date'] = datetime(*date)
    return l


def task(line):
    l = log1(line)
    #l = parse_date_speed(l)
    return l


def worker(lines, coll):
    docs = []
    for line in lines:
        l = task(line)
        docs.append(l)

    coll.importBulk(docs)


if __name__ == '__main__':
    conn = Connection(username='user', password='pass')
    db = conn['_system']
    try:
        coll = db.collections['logs']
    except KeyError:
        coll = db.createCollection(name=str("logs"))

    #pool = ThreadPoolExecutor(max_workers=8)
    for filename in os.listdir('logs/'):
        print('Processing ' + filename)

        lines = []
        with open('logs/' + filename) as f:
            for i, line in enumerate(f, 1):
                lines.append(line)
                if i % 2000 == 0:
                    #pool.submit(worker, lines, coll)
                    worker(lines, coll)
                    lines = []

            #pool.submit(worker, lines, coll)
            worker(lines, coll)
