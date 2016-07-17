#! /usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import sys
import logging
from tool import Repository
from exceptions import GitException, BanchNotExistException, MergeException

_logger = logging.getLogger(__name__)


def merge(args):
    """
    Выполнение мержа из SRC_BRANCH в DST_BRANCH
    Если мерж уже был, удаляем этот коммит (остальные оставляем) и делаем его снова
    :param args:
    :return:
    """

    repo = Repository('.')

    try:
        commit = repo.branch_is_merged(args.SRC_BRANCH, args.DST_BRANCH)

        if commit:
            repo.delete_merge(args.DST_BRANCH, commit)
            repo.merge(args.SRC_BRANCH, args.DST_BRANCH)
        else:
            repo.merge(args.SRC_BRANCH, args.DST_BRANCH)
    except BanchNotExistException as e:
        _logger.error('branch does not exist')
    except MergeException as e:
        _logger.error('merge error')
    except GitException as e:
        _logger.error('git error')


def config(args):
    """
    Настройка логгирования
    :param args:
    :return:
    """

    if args.debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)

    f = logging.Formatter('%(levelname)s %(message)s')
    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(f)

    logging.root.addHandler(handler)

    _logger.debug('Starting mergetool')


def parse_args():
    """
    Парсинг командной строки
    :return:
    """

    parser = argparse.ArgumentParser(description='Git merge branch tool')
    parser.set_defaults(func=merge)
    parser.add_argument("SRC_BRANCH",
                        help="source branch")
    parser.add_argument("DST_BRANCH",
                        help="destination branch")
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="debug output")
    return parser.parse_args()



def main():
    args = parse_args()
    config(args)
    args.func(args)



