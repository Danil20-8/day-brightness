# Установка и использользование

1. Склонировать проект
2. Выполнить скрипт setup.sh - он установит необходимые зависимости
3. Добавить строку в cron `*/1 * * * * bash '/{path to project}/day-brightness/update-brightness.sh'`
   1. Выполнить команду `sudo crontab -e` для открытия редактора cron
   2. Добавить в конец файла указанную выше строку

Результатом станет автозапуск скрипта обновления яркости экрана каждую минуту. На данный момент установлено определение яркости по фото с камеры.

# Системные требования

- Работа скрипта проверена на `Ubuntu 22.04`
- На данный момент поддерживаются только видеокарты `Intel`
- Скрипт работает только под пользователем `root`, поэтому требует запуск cron от пользователя root
- При использовании автояркости от времени с учётом таблицы положения солцна требуется подключение к интернету 1 раз в год
