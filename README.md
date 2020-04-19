## Full Stack Web App Template - FARM Stack

This repository contains a full stack web application template that runs on the FARM solution stack, which stands for:
- **F**lask, a backend **Python** web framework.
- **A**mazon Web Services, a cloud service that can host software.
- **R**eact, a frontend **JavaScript** web framework.
- **M**ySQL, a relational database management system.

This particular template does not use an ORM, and there is no opinion for what operating system to use.

### Flask
Flask is used to write the web APIs / middleware that can communicate between the web UI and the web backend / database. This is the core of the entire application that glues the pieces of the full stack application together.

### Amazon Web Services
AWS is where the different pieces of the application are hosted. We can use the following services:
- **AWS Lambda** for hosting our applications on a serverless infrastructure. We can also choose to host our Flask APIs via [Zappa](https://github.com/Miserlou/Zappa), making deployment to production exceedingly easy.
- **AWS RDS** for hosting our database. 
- **AWS S3** for storing all sorts of other objects like images and files.

### React
React is the framework which the web UI runs on. The React application may also be run on AWS Lambda with NodeJS.

### MySQL
MySQL is the relational database which the web backend uses.
