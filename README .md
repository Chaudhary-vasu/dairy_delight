
# Dairy Delight

A new E-commerce web application to meet your Daily Dairy products requirements. I have developed this application using Django framework with postgres integration of database.

#### Technologies used in the project:

- HTML, CSS and JavaScript (Frontend)
- Django framework (Backend)

## Features

- welcome landing page and designed logo
- select dairy products like milk,cheese from menu
- cart overlay
- add dairy products in cart
- order dairy products from cart
- remove and add items in cart
- checkout panel for ordering products
- Payment gateway using razorpay


## Software Required

- Django (LTS version)
- Python (version - 3.10.7)
- VS Code
- Postgres

## Installation Steps

- Install all the required softwares properly.

- Open the "ecommerce" folder in any code editor (for example: VS Code).

- Now open the terminal in the editor.

- To install all of Python's required packages and libraries, we must execute:

```cmd
    pip install -r requirements.txt     (for windows)
    pip3 install -r requirements.txt     (for mac)
```

- After successful installation of all the packages.

- Now we setup Postgres, for this you have to make database in PgAdmin of Postgres.

- After this, In settings.py add <NAME_OF_YOUR_DATABASE> and <PASSWORD> :

```code
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": <NAME_OF_YOUR_DATABASE>,
        "USER": "postgres",
        "PASSWORD": <PASSWORD>,
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

- After this, we have to create tables in database, for this we can run following command on terminal:
```cmd
    python manage.py makemigrations
    python manage.py migrate
```

- Now run the following command:
```cmd
    python manage.py runserver
```

- Now all set, a web page will appear on the [Local Server](http://localhost:8000/), where you can login and signup and access dairy delight features.

**Note**:
- Create the virtualenv in python for good practice.
- After the server start, to signup and login tap on login and signup respectively.







