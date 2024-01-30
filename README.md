# Django Template

## Structure

### **{{ your_project_name }} dir**

Django 프로젝트를 서비스하기 위한 디렉토리이다.

- **config**

  Django 서버를 호스팅하기 위한 설정들이 존재하는 디렉토리로, 각 환경에 맞는 settings 파일(base, local, production.py)들과 asgi, wsgi, urls, celery_app 파일들이 존재한다.

  사용할 때 로컬 환경에서 DB 테스트틑 위해 `settings/base.py` 내 `DATABASE` 설정을 해주어야 한다.

- **{{your_app_name}}**

  기존 `python manage.py startapp` 명령어를 통해 생성된 app 디렉토리와 동일하다. 기본적으로 `AbstractUser`를 상속받은 `User` 모델을 위한 APIView, Serializer 등이 정의되어 있으며, 필요에 따라 수정하여 진행할 수 있다.

- **{{your_project_name}}**

  Django 프로젝트 전반적으로 공유하기 위한 파일들의 모음으로, `static`, `template`, `fixtures` 가 이에 해당된다.

### **bin dir**

도커 환경 구성을 위한 전반적인 코드들이 존재하는 디렉토리로, 도커 실행을 위한 스크립트, 컴포즈 환경 구성을 위한 도커파일들이 존재한다.

- **.envs**

  도커 환경에서의 서비스에 필요한 설정들(ex. DB URL, PW 등)을 분리하여 관리하기 위한 디렉토리다. 로컬(.local), 서비스(.production)용으로 구분되어있으며 서비스용은 공개된 저장소에 올라가지 않도록 주의할 필요가 있다.

- **compose**

  도커 컴포즈 환경을 구성할 때 각 도커 컨테이너를 구성하기 위한 도커파일들과 서버 실행(ex. start) 및 부가적으로 확인(ex. entrypoint)하기 위한 명령어들 또한 위치해 있다.

- **requirements**

  서버 운용에 필요한 패키지 파일들로, base, local, production 3가지로 구분되어 있다.

- **local.yml & production.yml**

  로컬 및 서비스 환경에 맞는 도커 컴포즈를 구성하기 위한 `docker-compose.yml` 파일이다.

- **restart\_(local OR production)\_docker.sh**

  도커 컴포즈 실행을 위한 명령어를 모아둔 쉘 스크립트 파일이다.

## Usage

Template을 로컬에 클론한다

```bash
$ git clone https://github.com/bigpie1367/inco-django-template.git
```

이후 본인 프로젝트에 맞게 설정하기 위해 동봉된 파이썬 코드를 실행하여 프로젝트를 설정한다. 해당 코드는 아래와 같은 순서로 수행된다

1. 사용자로부터 project, app name을 입력받아 기존 값 대체
2. Celery, Redis 사용 유무에 따라 사전에 설정된 코드들이 존재하는 git branch로 switch
3. 사용자로부터 Git URL을 입력받아 정상적인 URL인지 확인 후 Git 초기화 및 연결

```python
$ python build_project.py

Enter the new project name:
Enter the new app name:
Use Celery (y/n):
Use Redis (y/n):
Enter the Git remote URL:
```

이후 본인의 프로젝트 환경에 맞게 추가적으로 수정을 진행할 필요가 있다.

```python
# {{ your_project_name }}/settings/base.py line 25
# 테스트를 진행할 로컬 DB 환경에 맞게 수정

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='{{ your_project_name }}'),
        'USER': env('POSTGRES_USER', default='your_database_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='your_database_password'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    }
}
```

```python
# {{ your_project_name }}/settings/base.py line 25
# 테스트를 진행할 로컬 DB 환경에 맞게 수정

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='{{ your_project_name }}'),
        'USER': env('POSTGRES_USER', default='your_database_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='your_database_password'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    }
}
```

## Run Django Project

프로젝트는 아래와 같은 명령어를 통해 희망하는 환경에 맞게 수행할 수 있다

```bash
# Run in local

cd {{ your_project_name }}
python manage.py runserver
```

```bash
# Run Docker-compose for local

cd bin
sh restart_local_docker.sh
```

```bash
# Run Docker-compose for production

cd bin
sh restart_production_docker.sh
```
