# Django Template

## Structure

### **{{ your_project_name }} dir**

### **bin dir**

도커 환경 구성을 위한 전반적인 코드들이 존재하는 디렉토리로, 도커 실행을 위한 스크립트, 컴포즈 환경 구성을 위한 도커파일들이 존재한다.

- .envs
  서비스에 필요한 설정들(ex. DB URL, PW 등)을 분리하여 관리하기 위한 디렉토리다. 로컬(.local), 서비스(.production)용으로 구분되어있으며 서비스용은 공개된 저장소에 올라가지 않도록 주의할 필요가 있다.

- compose
  도커 컴포즈 환경을 구성할 때 각 도커 컨테이너를 구성하기 위한 도커파일들과 서버 실행(ex. start) 및 부가적으로 확인(ex. entrypoint)하기 위한 명령어들 또한 위치해 있다.

- requirements
  서버 운용에 필요한 패키지 파일들로, base, local, production 3가지로 구분되어 있다.

- local.yml & production.yml
  로컬 및 서비스 환경에 맞는 도커 컴포즈를 구성하기 위한 `docker-compose.yml` 파일이다.

- restart\_(local OR production)\_docker.sh
  도커 컴포즈 재실행을 위한 명령어를 모아둔 쉘 스크립트 파일이다.

## Usage

Template을 로컬에 클론한다

```bash
$ git clone https://github.com/bigpie1367/inco-django-template.git
```

이후 본인 프로젝트에 맞게 설정하기 위해 동봉된 파이썬 코드를 실행하여 프로젝트를 설정한다.

```python
$ python build_project.py

Enter the new project name:
Enter the new app name:
Use Celery:
Use Redis:
```

## Run Django Project

Run in local without docker

```bash
cd {{ your_project_name }}
python manage.py runserver
```

Run in local with docker

```bash
cd bin
sh restart_local_docker.sh
```

Run in production

```bash
cd bin
sh restart_production_docker.sh
```
