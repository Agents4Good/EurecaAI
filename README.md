# MCP Tools UFCG

Este repositório contém uma coleção de **tools MCP** desenvolvidas para acessar dados acadêmicos da UFCG. As ferramentas são implementadas em Python e podem ser utilizadas diretamente via **MCP Server**.

## Como rodar o MCP Server

Para iniciar o servidor e carregar todas as tools, utilize o comando:

```
python -m main
```
Após a inicialização, todas as tools estarão disponíveis para agentes cadastrados no MCP.

---

## Categorias de Tools

As tools estão organizadas por tipo de dado que manipulam:

- **Campus**  
- **Setores**  
- **Cursos**  
- **Disciplinas**  
- **Estágios**  
---

## Campus

- **Descrição**: Permite consultar informações sobre todos os campi da UFCG.  
- **Informações retornadas**: código do campus, nome completo e representação em algarismos romanos.  
- **Uso típico**: listar todos os campi disponíveis para outros filtros ou consultas.

---

## Setores

- **Descrição**: Permite consultar todos os setores de um campus específico.  
- **Informações retornadas**: código do setor, descrição, código do campus e e-mail de contato (quando disponível).  
- **Uso típico**: identificar unidades acadêmicas ou administrativas de cada campus.

---

## Cursos

- **Descrição**: Retorna todos os cursos oferecidos em um campus específico da UFCG.  
- **Informações retornadas**: código e nome do curso, status, grau do curso, setor responsável, turno, período de início, código INEP, modalidade acadêmica, currículo vigente, área de retenção e ciclo do ENADE.  
- **Uso típico**: consultar cursos ativos e obter informações detalhadas para planejamento acadêmico.

---

## Disciplinas

- **Descrição**: Lista todas as disciplinas de um curso em um campus específico.  
- **Informações retornadas**: dados detalhados de cada disciplina, incluindo código, nome, carga horária, período, e outros atributos acadêmicos.  
- **Uso típico**: construir matrizes curriculares ou verificar informações detalhadas de cada disciplina.

---




