import json, pandas, re, os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatDeepInfra
from dotenv import load_dotenv
from pymongo import MongoClient
from rapidfuzz import process, fuzz
import unicodedata

load_dotenv(override=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongoClient("mongodb://localhost:27017/")
CLIENT_NOSQL = client["eureca_chat"]

class GerenciadorNoSQLAutomatizado:
    def __init__(self, db, collection_name, json_data, prompt, temperature=0.0):
        self.db = db
        self.collection = self.db[collection_name]
        self.llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=temperature)
        #self.llm = ChatDeepInfra(model="openai/gpt-oss-20b", temperature=0)
        self.path = os.path.join(BASE_DIR, "", collection_name, "tabela.json")
        self.meaning = self.get_meaning(collection_name)
        self.prompt = prompt

        try:
            self.json_data = json.loads(json.dumps(json_data))
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao converter o JSON de exemplo: {e}")

        if isinstance(self.json_data, dict):
            self.documentos = [self.json_data]
        elif isinstance(self.json_data, list):
            self.documentos = self.json_data
        else:
            raise ValueError("JSON deve ser dict ou lista de dicts.")

        if self.documentos:
            pass
        else:
            raise ValueError("Lista de documentos está vazia.")

        self.attribes_json = self.get_attributes_json(
            self.documentos,
            self.meaning
        )


    def get_meaning(self, collection) -> dict:
        with open(self.path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Erro ao carregar o arquivo JSON: {e}")
        
        if collection not in data:
            raise ValueError(f"A tabela '{collection}' não foi encontrada no arquivo JSON.")
        
        meaning = {}
        for _, column_type in data[collection].items():
            mapper_key = column_type["mapper"]
            meaning[mapper_key] = f"{column_type['type']} -- {column_type['description']}"
        print(f"Significado dos campos: {meaning}")

        return meaning


    def get_attributes_json(self, documentos, meaning):
        if not isinstance(documentos[0], dict):
            raise ValueError("Itens da lista precisam ser dicts.")

        template = documentos[0]

        attributes = {}
        for key, value in template.items():
            if key == "_id": continue
            tipo = type(value).__name__
            significado = meaning.get(key, "")
            attributes[key] = f"{tipo} -- significado: {significado}"

        return attributes


    def invoke_pandas(self, input):
        df = pandas.DataFrame(self.documentos)
        formatted_prompt = self.prompt.format(
            format=json.dumps(self.attribes_json, indent=2, ensure_ascii=False),
            input=input
        )
        print(formatted_prompt)

        response_llm = self.llm.invoke(formatted_prompt).content.strip()
        response_llm = re.sub(r"```.*?```", lambda m: m.group(0).strip("`").split("\n", 1)[-1], response_llm, flags=re.DOTALL).strip()
        response_llm = re.sub(
            r"df\[(df\['(\w+)'\]\.str\.contains\('([^']+)'(?:, case=False)?\))\]",
            r"fuzzy_filter(df, '\2', '\3')",
            response_llm
        )

        def fuzzy_filter(df, col, term, limiar=80):
            term_norm = unicodedata.normalize('NFKD', term.lower()).encode('ASCII', 'ignore').decode('utf-8')
            col_norm = df[col].apply(lambda x: unicodedata.normalize('NFKD', x.lower()).encode('ASCII', 'ignore').decode('utf-8'))
            matches = process.extract(term_norm, col_norm, scorer=fuzz.partial_ratio)
            indices = [i for _, score, i in matches if score >= limiar]
            return df.iloc[indices]

        try:
            resultado = eval(response_llm, {"df": df, "fuzzy_filter": fuzzy_filter})
        except Exception as e:
            resultado = f"Erro ao executar a expressão: {e}"

        del df

        result = {
            "Consulta gerada": response_llm,
            "Resultado": resultado.to_dict(orient="records") if hasattr(resultado, "to_dict") else resultado
        }

        print(result)

        return result
    

    def invoke_mongodb(self, input):
        self.collection.insert_many(self.documentos)
        formatted_prompt = self.prompt.format(
            format=json.dumps(self.attribes_json, indent=2, ensure_ascii=False),
            input=input
        )
        print(formatted_prompt)

        response_llm = self.llm.invoke(formatted_prompt)
        print(f"\n\nConsulta gerada: {response_llm}")

        try:
            query_dict = eval(response_llm)
            filtro = query_dict.get("filter", {})
            projecao = query_dict.get("projection", {"_id": 0})
            if "_id" not in projecao:
                projecao["_id"] = 0

            resultados = list(self.collection.find(filtro, projecao))
            self.collection.delete_many({})

            resultado_NoSQL = {
                "NoSQL": query_dict,
                "Resultado": resultados
            }

            return resultado_NoSQL

        except Exception as e:
            print("Erro ao processar a consulta:", e)