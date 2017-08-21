# -*- coding: utf-8 -*-
import os
import apache_log_parser


line_parser = apache_log_parser.make_parser(
    "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\""
)


def log1(l):
    return line_parser(l)

if __name__ == '__main__':
    for filename in os.listdir('logs/'):
        print('Processing ' + filename)
        with open('logs/' + filename) as f:
            for line in f:
                log1(line)
