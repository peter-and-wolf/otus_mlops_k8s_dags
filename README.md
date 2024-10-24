# otus_mlops_k8s_dags

Материалы к занятию №38 **«Поиск отклонений и сдвигов в данных / MLOps в k8s»**. 

## Пререквизиты

Предполагается, что у вас запущен кластер кубера. Это может быть кластер, которым вы можете управлять (*и который вам не жалко поломать*): например, – в облаке (YC) или кластер, запущенный локально с помощью соответствующей сборки (например, [kind](https://kind.sigs.k8s.io/) или [mimnikube](https://minikube.sigs.k8s.io/docs/)).

## Структура репозитория

* [apps/joke-api](apps/joke-api) – простое FastAPI-приложение, которое которое экспонирует ручку `api/v1/jokes`. Если за нее дернуть, вернется случайная выборка коротких и глупых текстов из файла [jokes.csv](apps/joke-api/data/jokes.csv);
* [apps/joke-to-s3](apps/joke-to-s3) – приложение, которое обращается к `apps/joke-api`, получает json с выборкой текстов, преобразует его в csv и загружает его в `s3`.  
* [dags](dags) – директория содержит скрипты DAG-ов для Airflow, который запущен к кластере кубера.
* [k8s](k8s) – директория содержит необходимые конфигурации для Airflow в кубере. 

## Подготовка

### joke-to-s3

Собираем Docker-образ c приложением:

```bash
docker build --platform linux/amd64 -t {ваш-логин-на-dokerhub}/joke-to-s3:v1 -f Dockerfile
```

Отправляем образ в [dockerhub](https://hub.docker.com/):

```bash
docker push {ваш-логин-на-dokerhub}/joke-to-s3:v1
```

### joke-api

Сервис должен быть запущен там, до куда под, запущенный в вашем кластере кубера, сможет дозвониться. Проще всего создать виртуальную машину в YC (самую слабую и дешевую) и развернуть сервис там:

1. Клонируете репозиторий;
1. Создаете виртуальное окружение python и устанавливаете в него пакеты из `apps/joke-api/requirements.txt`;
1. Запускаете FastAPI-сервис: `fastapi run main.py`

Если все получилось, то:

```bash
curl http://{публичный-IP-вашей-ВМ}:8000/api/v1/jokes
```

вернет json-простыню с текстами на кириллице.

## Конфигурация кубер-кластера

### Установка Airflow

В файле [k8s/airflow/values.yaml](k8s/airflow/values.yaml) в секции `extraEnvVars` измените значения следующих переменных окружения:

* `JOKE_API_ENDPOINT` – url к вашему joke-api, запущенному [тут](#joke-api);
* `S3_ENDPOINT` – url к вашему S3 (если используете объектное хранилище YC, почти наверняка будет `https://storage.yandexcloud.net`);
* `S3_BUCKET` – имя бакета, в который хотите складывать файлы;
* `JOKE_TO_S3_IMAGE` – тег Docker-образа, который вы собрали [тут](#joke-to-s3) и отправили в Dockerhub;

В файле [k8s/ya-s3-secret.yaml](k8s/ya-s3-secret.yaml) в секции `stringData` измените значения следующих переменных окружения:

* `AWS_ACCESS_KEY_ID` – укажите идентификатор вашего секретного ключа для доступа в S3;
* `AWS_SECRET_ACCESS_KEY` – укажите ваш секретный ключ для доступа в S3;

Установте Airflow из helm-чарта [bitnami](https://artifacthub.io/packages/helm/bitnami/airflow):

```bash
# Подключаем репозиторий
helm repo add bitnami https://charts.bitnami.com/bitnami

# Обновляем индекс
helm repo update

# Ставим чарт
helm install airflow bitnami/airflow
```

Примените конфигурацию:

```bash
helm upgrade --install airflow bitnami/airflow -f k8s/airflow/values.yaml --set scheduler.automountServiceAccountToken=true --set worker.automountServiceAccountToken=true --set rbac.create=true
```

Активируйте манифест с секретами для доступа в S3:

```bash
kubectl apply -f k8s/ya-s3-secret.yaml
```

## Работа с Airflow

Пробросьте порт из кластера наружу:

```bash
kubectl port-forward svc/airflow 8080:8080
```

Идите браузером на `localhost:8080`, откроется морда аутентификации Airflow. Логин – `user`, пароль узнайте вот так:

```bash
kubectl get secret --namespace "default" airflow -o jsonpath="{.data.airflow-password}" | base64 -d
```

Когда залогинитесь, увидите единственный DAG `hello_world_dag`, запустите его, убедитесь, что он работает: забирает данные из `joke-api`, преобразует их в csv и перекладывает в S3.


Спасибо! И да пребудет с вами сила. 



