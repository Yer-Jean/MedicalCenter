

## Требования для работы программы
- Сервер PostgreSQL (локальный или удаленный) с имеющейся на нем, установленной по умолчанию, базой данных postgres
- Отредактированный файл example.env, находящийся в корневой директории проекта, согласно параметрам доступа к
имеющемуся серверу PostgreSQL, а также другим настройкам. Затем этот файл необходимо переименовать в .env
- Установленные зависимости, указанные в файле requirements.txt командой ***pip install -r requirements.txt***
- Необходимо действия:
  - создать на сервере PostgreSQL пустую базу данных с именем, указанном в файле .env (POSTGRES_DB)
  - применить к этой БД миграции из проекта командой python manage.py migrate
  - создать superuser'а командой ***python manage.py create_super_user [email] [first_name] [last_name] [password]***
  - создать в БД группы пользователей managers и doctors и присвоить им кастомные права командами
    - ***python manage.py create_user_group managers set_promo_active_status*** 
    - ***python manage.py create_user_group doctors modify_tests_results***
  - заполнить БД тестовыми данными из файлов main_data.json и promo_data.json командами
    - ***python manage.py loaddata users_data.json***
    - ***python manage.py loaddata main_data.json***
    - ***python manage.py loaddata promo_data.json*** 

