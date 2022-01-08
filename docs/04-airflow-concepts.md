## Linkx

Muito bom em POrtugues
https://medium.com/datarisk-io/apache-airflow-conceitos-iniciais-e09c0dd18141
bom
https://medium.com/apache-airflow/apache-airflow-2-0-tutorial-41329bbf7211

https://medium.com/plumbersofdatascience/key-concepts-in-apache-airflow-ee04cbdf45cc

## conceitos


### DAG

As DAGs são o ponto chave para o bom funcionamento do Airflow e um dos porquês de ele ser tão adotado. DAG ou Directed Acyclic Graph — que significa grafo acíclico dirigido — de forma bem resumida, é uma ferramenta matemática composta de nós e arestas que conectam estes nós. O fato de ser direcionado implica que estas arestas são “setas” unidirecionais e, por ser acíclico, cria a restrição de não entrarmos em nenhum caminho que leve a um loop, ou seja, seguindo o sentido das arestas eventualmente iremos parar em um ou mais nós onde não há mais caminho a ser percorrido.
O Airflow se baseia em DAGs para desenhar um pipeline de dados, seja qual for a sua função. Em uma dada DAG, cada uma das tarefas ou tasks do Airflow é um nó do grafo e as arestas representam a ordem de execução desejada dessas tarefas, conforme exemplo abaixo:

Exemplo de DAG com 3 tarefas. As arestas mostram a dependência entre elas.
No exemplo acima, vemos que a única task que não depende de nenhuma outra para iniciar é a print_date. Com isso, ela deve ser a primeira a ser executada. Vemos, também, que as tasks sleep e templated dependem da task print_date para serem executadas, e, por isso, apenas começam quando a task print_date tiver sido completada com sucesso.
As DAGs devem ser escritas em Python e as dependências entre as tasks são totalmente definidas no próprio código.
### DAG Run

A DAG Run é a realização de uma DAG. Enquanto a DAG engloba o conjunto das tasks e suas dependências, ela é atemporal e não implica que algo tenha sido executado ou não. Por outro lado, uma DAG Run é uma execução propriamente dita de uma DAG, incluindo horários, tempos de execução de cada uma das tasks, status de cada uma delas, etc.

### Task 
Já falamos bastante nas tasks ao longo do post, porque é algo bastante claro. Dando um pouco mais de detalhe, uma task deve implementar alguma lógica a ser executada, que pode ser a ingestão de um dado através de uma API, a transformação de uma tabela ou até mesmo o treinamento de um modelo de machine learning. Além disso, quanto mais pudermos isolar estas atividades em diferentes tasks e desenhar uma DAG de forma coerente com a dependência entre elas, o processo ficará mais enxuto e será mais fácil de detectarmos e corrigirmos erros, pois teremos isolado cada uma das atividades e, consequentemente, as possíveis fontes de erro.

### Operators

---

https://medium.com/plumbersofdatascience/key-concepts-in-apache-airflow-ee04cbdf45cc

Tasks
Tasks in airflow are built around operators. These operators determine which workers are initialized and used to complete a certain task. The common operators used include Bash operators, Python operators, Email operators, Simple HTTP operators, and sensors.
+ Bash Operators — Used mainly for executing bash scripts, however, It can be slightly modified and used to run other types of files.
+ Python Operators — Used for executing python scripts as well as python functions that have been created within the DAG file.
+ Email Operators — Utilized for sending out notifications to users when a task fails or is successful. It can also come in handy in cases where a task involves an email sending operation.
+ Simple HTTP Operators — Implemented in cases where the data used in the task is obtained from an API that requires HTTP authentication.
+ Sensor Operators — Waits for updates in files, folders, S3 buckets, remote repositories, or other data sources before triggering a task.
+ Database Operators — These are database engine-specific operators utilized when data is obtained from a database and allow the user to execute SQL commands against the database provided correct authentication information is provided. They include: MySqlOperator, SqliteOperator, PostgresOperator, JdbcOperator etc.


