#! /usr/bin/env python
# -*- coding: utf-8 -*-


class GitException(Exception):
    """
    Git error
    """
    pass


class BanchNotExistException(Exception):
    """
    Branch does not exist
    """
    pass


class MergeException(Exception):
    """
    Merge error
    """
    pass