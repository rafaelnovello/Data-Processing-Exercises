# Data-Processing-Exercises

Repo para compartilhar experimentos com processamento e engenharia de dados.

# Experimentos

O primeiro experimento, com scripts em Python e Go, faz a extração de dados de aquivos de log e a inserção dos dados em um banco de dados NoSQL (ArangoDB).

As premissas para o experimento são:

- Fazer a extração dos dados sem usar regex
- Fazer a inserção dos dados em lotes de 2000 registros
- Executar de forma sincrona

O uso de regex para a extração dos dados foi testada preveamente mas não apresentou boa performance e, por isso, foi descartada.

Foram feitos testes usando CPython (Python 3.5), PyPy2.7 (v5.8.0) e Go (v1.8.3). Todos os testes rodaram no mesmo hardware com OS Ubuntu 14.04, ArangoDB 3.2.1 local e processaram a mesma massa de dados.

A massa de dados consiste em 100 arquivos de log no formato texto, num total de 2,4G de dados (2402 mega).

Os tempos de execução foram obtidos com o comando `time` do sistema operacional. Os resultados foram:

Engine|Tempo de Exc|Total de registros no BD
-|------------|------------------------
CPython|3:50 min|10.560.341
PyPy|2:41 min|10.560.341
Go|4:25 min|10.560.341

Abaixo esta um print do painel de controle do ArangoDB onde é possível ver as taxas de requisições por segunto e de transferência de dados por segundo:

![ArangoDB-Panel](ArangoDB-Panel.png)

Dentre os 3 testes o PyPy foi o que conseguiu as melhores taxas de requisição e transferência por segundo.

## Considerações

Por não ter experiência com a linguagem Go, é quase certo que existem várias oportunidades de otimização no script Go. Por isso peço que entrem em contato se souberem como otimizar o script em Go (e o script Python também!)
