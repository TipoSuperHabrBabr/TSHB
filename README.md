## Проект "TipoSuperHabrBabr"
## Командная разработка по методологии Agile:Scrum

### Базовая документация к проекту

Стек:

* Ubuntu 22.04.1 LTS
* Python 3.10
* Django 4.1.2
* SQLite3
* HTML/CSS
* GitHub

### Установка необходимого ПО
#### обновляем информацию о репозиториях
```
apt update
```
#### Установка СУБД SQLite3, Git, virtualenv
СУБД SQLite3
```
apt install sqlite3
```
Git
```
apt install git-core
```
virtualenv
```
apt install python3-venv
```
#### Настраиваем виртуальное окружение
При необходимости, для установки менеджера пакетов pip выполняем команду:
```
apt install python3-pip
```
Создаем и активируем виртуальное окружение:
```
mkdir /opt/venv
python3 -m venv /opt/venv/tshb_env
source /opt/venv/tshb_env/bin/activate
```
Устанавливаем права:
```
chown -R hh /opt/venv/tshb_env
```
Клонируем репозиторий:
```
git clone https://github.com/TipoSuperHabrBabr/TSHB.git /opt/venv/tshb_env/src
cd tshb_env/
```
Устанавливаем Django 4.1.2:
```
pip3 install Django==4.1.2
```
#### Суперпользователь
```
python3 manage.py createsuperuser
```
к примеру (логин/пароль): admin:admin
#### Выполнение миграций и сбор статических файлов проекта
Создаем миграции:
```
python3 manage.py makemigrations
```
Выполняем миграции:
```
python3 manage.py migrate
```
#### Запускаем сервер
```
python3 manage.py runserver
```