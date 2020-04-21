## Full Stack Web App Template - FARM Stack

This repository contains a full stack web application template that runs on the FARM solution stack, which stands for:
- **F**lask, a backend **Python** web framework.
- **A**mazon Web Services, a cloud service that can host software.
- **R**eact, a frontend **JavaScript** web framework.
- **M**ySQL, a relational database management system.

## What is FARM?
The FARM stack is more or less an extension of the LAMP stack with these notable changes:
- The middleware framework is explicit (Flask)
- Like the MEAN stack, it includes an application presentation layer (React)
- The environment which the software runs on is instead replaced by PaaS/IaaS cloud computing services (AWS)
- There is no opinion for which operating system to use

### Flask
Flask is used to write the web APIs / middleware that can communicate between the web UI and the web backend / database. This is the core of the entire application that glues the pieces of the full stack application together.

Note that this particular template does not use an ORM, and instead uses the `pymysql` module. This means developers need to write SQL queries, but can maximize the complexity of the queries they need to run on the database.

### Amazon Web Services
AWS is the cloud service which the application can be hosted on. We can host the entire software stack on the following services:
- **AWS Lambda** for hosting our applications on a serverless infrastructure. We can also choose to host our Flask APIs via [Zappa](https://github.com/Miserlou/Zappa), making deployment to production exceedingly easy.
- **AWS RDS** for hosting our database. 
- **AWS S3** for storing all sorts of other objects like images and files.

This means that developers can keep everything on one platform and minimize DevOps / IT work.

### React
React is the framework which the web UI runs on. The React application may also be run on AWS Lambda with NodeJS.

This template uses JavaScript / JSX, but TypeScript may be used as well.

### MySQL
MySQL is the relational database which the web backend uses. This can also be hosted on AWS through its RDS service.

## How to Run Locally
To run this web application, the following needs to be done:
1. Setup a local MySQL instance using the schema in `db/`
2. Install modules for the API and UI
3. Run the API and UI locally

### Database Setup
To set up the MySQL instance, follow these steps:
1. Create and connect to a MySQL database instance. The most common ways to do this are with MySQL Workbench or `mysql` on the Linux command line interface.
2. Run `sample.sql` within the instance. It will create a schema called `SampleInventory` and then initialize a table called `Inventory`.

### API Setup
The codebase for the Flask API can be found in the `api/` directory.

#### First-time Setup (macOS)
1. Create a Python virtual environment with `virtualenv farm-stack` after navigating to that directory.
2. Activate it with `source farm-stack/bin/activate`
3. Navigate to `api/` and run `pip3 install -r requirements.txt` to install all Python modules necessary for the API.
4. Open `dbcreds.py` in the `api/` directory and edit database credentials as needed.

#### Running the API
1. Activate the virtual environment from above.
2. Run `python3 app.py` to run the API on `http://localhost:8080`.

### UI Setup
The codebase for the React UI can be found in the `ui/` directory. This template uses `yarn` as its package manager; it is crucial that developers do not mix other package managers like `npm` when adding new modules.

Note that packages like `react-bootstrap` are missing from this template.

#### First-time Setup (macOS)
1. Run `yarn install` to install all dependencies required.

#### Running the UI
1. Run `yarn start` to run in development mode.
2. Navigate to `http://localhost:3000` on the browser.
