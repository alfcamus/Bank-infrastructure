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
use bank_infrastructure;
```

or in powershell

```powershell
mysqlsh
```

## Running applications

### Running backend

```powershell
C:\progs\GettingStarted\Bank-infrastructure

python -m controller.main_bank_controller
```

### Running frontend

```powershell
python -m webapp.frontend_controller
```

## Podman/Docker deployment

```commandline
podman build . -t bankinfra_frontend:latest Front.Dockerfile
podman build . -t bankinfra_backend:latest Main.Dockerfile
podman-compose up
```