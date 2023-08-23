### Описание:

# test-task-phonebook.

Телефонный справочник, в котором можно создавать новые записи, редактировать старые, фильтровать по указанным параметрам и просматривать записи по страницам. Записи сохраняются в csv файле.

### Технологии

Python 3.7

pandas 2.0.3

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Sarugot/test-task-phonebook
```

```
cd test-task-phonebook
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python test_task_phonebook.py
```