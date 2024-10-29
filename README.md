# Шаблонный Телеграм бот для Хакатона

### Запуск:

1. #### Указать переменные окружения в _.\\deployments\\.env_
* TELEGRAM_API_TOKEN - Токен телеграм-бота. Получить можно [тут](https://t.me/BotFather)
* ADMIN_ID - TG ID адмиистратора, которому будут приходить уведомления о старте/завершении работы телеграм-бота
* URL_TO_API - URL для отправки запросов
* HOST_DB - хост сервера базы данных
* PORT_DB - порт сервера базы данных
* USER_DB - логин к серверу базы данных
* PASSWORD_DB - пароль к серверу базы данных
* NAME_DB - наименование базы данных

2. #### Заменить на корректные значения (TODO метка) в файле _source\handlers\user_handlers.py_

3. #### Собрать Docker образ и запустить его
```bash
docker compose -f .\deployments\docker-compose.yml build
docker compose -f .\deployments\docker-compose.yml up
```