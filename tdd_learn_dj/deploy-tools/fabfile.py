from fabric import task, Connection
from patchwork.files import append, exists
import random


# Fabric - Python-библиотека для удаленного выполнения команд на сервере.

REPO_URL = 'https://github.com/karpust/tdd_learn.git'


@task
def deploy(c):
    """Развернуть проект на сервере"""
    site_folder = f'/home/{c.user}/my_sites/{c.host}'  #  переназови хост!!
    source_folder = f'{site_folder}/tdd_learn'

    _create_directory_structure_if_necessary(c, site_folder)
    _get_latest_source(c, source_folder)
    _update_settings(c, source_folder, c.host)
    _update_virtualenv(c, source_folder)
    _update_static_files(c, source_folder)
    _update_database(c, source_folder)

"""
c — это параметр, который передаётся в функцию при вызове задачи, 
если задача объявлена с помощью декоратора @task в Fabric.
Когда запускается команда через fab deploy -H user@server, 
Fabric автоматически создаёт объект Connection и передаёт его в твою задачу.
(Fabric создает объект Connection для каждого указанного хоста.
Этот объект передаётся в задачу как аргумент c.
Ты вызываешь c.run("команда") для выполнения команд на удалённом сервере.

Что происходит: 
Когда выполняется команда через fab deploy -H user@server, 
Fabric автоматически подключается к серверу по SSH и 
создаёт объект Connection, который сохраняет все параметры подключения.
Этот объект передаётся в функцию задачи как c.
с - это экземпляр класса Connection, через него вызываем методы 
для выполнения команд на удалённом сервере.

"""
def _create_directory_structure_if_necessary(c, site_folder):
    """Создает структуру директорий, если ее нет"""
    for subfolder in ('database', 'static', 'my_env', 'tdd_learn'):
        c.run(f'mkdir -p {site_folder}/{subfolder}')
        # c.run() - выполнение команды в оболочке сервера


def _get_latest_source(c, source_folder):
    """Клонирует/обновляет репозиторий"""
    """
    ищем скрытую папку .git, чтобы проверить,
    был ли репозиторий уже клонирован в нее;
    используем f-строки, а не команды os.path.join,
    тк если сценарии выплняем из Windows,
    используем обратные косые,
    но на сервере нужны прямые косые!
    используем cd тк Fabric не помнит, в какой директории находимся
    
    c.local('git log -n 1 --format = %H', capture = True), 
    где:
    local - Execute a shell command on the local system.
    'git log -n 1 --format = %H' - 
    выведет последний коммит с полным хешем.
    (каждый коммит имеет уникальный 40-символьный SHA-1 хеш)
    capture = True - 
    выполнит команду локально и вернет её вывод
    
    git fetch загружает обновления из удалённого репозитория, 
    но не изменяет файлы в локальной копии.
    git reset --hard удаляет все незакоммиченые изменения(речь про сервер!)
    Если бы использовали git pull - возможны конфликты, 
    если есть локальные изменения. 
    git fetch + git reset --hard даёт жёсткую синхронизацию 
    с удалённым репозиторием.
    
    """

    if exists(c, source_folder + '/.git'):
        c.run(f'cd {source_folder} && git fetch')
    else:
        c.run(f'git clone {REPO_URL} {source_folder}')
    current_commit = c.local('git log -n 1 --format=%H', hide=True).stdout.strip()
    c.run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(c, source_folder, site_name):
    """Обновляет настройки Django"""

    """
    команда sed для замены текста:
    sed -i "s/старый_текст/новый_текст/" файл.py
    редактирует файл на месте - без создания временных копий
    sed — потоковый редактор, обрабатывает текст, -i - на месте;
    разрешаем только один хост в ALLOWED_HOSTS;
    если secret_key джанги есть в репозитории, то генерим новый,
    (между развертывания он не должен отличаться),
    сохраняем в файл и добавляем в settings.py импорт из него.
    
    """
    # settings_path = f'{source_folder}/tdd_learn_dj/settings.py'
    settings_path = f'{source_folder}/tdd_learn_dj/tdd_learn_dj/settings.py'
    c.run(f'sed -i "s/DEBUG = True/DEBUG = False/" {settings_path}')
    c.run(f'sed -i "s/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = [\'{site_name}\']/" {settings_path}')

    # secret_key_file = source_folder + '/tdd_learn_dj/secret_key.py'
    secret_key_file = source_folder + '/tdd_learn_dj/tdd_learn_dj/secret_key.py'
    if not exists(c, secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(c, secret_key_file, f'SECRET_KEY = "{key}"')
    append(c, settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(c, source_folder):
    """Обновляет зависимости в виртуальном окружении"""

    virtualenv_folder = f'{source_folder}/../my_env'
    if not exists(c, f'{virtualenv_folder}/bin/pip'):
        c.run(f'python3 -m venv {virtualenv_folder}')
    c.run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(c, source_folder):
    """Собирает статические файлы Django"""
    """
    строки без запятой между ними конкатенируются в одну
    поэтому можно смело дробить длинные строки.
    """
    c.run(f'cd {source_folder}/tdd_learn_dj'
          f'&& ../../my_env/bin/python manage.py collectstatic --noinput')


def _update_database(c, source_folder):
    """Применяет миграции базы данных"""
    """
    --noinput удаляет интерактивные подтверждения типа да/нет, 
    с которыми Fabric не справится.
    
    """
    c.run(f'cd {source_folder}/tdd_learn_dj && ../../my_env/bin/python manage.py migrate --noinput')
