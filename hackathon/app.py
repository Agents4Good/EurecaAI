from flask import Flask, request, render_template, jsonify
from langchain_community.chat_models import ChatDeepInfra
from langchain_core.messages import HumanMessage
import asyncio, json
from dotenv import load_dotenv
load_dotenv(override=True)


app = Flask(__name__, static_url_path="/static")

"""_summary_
Retorna a página HTML de chat a ser renderizada.

Returns:
    Any: Retorna a página de chat.
"""
@app.route('/')
def home():
    return render_template('index.html')


"""_summary_
Deleta um chat já criado pelo usuário.

Returns:
    dict: Retorna uma mensagem 'apagado' e o status OK informado que o chat foi deletado. 
"""
@app.route('/delete_chat', methods=["POST"])
def delete_chat() -> dict:
    return jsonify({"msg": "apagado"}), 200


"""_summary_
Abre uma conexão HTTP com o frontend para receber a pergunta e retorna um resumo 
para ser renderizado no Front-End sobre o tópico abordado.
O resumo contém 3 palavras e será mostrado no drawer como titulo da conversa.

Returns:
    dict: Retorna um resumo da conversa com até 3 palavras.
"""
@app.route('/resumir', methods=["POST"])
def resumir() -> dict:
    data = request.get_json()
    if not data or 'texto' not in data:
        return jsonify({"erro": "Campo 'texto' é obrigatório"}), 400

    texto = data['texto']

    try:
        llm = ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
        resposta = llm.invoke(
            f"""
            Gere um título de até 3 palavras para o texto a seguir:
            '{texto}'
            
            *IMPORTANTE*:
            - Você sempre deve gerar um título, não faça nada além disso.
            - Sempre gere no seguinte formato: {{"titulo": "titulo_gerado"}}
            """
        )

        resumo = resposta.content if hasattr(resposta, "content") else str(resposta)
        resumo = resumo.replace("'", '"')
        resumo = json.loads(resumo)
        return jsonify({"resumo": resumo['titulo']}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar resumo: {str(e)}"}), 500


"""_summary_
Função assincrona que usará os agentes para responder a pergunta do usuário.
"""
async def process_query(query):
    """
    Processa a consulta do usuário usando o sistema de agentes.
    """
    config = {"configurable": {"thread_id": "1"}}
    inputs = {"messages": [HumanMessage(content=query)]}
    response = []

    """
    async for chunk in system.astream(inputs, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()
        response.append(chunk["messages"][-1].content)
    """
    return response[-1] if response else "Desculpe, não consegui processar sua solicitação."


"""_summary_
Função que recebe uma entrada para os agentes processar e respoonder a pergunta do usuário.

Returns:
    Any: Retorna a resposta dos agentes que respondem a pergunta feita pelo usuário.
"""
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_input']
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot_message = loop.run_until_complete(process_query(user_message))
    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")
        bot_message = "Desculpe, ocorreu um erro ao processar sua solicitação."
    return {'response': bot_message}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)