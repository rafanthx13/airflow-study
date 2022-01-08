# 01 - O que é Apahe Airflow

## Links

https://medium.com/datarisk-io/apache-airflow-conceitos-iniciais-e09c0dd18141

## Concorrentes

Luigi: Python module that helps you build complex pipelines of batch jobs. It handles dependency resolution, workflow management, visualization, etc. It also comes with Hadoop support built-in

Oozie: workflow scheduler system to manage Apache Hadoop jobs(DAGs).

Airbyte

Prefect

Dagstesr

## O que é 

O Airflow é uma ferramenta que nos possibilita realizar a criação, agendamento e monitoramento de pipeline de forma programática.

Quando falamos em processos de ETL básicos, muitas vezes pensamos que não precisamos de uma ferramenta tão robusta para gerenciarmos nossos processos. Muitas vezes um simples scheduler consegue dar conta do recado e realizar todas as tarefas de um pipeline tranquilamente. No entanto, quando começam a surgir dependências entre as tarefas e, principalmente, quando é difícil de se determinar o tempo de execução de tarefas que possuem tarefas subsequentes dependentes de seus términos para iniciarem, vemos que existe a necessidade de utilizarmos ferramentas mais complexas e desenvolvidas, justamente para este tipo de situação.

### De onde veio

Um resumo sobre o Airflow: é uma ferramenta Open-Source que foi criada no Airbnb em 2014 e desde 2019 fez parte da Apache Software Foundation.

Ele se baseia em 4 princípios diretos:
+ Dinâmico: com a utilização do conceito de configuration-as-code, o Airflow permite criar pipelines dinamicamente de forma programática;
+ Extensível: a partir de uma variedade de operadores, executores e a possibilidade de extensão das bibliotecas é possível criar um ambiente adequado ao nível de abstração desejado;
+ Elegante: os pipelines são enxutos e diretos, além da possibilidade de uso do Jinja templating engine;
+ Escalável: por ter sido desenvolvido com uma arquitetura modular, é possível utilizar sistemas de mensageria para realizar a orquestração dos workers.

Além disso, um detalhe importante do Airflow é que ele é totalmente escrito na linguagem Python, que é uma das linguagens mais populares atualmente na área de dados.

## Descrição

**What is Airflow?**
As a Data Engineer there will be a point when you think up to orchestrating your workflows, and here come Apache Airflows to fill the gap. Originally created at Airbnb in 2014, Apache Airflow is an open-source tool for orchestrating complex workflows and data processing pipelines. It is a platform to programmatically Authoring, Scheduling, and Monitoring workflows.
+ Authoring: Workflows in Airflow are written as Directed Acyclic Graphs(DAGs) in Python Programming Language. It allows the user to write their custom workflows in python.
+ Scheduling: The user can specify when a workflow should start, end, and after what interval it should run again.
+ Monitoring: The Airflow UI makes it easy to monitor and troubleshoot your data pipelines. It has a bunch of tools to track your workflow in real-time.

## Airflow no Windows

Airflow precisa de certos pacotes pytohn que não rodam no winsow, a não ser que utilize o WSL Ubuntu