### Task Instance
A Task Instance está para uma Task assim como a DAG Run está para a DAG. Dessa maneira, uma task instance nada mais é que a realização de uma task, onde podemos ter acesso aos logs cada vez que aquela task for executada, os tempos de execução, o status da task, se foi concluída ou se houve algum erro, etc.
### XCom
XCom (comunicação cruzada) é uma forma de troca de mensagens curtas entre diferentes tasks. Apesar do Airflow poder ser integrado a diferentes ferramentas de Big Data, por exemplo o Apache Spark, o tratamento de dados grandes deve permanecer dentro de cada Task de forma que somente pequenas mensagens, basicamente metadados, sejam trocados entre as Tasks por meio de XCom. Por exemplo, o retorno de uma função executada em uma task pode servir de parâmetro para uma execução de tasks subsequentes, e com isso, as XComs tornam-se bastante úteis.
### Executor
O executor é o mecanismo pelo qual uma Task é realizada. Ele é definido no momento da instalação do Airflow, de forma que, uma vez definido, será o mesmo em todas as DAGs de uma mesma instalação do Airflow. Basicamente, o executor trata do mecanismo de execução de cada código, ou seja, qual infraestrutura o código deverá ser executado, por exemplo, utilizando as capacidades do Kubernetes, através do KubernetesExecutor, ou simplesmente uma execução em máquina local, utilizando o LocalExecutor.

---

https://medium.com/apache-airflow/apache-airflow-2-0-tutorial-41329bbf7211

Executor is one of the crucial components of Airflow and it can be configured by the users. It defines where and how the Airflow tasks should be executed. The executor should be chosen to fit your needs and as it defines many aspects of how Airflow should be deployed.
Currently Airflow supports following executors:

+ LocalExecutor—executes the tasks in separate processes on a single machine. It’s the only non-distributed executor which is production ready. It works well in relatively small deployments.
+ CeleryExecutor—the most popular production executor, which uses under the hood the Celery queue system. When using this executor users can deploy multiple workers that read tasks from the broker queue (Redis or RabbitMQ) where tasks are sent by scheduler. This executor can be distributed between many machines and users can take advantage of queues that allow them to specify what task should be executed where. This is for example useful for routing compute-heavy tasks to more resourceful workers.
+ KubernetesExecutor— is another widely used production-ready executor. As the name suggests it requires a Kubernetes cluster. When using this executor Airflow will spawn a new pod with an Airflow instance to run each task. This creates an additional overhead which can be problematic for short running tasks.
+ CeleryKubernetsExecutor— the name says it all, this executor uses both CeleryExecutor and KubernetesExecutor. When users select this executor they can use a special kubernetes queue to specify that particular tasks have to be executed using KubernetesExecutor. Otherwise tasks are routed to celery workers. In this way users can take full advantage of horizontal auto scaling of worker pods and possibility of delegating longrunning / compute heavy tasks to KubernetesExecutor.
+ DebugExecutor—this is a debug executor. Its main purpose is to debug DAG locally. It’s the only executor that uses a single process to execute all tasks. By doing so it’s simple to use it from IDE level as described in docs.






### Operator
O operator é o template de uma Task, determina qual a ferramenta usada para executar determinado código. Como exemplo, temos o PythonOperator, que é o template para a execução de scripts escritos em Python. O Airflow permite a utilização de uma gama de diferentes operators para as mais diversas situações. Por exemplo, se precisarmos realizar uma tarefa bem específica onde há a necessidade da montagem de um ambiente complexo, podemos utilizar o DockerOperator, com o qual é possível realizar a execução de um código inclusive em linguagem diferente do Python, contido em determinada imagem que é passada como parâmetro ao operator.

## Arquiteturado Apache Airflow

Agora, vamos falar um pouco sobre os diferentes serviços que integram o Airflow para que ele consiga fazer funcionar as diferentes DAGs com robustez.

