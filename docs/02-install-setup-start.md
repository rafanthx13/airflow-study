# Instalar, Configurar e Executar Airflow

## Links

part 1 : https://medium.com/analytics-vidhya/manage-your-workflows-with-apache-airflow-e7b0e45544a8
part 2 : https://medium.com/analytics-vidhya/manage-your-workflows-with-apache-airflow-7d39e12b302b
airflwo no mysql

## Executar Localmente num Venv

**Criar Venv**

````sh
virtualenv venv # create virtual env
source venv/bin/activate # activate virtual env
````

**Instalar Dependências**

````sh
pip install --upgrade pip         # pip upgrade
pip install apache-airflow        # installing airflow
````

**Checar versão do Airflow**


````sh
$ airflow version
>> 2.2.3
````

ou tambem

````
airflow info
````

## Pacotes adicionais na instalaçâo

O objetivo do apache airflow é faze ETL, ou seja, mexeer muit com banco e dados.

Por isos, é possível instalra ele e tambem deependencais de BD

No link a aseguir h'a tudo adicional que da para baixar
https://airflow.apache.org/docs/apache-airflow/1.10.2/installation.html

Exemplos;
````
pip install'apache-airflow[mysql]'
````

## Variáveis de Ambiente do Linux


**export  (only linux)**

Airflow requires a location on your local system to run known as AIRFLOW_HOME. If we don’t specify this it will default to your route directory. I recommend you to set up the AIRFLOW_HOME under the same directory where you are currently in i.e where you created the virtual environment.

````sh
$ export AIRFLOW_HOME=$PWD
````

$PWD é o seu diretório atual. Se você não coloca isso, vai criar o projeto do airflow na pasta `home` do linux.

**Ver variáveis de ambiente**

printenv

**Ver se essa variável está setada**

printenv | grep AIRF


## Iniciar Airflow

**Inicilizar db**

After configuration, you’ll need to initialize the database before you can run tasks:

````
$ airflow db init
````

This will initiate the prerequisite to run your airflow task. If you see closely there will be some folder created under your Airflow directory. Will look into it closely some other day.

**Criar usuário se senha**

````sh
$ airflow users create --role Admin --username rafan10 --email rafaassis15@gmail.com --firstname Rafael --lastname Assis --password airflow7
````

ou usar a seguinte sintex 

````sh
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
````

**Start**

Step: 7

Now we are ready to run Airflow Web Server and Scheduler locally. Use two separate shell tabs to run both processes and don’t forget to activate the virtual environment in the new tab.
For good practice, I suggest you run Scheduler first and then go for the Web Server.

Vai requerer abrir dois terminais

**GARANTA QUE AMBOS ESTEJA COM  ` export AIRFLOW_HOME=$PWD` configurados**
````
# Start the Scheduler
$ airflow scheduler
# Start the WebServer
$ airflow webserver --port 8080     #default port is 8080
````

## Executando tudo junto

````
$ source venv/bin/activate && export AIRFLOW_HOME=$PWD 
$ airflow scheduler -D airflow webserver --port 8080
````

Tanto o scheduler quanto o webServer podem rodar no modo daemon (coloca -D ou --daemon), ou seja, em background, asism podemos executar tudo no mesmo terminal.

## Resumindo

````sh
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=~/airflow

# install from pypi using pip
pip install apache-airflow

# initialize the database
airflow db init

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

# start the web server, default port is 8080
airflow webserver --port 8080

# start the scheduler
# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
airflow scheduler

# visit localhost:8080 in the browser and use the admin account you just
# created to login. Enable the example_bash_operator dag in the home pag
````

# PARTE 2

Dag files should have .py extention and stored inside a folder named dagswhere you have initiated the db.

As Dags colocadas em /dags precisam ser válidas para o airflow que está rodando. Ou seja, se tier algum import de algo que não está instalado no venv, ela não vai aparecer.

Para ver melhors as dags, usa o web-server, nele haverá os logs de erros bem melhor do que olhar no terminal.

Neste exemplo, necessitava da pandas que nao estava instalado, entao, tive que instalar e só depois deu certo

DO comando 

````
airflow dags list
````

sai entao (se o codigo estiver sem erros e sem import quebrados)


````
zalando_workflow                        | /home/rhavel/Documentos/STUDY-PROJECTS/airflow-study/projects/shritam-airflow/dags | airflow | True  
                                        | /zalando_etl.py                                                                    |         |       
````

# BD do Airflow

https://teguharif.medium.com/data-engineering-series-apache-airflow-1-6ed993666246

O Airflow roda as taske, e tudo mais e salvar em um banco de dados.

ELe por default muitas vezes noa cria o banco, entao alem de especificar a URL de acesso, voce precisa criar a tbela

### MYSQL

https://teguharif.medium.com/data-engineering-series-apache-airflow-1-6ed993666246

````sql
CREATE DATABASE airflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airflow_user' IDENTIFIED BY 'airflow_pass';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'airflow_user';
````

e  mude o seguinte code no `aiflwow.conf`

````
${AIRFLOW_HOME}/airflow.cfg
sql_alchemy_conn = mysql://{user}:{password}@{hostname}:3306/airflow
````
