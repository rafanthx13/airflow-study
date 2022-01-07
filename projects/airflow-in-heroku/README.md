# Airflow no Heroku

Dentre os vários links que tentei, somente esse deu certo:

https://github.com/arboiscodemedia/Heruko-Airflow-Requisite

**OBS: O AIRFLOW NÃO FUNCIONA BEM NO HEROKU PORQUE CONSOME MUITA MEMÓRIA E HÁ UM LIMITE NO PLANO FREE DO HEROKU: 500MB**

## virtual env

````sh
> virtualenv venv
> source venv/bin/activate
> pip install "apache-airflow[postgres, password]"
> pip freeze >> requirements.txt
````

## Dependências desse projeto

Primeiramente eu tentei instalar o airflow mais novo com `pip install "apache-airflow[postgres, password]"` mas não deu certo. Então, baixei diretamente as dependências do git, o arquivo a seguir:

https://github.com/arboiscodemedia/Heruko-Airflow-Requisite/blob/main/requirements.txt

````sh
pip3 install -r requirements.txt
````

## Iniciar projeto Airflow

**Iniciar projeto airflow**
+ Os comandos a seguir cria as pastas do projeto

````sh
export AIRFLOW_HOME=$PWD
airflow db init
````

**Executar**

````sh
airflow standalone
````

Vai subir um servidor no seguinte link : http://localhost:8080/

E vai criar um usuário e senha:

````
standalone | Airflow is ready
standalone | Login with username: admin  password: PTPzb6mEvDwPS5Y9
````

## Configurar chave de criptografia

At this point, we will need to create a file named `generate_kernet_key.py` that we will use to generate a sensitive data encryption key that will be used by Airflow.

````python
# // Arquivo generate_fernet_key.py
from cryptography import fernet

print(fernet.Fernet.generate_key().decode("utf-8"))
````

Usar essa chave gerada nas variáveis de ambiente do heroku

## `airflow.ctg`

Contém arquivos de configuração do airflow, vamos mudar para usar o postgre ao invés do SQLite

````sh
# Here we define the path to our databa (linha 30)
sesql_alchemy_conn = postgresql+psycopg2://postgres:postgres@localhost:5432/airflow

# Airflow has some classes that can be used i.e LocalExecutor CeleryExecutor.. 
# In this example we will use LocalExecutor (linha 24)
executor = LocalExecutor

# Here we will use our Fernet script to generate an encryption key  (linha 123)
fernet_key = $(python3 "contrib/generate_fernet_key.py")
````

remova o bd do sql `airflow.db` e execute denovo `airflow db init` para usar o BD do postgreSQL

## Configurando postgreSQL

## .gitignore

Cria git e faz commit e ignore os seguintes arquivos

````
.venv/
__init__.py
__pycache__/
````

## Fazendo deploy no heroku

1. Login to Heroku Website

````sh
heroku login
````

2. create your app 

````sh
heroku create my-heroku-airflow
````

3.  Create Heroku Postgresql

````sh
heroku addons:create heroku-postgresql:hobby-dev -a my-heroku-airflow
````

4.  Setup Heroku Config

Instalamos o postgre como add-on no heroku, podemos pegar seus dados com o seguinte comando que retorna todas as variáveis de ambiente do heroku:

```
heroku config -a my-heroku-airflow
```

Dentre elas, estará a variável com a URL para acesso do postgre e inserida na variável `AIRFLOW__CORE__SQL_ALCHEMY_CONN`

````sh
heroku config:set AIRFLOW__CORE__SQL_ALCHEMY_CONN = "postgresql://" 
heroku config:set AIRFLOW__CORE__LOAD_EXAMPLES=False -a my-heroku-airflow
heroku config:set AIRFLOW_HOME=/app -a my-heroku-airflow
````

   Run this line in Python:

   Pode ser feito no shell python, basta digitar `python` e executar esses comandos em ordem
````py
from cryptography.fernet import Fernet; 
print(Fernet.generate_key().decode())

# OUTPUT >> 5KaIPunwNmSisZ48JIhfsZoHTlgZ6qGgt4Hq0yUGxN8=
````


````sh
heroku config:set AIRFLOW__CORE__FERNET_KEY=<secret_key> -a my-heroku-airflow
````


5. Push to Heroku Master
````sh
git push heroku master
````
6. Check if no error
````sh
heroku logs --tail -a my-heroku-airflow  
````
7. Modify Procfile
````sh
web: airflow webserver --port $PORT
````
8. Setup Additional Heroku Config.
````sh
heroku config:set AIRFLOW__WEBSERVER__AUTHENTICATE=True -a my-heroku-airflow
heroku config:set AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.contrib.auth.backends.password_auth -a my-heroku-airflow
````
9. git update
````sh
git add .
git commit -m "change Procfile to start the webserver"
git push heroku master
````
10. Check if no error
````sh
heroku logs --tail -a my-heroku-airflow  
````
11. Preview

    Login to Heroku and goto app then click "open app"  


## Criando Usuário 

1. create a user account using ssh into the Heroku instance of our app:

````sh
heroku run bash -a heroku-airflow

airflow users create -r Admin -u admin -e arboiscodemedia@gmail.com -f Ricardo -l Arbois -p heroku2021
````

2. exit bash
   
      exit

## Executando DAG no heroku airflow


3. Login using the admin account using the information created earlier.

4. Create a sample dag file inside a dags folder
+ Create folder name "dags" then create a dag file name "hellodags.py"

````python
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def print_hello():
    return 'Hello world!'

dag = DAG('hello_world', description='Simple tutorial DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

dummy_operator >> hello_operator
````

5. Update dags in git

````sh
git add dags
git commit -m "create hello dag"
````
6. update Procfile by setting up the auto webserver and scheduler

````sh
web: airflow webserver --port $PORT --daemon & airflow scheduler
````
7. update the changes using git

````sh
git add Procfile
git commit -m "change Procfile to run the webserver as daemon and scheduler as main app"
````

8. Finally update changes to heroku master

````sh
git push heroku master
````
9. Login again to airflow for checking

10. If there no dags file display in the list then run again this line settings below then check again

````sh
heroku config:set AIRFLOW_HOME=/app -a heroku-airflow
````