
from typing import List
import unicodedata
import spacy
from transformers import BertTokenizer, BertModel
import torch
import os
import numpy as np
from nltk.corpus import stopwords

#nltk.download('stopwords')
#nltk.download('wordnet')

if os.path.isdir("./bert_tokenizer") and os.path.isdir("./bert_model"):
    tokenizer = BertTokenizer.from_pretrained("./bert_tokenizer")
    model = BertModel.from_pretrained("./bert_model")
else:
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    tokenizer.save_pretrained("./bert_tokenizer")
    model.save_pretrained("./bert_model")


#!guardrails hub install hub://guardrails/teste --quiet

def remove_pointing(text:str) -> str:
    """
        Remove pontuação do texto 

        Args:
            text: O texto a ser tratado
        
        Returns:
            O texto sem pontuação
    """
    ans = ""
    for c in text:
          if unicodedata.category(c) != 'Po':
               ans+=c
    return ans 

def remove_accent(text:str) -> str:
    """
        Remove os acentos das palavras do texto

        Args:
            text: O texto a ser tratado
        
        Returns:
            O texto sem acentos
    """
    nfkd = unicodedata.normalize('NFKD', text)
    ans = ""
    for c in nfkd:
         if not unicodedata.combining(c):
              ans += c
    return ans

def lemmatize(text: str) -> str:
    """
        Aplica lematização no texto

        Args:
            text: O texto a ser tratado
        Returns:
            O texto lematizado
    """

    nlp = spacy.load('pt_core_news_sm')
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])
   

def remove_stopwords(text: str) -> str:  
        """
            Remove as palavras irrelevantes do texto

            Args:
                words:  texto a ser tratado
            
            Returns:
                Lista de string sem as palavras irrelevantes
        """

        text_without_pointing_and_accent = remove_accent(remove_pointing(text))
        lemmatized_text = lemmatize(text_without_pointing_and_accent)

        words_splitted = lemmatized_text.split()     
        stop_words = set(stopwords.words("portuguese"))

        relevant_text = ""
        for word in words_splitted:
            if word.lower() not in stop_words:
                relevant_text += word.lower() + " "

        return relevant_text
 
def generate_embeddings(text: str) -> List[List]:
       
    """
    Retorna os embeddings do texto passado como parâmetro da função.

    returns: Embeddings das palavras.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    embeddings = outputs.last_hidden_state
    sentence_embedding = embeddings.mean(dim=1)
    
    return sentence_embedding


def cosine_similarity(text1: str, text2: str) -> float:
    """
    Calcula a similaridae cosseno entre dois textos.
    Gera-se os embeddings para cada texto e em seguida, fazemos a similarida usando os embeddings. 

    returns: Grau de similaridade em um intervalo fechado entre 0 e 1.
    """
    emb_text1 = generate_embeddings(text1)
    emb_text2 = generate_embeddings(text2)
    
    emb_text1 = emb_text1.cpu().numpy()
    emb_text2 = emb_text2.cpu().numpy()
    
    dot_product = np.dot(emb_text1, emb_text2.T)
    text1Norm = np.linalg.norm(emb_text1)
    text2Norm = np.linalg.norm(emb_text2)
    
    return dot_product / (text1Norm * text2Norm)


def split_text(text, max_length: int = 10) -> List:
        
    """
    Divide o texto em alguns pedaços de frases.

    returns: Lista de frases.
    """
    tokens = tokenizer.tokenize(text)
    chunks = [tokenizer.convert_tokens_to_string(tokens[i:i + max_length]) for i in range(0, len(tokens), max_length)]
    
    return chunks


def similarity_between_texts(text1, text2) -> float:
        
    """
    Calcula a similaridade entre dois textos.

    returns: Similaridade cosseno.
    """
    split_text1 = split_text(remove_stopwords(text1))
    split_text2 = split_text(remove_stopwords(text2))
    
    similarities = []
    
    if len(split_text1) == 0 or len(split_text2) == 0:
        return 0
        
    for text1 in split_text1:
        for text2 in split_text2:
            similarities.append(cosine_similarity(text1, text2)[0][0])

    return np.mean(similarities)





