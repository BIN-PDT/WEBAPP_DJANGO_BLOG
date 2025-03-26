**1. PROJECT**

```
git clone https://github.com/BIN-PDT/WEBAPP_DJANGO_WAGTAIL.git && rm -rf WEBAPP_DJANGO_WAGTAIL/.git
```

_For privacy reasons, replace the sensitive information in this project with your own._

-   _Generate `SECRET_KEY`_.

    ```
    python manage.py shell
    ```

    ```python
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    exit()
    ```

**2. VIRTUAL ENVIRONMENT**

```
python -m venv .venv
```

```
.venv\Scripts\activate.bat
```

**3. DEPENDENCY**

```
python.exe -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

**4. DATABASE**

```
python manage.py migrate
```

**5. RUN APPLICATION**

```
python manage.py runserver
```
