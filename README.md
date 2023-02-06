### Hexlet tests and linter status:
[![Actions Status](https://github.com/Zlober/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Zlober/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/a0650203237396645f3c/maintainability)](https://codeclimate.com/github/Zlober/python-project-lvl2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a0650203237396645f3c/test_coverage)](https://codeclimate.com/github/Zlober/python-project-lvl2/test_coverage)

https://python-project-52-production-e016.up.railway.app

A task management web application built with Python and Django framework. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

To provide users with a convenient, adaptive, modern interface, the project uses the Bootstrap framework.

The frontend is rendered on the backend. This means that the page is built by the DjangoTemplates backend, which returns prepared HTML. And this HTML is rendered by the server.

PostgreSQL is used as the object-relational database system.

### Installation
To use the application, you need to clone the repository to your computer. This is done using the git clone command. Clone the project:

>> git clone https://github.com/ivnvxd/python-project-52.git && cd python-project-52

Then you need to install all necessary dependencies:

>> make install

Create .env file in the root folder and add following variables:

>> DB = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}

>> SECRET_KEY = '{your secret key}'

>> access_token = '{your Rollbar token}'

To create the necessary tables in the database, start the migration process
>> make migrate

