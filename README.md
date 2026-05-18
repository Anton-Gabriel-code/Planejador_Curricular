# Planejador Curricular
## Aluno: Antônio Gabriel dos Santos Barbosa
# Trabalho acadêmico da disciplina de Estruturas de Dados — Tema C.

## Aplicação em Python que organiza a ordem correta para cursar as disciplinas do curso de Ciência da Computação, respeitando os pré-requisitos de cada matéria. O núcleo lógico é baseado na teoria dos grafos, utilizando um Grafo Direcionado Acíclico (DAG) e o algoritmo de Ordenação Topológica.

## Como o problema foi modelado
### Elemento do GrafoRepresentação no problemaVértice (nó)Uma disciplina do cursoAresta direcionadaUm pré-requisito (A → B significa "curse A antes de B")DAG (sem ciclos)Grade curricular válidaCiclo detectadoErro de dependência mútua na grade

## Funcionalidades

### Sequência válida de todas as disciplinas gerada por Ordenação Topológica
### Consulta de pré-requisitos diretos e indiretos de qualquer disciplina
### Consulta de quais disciplinas dependem de uma dada matéria
### Caminho mínimo entre duas disciplinas
### Detecção automática de ciclos na grade
### Exportação de visualização interativa em HTML


## Tecnologias utilizadas

> Python 3
>
> NetworkX — construção do grafo e algoritmos
>
> Pyvis — geração da visualização HTML interativa
