# Использование GitHub Actions
Пробуем создать свой CI/CD пайплайн для домашнего проекта при помощи Python и GitHub Actions<br/>

## 1. Зависимости
Для запуска этого проекта потребуется:
- VPS/VDS/VM с *nix ОС, куда будут деплоится контейнеры (проверено на Ubuntu Server 22.04)
- Белый IP адрес (проброшеный порт, иной способ получения веб хука)
- Python 3.11
- Docker
- Git

## 2. Установка
#### Установка и настройка серверной части на чистой Ubuntu Server 22.04
```shell script
sudo apt update

cd ../home
curl -fsSL https://get.docker.com -o get-docker.sh
sh ./get-docker.sh

git clone https://github.com/Friskes/actions_ci_example.git
cd actions_ci_example/ci_app/
sudo apt install python3-pip
sudo python3 setup.py install
sudo cp ../ci_example.service /etc/systemd/system/ci_example.service
# добавьте токен в файл: /etc/systemd/system/ci_example.service в переменную: DEPLOYMENT_TOKEN
# его можно сгенерировать командой: `openssl rand -hex 20`

sudo systemctl daemon-reload
sudo systemctl enable ci_example.service
sudo systemctl start ci_example.service
```

Проверить то что веб-сервер запустился и работает можно с помощью команд:
```shell script
sudo systemctl status ci_example.service
```
или
```shell script
curl 0.0.0.0:5000
```
Посмотреть лог веб-сервера:
```shell script
sudo journalctl -u ci_example.service
```

## 3. Настройка GitHub части
Заходим в свой GitHub репозиторий -> Settings -> блок Security -> Secrets and variables -> Actions

#### Создаем секретные переменные окружения:

- `DEPLOYMENT_SERVER_ADDRESS`
адрес вашего Ubuntu сервера с портом который указан в ci_app, x.x.x.x:5000

- `DEPLOYMENT_TOKEN`
со значением которое вы присвоили в переменную окружения DEPLOYMENT_TOKEN в файле ci_example.service на сервере

Для переменных ниже, необходимо создать аккаунт в DockerHub, на главной странице нажать Repositories -> Create repository, и установить имя репозитория, например как на гитхабе.

- `DOCKER_LOGIN`
ваше имя пользователя в DockerHub

- `DOCKER_REPOSITORY_NAME`
название вашего репозитория в DockerHub

- `DOCKER_ACCESS_TOKEN`
токен от DockerHub который можно получить в Account Settings -> Security -> New Access Token

## 4. Использование
При пуше нового кода в любую ветку, будет запущена задача тестирования из файла test_on_push.yaml, где будут проведены все тесты указанные в директории /tests/ корня проекта.<br/>

При создании релиза, будут выполены действия из файла deploy_on_release.yaml
А именно проход по всем тестам из директории /tests/
Если тесты будут пройдены успешно, то запустится процесс 
сборки докер образа, который будет отправлен в DockerHub.
Если пуш в регистри закончился успешно, то будет отправлен вебхук на ранее установленный вебсервер, который и задеплоит наш контейнер.

## 5. Создание релиза
Релиз можно создать кликнув на `Create a new release` на странице вашего репозитория.

Или из командной строки, для этого необходимо установить `github cli` с помощью команды:
```shell script
winget install --id GitHub.cli
```
После установки необходимо авторизоватся в GitHub с помощью команды:
```shell script
gh auth login
```
Затем выполните сам релиз с необходимыми вам параметрами:
```shell script
gh release create <версия тэга, например v0.0.1> --target <название ветки, например main>
```

#### Зайти на работающий сервер после создания релиза можно по адресу:
```
http://<ваш IP сервера>:8080
```

#### Посмотреть активные контейнеры можно сделав GET запрос с токеном авторизации (Linux):
```
curl --silent --show-error -X GET <ваш IP сервера>:5000 -H 'Authorization: <ваш секретный DEPLOYMENT_TOKEN>'
```

### Полезное
```
https://youtu.be/a0eZ03bmJvA?si=rrOwkNAAMuntHvw2
https://habr.com/ru/articles/476368/
https://github.com/gonfff/actions_ci_example
https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
https://github.com/actions/setup-python
https://github.com/cli/cli#windows
https://docs.github.com/en/github-cli/github-cli/quickstart#prerequisites
https://stackoverflow.com/a/65474194/19276507
```
