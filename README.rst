Описание
===========

Выполняет слинияние из SRC_BRANCH в DST_BRANCH
Запускать нужно в каталоге с репозиторием, мерж со squash определяет по коммитному сообщению =(
Не умеет разрешать конфликты

    usage: gitmerge [-h] [-d] SRC_BRANCH DST_BRANCH

    Git merge branch tool

    positional arguments:
      SRC_BRANCH   source branch
      DST_BRANCH   destination branch

    optional arguments:
      -h, --help   show this help message and exit
      -d, --debug  debug output
