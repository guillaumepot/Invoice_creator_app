# Invoice Creator App


Simple invoice generator using flask.


<img src="./media/img.jpeg" width="350" height="350">



## Current Features

- Start flask app & generate invoices using the script in utils


## Project Information

- **Version**: 1.0.0
- **Development Stage**: Prod
- **Author**: Guillaume Pot

[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/062guillaumepot/)




## Table of Contents
- [Installation](#installation)
    - [Requirements](#requirements)
- [Repository](#repository)
    - [Architecture](#architecture)
    - [Branch Policy](#branch-policy)
    - [Changelogs](#changelogs)
    - [Roadmap](#roadmap)
    - [Contributions](#contirbutions)
- [Miscellaneous](#miscellaneous)




## Installation

- Create a venv with requirements
- Start flask app
- Use generate_invoice.py script to generate invoices


### Requirements

- python
- flask
- weasyprint
- requests



## Repository



### Architecture


```
|
├── changelogs
|
├── documents          # Generated invoices are stored here
|
├── media               # General purpose files like imgs, txt used in the repository
|
├── src                 # Contains source files for app | modules
|    |
|    ├── static         # static files
|    |
|    ├── templates      # html templates
|    |
|    ├── app.py         # flask app
|    |
|    └── config.py      # flask config
|
├── utils               # Contains sscripts
|
├── LICENSE
|
├── README.md
|
└── requirements.txt    # Dependencies for flask app & scripts
```


### Branch Policy

```
├── main    # Main branch, contains releases
|   
├── build   # Used to build releases
|
├── debug   # Debug branch
|
└── develop # New features development branch
```


### Changelogs

[v1.0.0](./changelogs/1.0.0.md)
[v0.0.2](./changelogs/0.0.2.md)
[v0.0.1](./changelogs/0.0.1.md)



### Roadmap

```
-
```


### Contributions

```
-
```




## Miscellaneous

```
-
```