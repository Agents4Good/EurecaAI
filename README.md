<h1 align="center">EurecaAI</h1>

> Este projeto tem como objetivo criar um sistema de agentes inteligentes capazes de responder perguntas relacionadas à Universidade Federal de Campina Grande (UFCG), usando dados reais obtidos pela API oficial Eureca, para fornecer respostas precisas e contextualizadas. O sistema funciona como um chatbot.

---
## 🏛️ Arquitetura

O sistema multiagente é baseado em uma arquitetura de supervisor, onde diferentes agentes desempenham papéis específicos e um agente supervisor coordena a interação entre eles, com o objetivo de alcançar um comportamento global otimizado para o sistema como um todo. Abaixo está uma visão geral:

| **Agente**       | **Descrição**                              |
|-------------------|--------------------------------------------|
| Supervisor         | Coordenar a interação entre os demais agentes. |
| Cursos         | Obter informações da API com relação a cursos, currículos e estudantes da UFCG. |
| Disciplinas e Turmas         | Obter informações da API com relação as disciplinas, turmas, plano de aula, etc.|
| Campus         | Obter informações da API com relação aos campi, calendários e períodos. |
| Setor         | Obter informações da API com relação aos setores (unidades acadêmicas), professores e estágios.|
| Detector         | Detectar se o texto recebido da entrada possui tags que indicam tentativa de inserção de informações confidenciais. |
| Agregador         | Agregar as respostas de um ou mais agentes e compilá-las na saída final de cada fluxo de execução do sistema. |

---
## 🚀 Instalação

Para instalar basta executar o código abaixo:

```
pip install -r requirements.txt
```

---
## 👩🏻‍💻 Uso

1. Utilizando o Flask

Para executar o chatbot com uma mini aplicação Flask que serve um front-end, basta executar o código abaixo:

```
python -m flask_app.app
```

2. Utilizando linha de comando

Também é possível executar o chatbot diretamente pela linha de comando de duas formas:

```
python -m src.main
```
Onde será iniciada uma sessão iterativa, a qual pode-se conversar com o chatbot.

```
python -m src.main "Sua pergunta aqui"
```
Onde será feita uma única consulta ao chatbot.


---
## 🤝 Contribuição
Contribuições são bem-vindas! 
Siga os passos abaixo para colaborar: 
- Faça um fork do repositório;
- Modifique o que desejar e crie um pull request;
- Detalhe o pull request. Descreva suas alterações.
---

## 📜 Licença
Este projeto é licenciado sob a MIT - License
