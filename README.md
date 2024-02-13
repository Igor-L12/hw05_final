# Соцсеть Yatube
Социальная сеть блогеров. Повзоляет написание постов и публикации их в отдельных группах, подписки на посты, добавление и удаление записей и их комментирование. Подписки на любимых блогеров.


Стек:

- Python 3.10.5
- Django==2.2.28
- mixer==7.1.2
- Pillow==9.0.1
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- requests==2.26.0
- six==1.16.0
- sorl-thumbnail==12.7.0
- Pillow==9.0.1
- django-environ==0.8.1

### Настройка и запуск на ПК

Клонируем проект:

```bash
git clone https://github.com/Igor-L12/hw05_final.git
```

Переходим в папку с проектом:

```bash
cd hw05_final
```

Устанавливаем виртуальное окружение:

```bash
python -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/Scripts/activate
```

> Для деактивации виртуального окружения выполним (после работы):
> ```bash
> deactivate
> ```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python yatube/manage.py makemigrations
python yatube/manage.py migrate
```

Создаем супер пользователя:

```bash
python yatube/manage.py createsuperuser
```

При желании делаем коллекцию статики (часть статики уже загружена в репозиторий в виде исключения):

```bash
python yatube/manage.py collectstatic
```


```bash
SECRET_KEY='Ваш секретный ключ'
ALLOWED_HOSTS='127.0.0.1, localhost'
DEBUG=True
```

Для запуска тестов выполним:

```bash
pytest
```

Получим:

```bash
pytest
=================================================== test session starts ===================================================
platform win32 -- Python 3.9.10, pytest-6.2.4, py-1.11.0, pluggy-0.13.1 -- C:\Dev\hw05_final\venv\Scripts\python.exe
django: settings: yatube.settings (from ini)
rootdir: C:\Dev\hw05_final, configfile: pytest.ini, testpaths: tests/
plugins: Faker-12.0.1, django-4.4.0, pythonpath-0.7.3
collected 32 items

tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_view_get PASSED                                                                                                                      [  3%]
tests/test_paginator.py::TestGroupPaginatorView::test_group_paginator_not_in_context_view PASSED                                                                                                           [  6%]
tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_not_in_view_context PASSED                                                                                                           [  9%]
tests/test_paginator.py::TestGroupPaginatorView::test_index_paginator_view PASSED                                                                                                                          [ 12%]
tests/test_paginator.py::TestGroupPaginatorView::test_profile_paginator_view PASSED                                                                                                                        [ 15%]
tests/test_about.py::TestTemplateView::test_about_author_tech PASSED                                                                                                                                       [ 18%]
tests/test_auth_urls.py::TestAuthUrls::test_auth_urls PASSED                                                                                                                                               [ 21%]
tests/test_comment.py::TestComment::test_comment_add_view PASSED                                                                                                                                           [ 25%]
tests/test_comment.py::TestComment::test_comment_add_auth_view PASSED                                                                                                                                      [ 28%]
tests/test_create.py::TestCreateView::test_create_view_get PASSED                                                                                                                                          [ 31%]
tests/test_create.py::TestCreateView::test_create_view_post PASSED                                                                                                                                         [ 34%]
tests/test_follow.py::TestFollow::test_follow_not_auth PASSED                                                                                                                                              [ 37%]
tests/test_follow.py::TestFollow::test_follow_auth PASSED                                                                                                                                                  [ 40%]
tests/test_homework.py::TestPost::test_post_create PASSED                                                                                                                                                  [ 43%]
tests/test_homework.py::TestGroup::test_group_create PASSED                                                                                                                                                [ 46%]
tests/test_homework.py::TestGroupView::test_group_view PASSED                                                                                                                                              [ 50%]
tests/test_homework.py::TestCustomErrorPages::test_custom_404 PASSED                                                                                                                                       [ 53%]
tests/test_homework.py::TestCustomErrorPages::test_custom_500 PASSED                                                                                                                                       [ 56%] 
tests/test_homework.py::TestCustomErrorPages::test_custom_403 PASSED                                                                                                                                       [ 59%]
tests/test_post.py::TestPostView::test_index_post_with_image PASSED                                                                                                                                        [ 62%]
tests/test_post.py::TestPostView::test_index_post_caching PASSED                                                                                                                                           [ 65%]
tests/test_post.py::TestPostView::test_post_view_get PASSED                                                                                                                                                [ 68%]
tests/test_post.py::TestPostEditView::test_post_edit_view_get PASSED                                                                                                                                       [ 71%]
tests/test_post.py::TestPostEditView::test_post_edit_view_author_get PASSED                                                                                                                                [ 75%]
tests/test_post.py::TestPostEditView::test_post_edit_view_author_post PASSED                                                                                                                               [ 78%]
tests/test_profile.py::TestProfileView::test_profile_view_get PASSED                                                                                                                                       [ 81%]
tests/test_comment.py::TestComment::test_comment_model PASSED                                                                                                                                              [ 84%] 
tests/test_follow.py::TestFollow::test_follow[author] PASSED                                                                                                                                               [ 87%] 
tests/test_follow.py::TestFollow::test_follow[user] PASSED                                                                                                                                                 [ 90%] 
tests/test_homework.py::TestPost::test_post_model PASSED                                                                                                                                                   [ 93%] 
tests/test_homework.py::TestPost::test_post_admin PASSED                                                                                                                                                   [ 96%] 
tests/test_homework.py::TestGroup::test_group_model PASSED                                                                                                                                                 [100%] 

============================================================================================== 32 passed in 14.30s ============================================================================================== 
```

Запускаем проект:

```bash
python yatube/manage.py runserver localhost:80
```

После чего проект будет доступен по адресу http://localhost/80

Заходим в http://localhost/admin и создаем группы и записи.
После чего записи и группы появятся на главной странице.

Автор: [Игорь Любаев](https://github.com/Igor-L12)
