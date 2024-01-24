# Django Template

Django Custom Template 입니다

## Usage

Template를 로컬에 클론합니다.

```bash
$ git clone https://github.com/bigpie1367/inco-django-template.git
```

이후 본인 프로젝트에 맞게 설정하기 위해 동봉된 파이썬 코드를 실행하여 프로젝트를 설정합니다.

```python
$ python build_project.py

Enter the new project name:
Enter the new app name:
```

## Run Django Project

Run in local

```bash
  $ docker-compose build
  $ docker-compose up
```

Run in production

```bash
  $ docker-compose -f docker-compose-deploy.yml build
  $ docker-compose -f docker-compose-deploy.yml up
```

## Roadmap

- [ ] coverage
- [ ] CI
- [ ] CD
- [ ] MySQL
- [ ] No docker
- [ ] Django Rest Framework

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@gmlwo530](https://github.com/gmlwo530)