Conforme podemos ver na imagem acima, temos de mais próximo ao usuário o Webserver, que é responsável por fornecer uma interface com a qual podemos interagir com o Airflow para controlar e monitorar nossas DAGs. Por sinal, a interface do Airflow dispensa comentários por ser ao mesmo tempo enxuta e conter diversas informações muito úteis para a execução e monitoramento das DAGs. Com certeza é um dos motivos que fez o Airflow ganhar tanta popularidade.
Além do Webserver, temos um banco de dados que é responsável por guardar metadados. E que dados seriam estes? Todos aqueles relacionados a cada task instance de cada DAG Run. Essencialmente, lá ficam armazenadas informações como: os momentos de execução, o status de cada task instance, os tempos de execução de cada task instance, os agendamentos de cada DAG, etc. Só não ficam armazenados no banco de dados os próprios códigos das DAGs e nem os logs de cada task instance.
Outra peça bastante fundamental nesse quebra-cabeça é o scheduler. Ele é responsável por garantir que cada uma das tasks dentro de cada uma das DAGs seja executada no momento correto. Ele controla, portanto, os agendamentos e garante a ordem de execuções de tasks que dependem de outras tasks. Está em contato direto com o Executor para disparar uma solicitação para que seja executada cada uma das tasks. O executor, por sua vez, será o responsável por fazer a coisa acontecer.
Não podemos deixar de falar do DAG Directory, que é o local onde serão armazenados os códigos em Python que compõem cada uma das DAGs. Há algumas opções bastante interessantes para o armazenamento dos códigos. Por exemplo, podemos colocá-los na própria imagem do Airflow, de forma que quando feito o deploy, os códigos estejam locais à instalação. Uma forma mais interessante é a utilização da ferramenta git-sync, que é basicamente um “container sidecar” que é colocado nos containers do Webserver e do Scheduler, que permite realizar a sincronização com periodicidade pré-definida com o repositório onde se encontram os códigos com as DAGs. Dessa maneira, com uma atualização simples do repositório, de tempos em tempos o Airflow irá buscar por atualizações das DAGs e realizar o pull desses códigos para que estejam presentes em uma pasta local ao Airflow que irá conter todos as DAGs.
Na figura acima, há também a presença dos workers, que vão depender do tipo do Executor escolhido. Por exemplo, no caso da utilização do CeleryExecutor, utiliza-se a ferramenta Celery para distribuir diferentes tasks entre os workers disponíveis. No caso do KubernetesExecutor, o Kubernetes cria um POD para cada Task Instance, situação em que podemos entender os Workers como sendo basicamente os PODs em que cada uma das Tasks será executada.

----

https://medium.com/plumbersofdatascience/key-concepts-in-apache-airflow-ee04cbdf45cc

**Web Server**

The Airflow webserver accepts HTTP requests and allows the users to access the Airflow Web UI. The airflow user interface allows the users to manage their DAGs, users can: trigger, pause, unpause and delete DAGs. The Admin pane also allows for more complex configurations to be made such as providing third-party access.

**Scheduler**

The scheduler is a key part of the Apache Airflow ecosystem. The scheduler constantly runs in the background to monitor all the tasks, DAGs and ensure that all dependencies have been met. Most importantly it ensures that all the DAGs are triggered at the right time and manages any queues that may form.

It is important to take note of the time zone settings to ensure that the time zone being used by the scheduler is correct. The time zone can be changed on the Airflows web user interface.

**Backend Database**

The airflow webserver and scheduler need a point of reference to authenticate users and store logs regarding DAG executions. The data stored by airflow is referred to as the Airflow Metadata and is important for the scheduler to be able to operate efficiently.
The default database used by Apache Airflow is SQLite, however, it's recommended only for testing purposes and therefore it is advised that another database such as MySQL or Postgres is set up in its place.


## DEploy

Deploying Airflow

Airflow as a distributed system
Although Airflow can be run on a single machine it is fully designed to be deployed in a distributed manner. This is because Airflow consist of separate parts:
**1.**
Scheduler — this is the brain and heart of Airflow. Scheduler is responsible for parsing DAG files, managing database state and — as the name suggests — for scheduling tasks. Since Airflow 2.0 users can run multiple schedulers to ensure high availability of this crucial component.
**1.**
Webserver — the web interface of Airflow which allows to manage and monitor DAGs.
**1.**
Worker — a Celery worker application which consumes and executes tasks scheduled by scheduler when using a Celery-like executor (more details in next section). It is possible to have many workers in different places (for example using separate VMs or multiple kubernetes pods).

All those components can be started using the airflow command. And all of them require access to the Airflow metadatabase which is used to store all information about DAGs and tasks. Additionally both scheduler and worker need access to exactly the same DAG files. That’s why we will shortly discuss DAG distribution approaches later on but first let’s learn about Airflow’s executors.
