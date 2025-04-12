# Setup

## Necessary tooling
* python > 3
* wsl2
* [postman](https://www.postman.com/) 
* [podman](https://podman.io/)
* [mysql shell](https://dev.mysql.com/downloads/shell/)

## Database

```commandline
 podman run --name bank_app -e MYSQL_ROOT_PASSWORD=password -d mysql
```
In mysql shell:
```commandline
 \connect root:password@localhost:3306
```