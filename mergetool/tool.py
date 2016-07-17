#! /usr/bin/env python
# -*- coding: utf-8 -*-

import git
import logging
from git.exc import InvalidGitRepositoryError, NoSuchPathError, GitCommandError, GitCommandNotFound
from exceptions import GitException, BanchNotExistException, MergeException
import re
import random, string


_logger = logging.getLogger(__name__)

class Repository(object):

    # Сообщение для коммита
    _commit_message = 'Squashed commit of '

    def __init__(self, dir='.'):
        """

        :param dir:
        :return:
        """

        _logger.debug('Use directory %s' % dir)

        try:
            self._repo = git.Repo(dir)

        except NoSuchPathError as e:
            msg = 'No sush repository on path: %s' % e
            _logger.error(msg)
            raise GitException(msg)

        except InvalidGitRepositoryError as e:
            msg = 'Invalid git repository on path: %s' % e
            _logger.error(msg)
            raise GitException(msg)


        self._git = self._repo.git



    def _branch_is_exist(self, name):
        """
        Проверка на существование бранча
        :param name:
        :return:
        """

        for b in self._repo.branches:
            if b.name.lower() == name.lower():
                return True

        return False



    def get_all_commits(self, branch):
        """
        Возвращает список всех коммитов из бранча
        :param branch: имя бранча
        :return: список коммитов
        """

        return self._repo.iter_commits(branch)

    def get_last_commit(self, branch):
        """
        Возвращает самый последний коммит из бранча
        :param branch: имя бранча
        :return: коммит
        """

        for i in self._repo.iter_commits(branch):
            return i
        return None


    def branch_is_merged(self, src_branch, dst_branch):
        """
        Так как мердж со squash не является коммитом слияния, то определяем что был мерж из сообщения в коммите
        Если пользуемся только этой утилитой, то проблем быть не должно :)
        Либо, наверное, еще вариант сложнее -- проходить по файлам в src_branch и делать diff с двух коммитов
        в dst_branch (?)

        :param src_branch:
        :param dst_branch:
        :return: Возвращает Commit, в котором бранч src_branch был вмержен в dst_branch или None
        """

        # проверяем, существуют ли бранчи
        if not self._branch_is_exist(src_branch) or not self._branch_is_exist(dst_branch):
            raise BanchNotExistException('Branch %s or %s not exist' % (src_branch, dst_branch))

        # ищем мерж по сообщению :)
        for dst in self.get_all_commits(dst_branch):
            branch_merged = re.search('^%s(.*?)$' % self._commit_message, dst.message, re.IGNORECASE)
            if branch_merged:
                branch_name = branch_merged.group(1)
                if branch_name.lower() == src_branch.lower():
                    _logger.debug('Found squashed commit of %s' % branch_name)
                    return dst

        return None



    def merge(self, src_branch, dst_branch):
        """
        Выполняет merge
        FIXME конфликты не разрешаются

        :param src_branch:
        :param dst_branch:
        :return:
        """
        try:
            self._git.checkout(dst_branch)
            self._git.merge('--squash', src_branch)
        except GitCommandError as e:
            _logger.debug('git error %s' % e)
            raise MergeException(e)
        except GitCommandNotFound as e:
            _logger.debug('git command not found %s' % e)
            raise MergeException(e)

        self._repo.index.commit('%s%s' % (self._commit_message, src_branch))


    def get_last_commit(self, branch, commit):
        """
        Ищет коммит, предшествующий удаляемому commit

        :param branch: бранч для просмотра
        :param commit: коммит, который надо удалить
        :return: коммит, предшествующий удаляемому коммиту
        """

        is_skiped = False   # флаг, что добрались до коммита, который надо удалить

        for cm in self.get_all_commits(branch):

            if is_skiped:
                return cm

            if cm == commit:
                is_skiped = True

        return None



    def delete_merge(self, branch, commit):
        """
        Удаляет из branch коммит commit, все остальные сохраняет

        :param branch: бранч, откуда удаляем
        :param commit: коммит, который удаляем
        :return:
        """

        random_branch = 'tmp_%s' % ''.join(random.choice(string.lowercase) for i in range(8))

        _logger.debug('temp branch name is %s' % random_branch)

        last_commit = self.get_last_commit(branch, commit)

        if not last_commit:
            # FIXME: если не нашли коммит, предшествующий удаляемому, отваливаемся, не хватило времени доделать ))
            _logger.error('Last commit not found. Not implement :)')
            raise MergeException

        try:
            self._git.checkout(last_commit)

            self._git.checkout('-b', random_branch)

            for cm in self.get_all_commits(branch):

                # переносим все коммиты, до удаляемого
                if cm != commit:
                    self._git.cherry_pick(cm)
                else:
                    break

            self._git.checkout(branch)
            self._git.reset('--hard', last_commit)
            self._git.merge(random_branch)
            # TODO вынести в finally
            self._git.branch('-D', random_branch)


        except GitCommandError as e:
            _logger.debug('git error %s' % e)
            raise MergeException(e)
        except GitCommandNotFound as e:
            _logger.debug('git command not found %s' % e)
            raise MergeException(e)

