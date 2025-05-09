# Setup

## Necessary tooling
* python > 3
* wsl2
* [postman](https://www.postman.com/) 
* [podman](https://podman.io/)
* [mysql shell](https://dev.mysql.com/downloads/shell/)

## Database

```powershell
podman machine stop;podman machine start;
podman start bank_app;
```
or with migration of db schemas:
```powershell
podman rm bank_app;
podman run --name bank_app -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql
```
In mysql shell:
```powershell
\connect root:password@localhost:3306
```
or in powershell
```powershell
mysqlsh
```

## Running applications

### Running backend
```powershell
python -m controller.MainBankController
```

### Running frontend
```powershell
python -m webapp.FrontEndController
```
