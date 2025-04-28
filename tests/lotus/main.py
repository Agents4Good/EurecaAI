from lotus.models import LM, SentenceTransformersRM
import pandas as pd
import lotus

lm = LM(model="ollama/llama3.2")
rm = SentenceTransformersRM(model="intfloat/e5-base-v2")

lotus.settings.configure(lm=lm, rm=rm)

data = {
"Course Name": [
    "LETRAS - LÍNG.PORT./LÍNG.FRANC.(LIC)-D",
    "LETRAS - LÍNGUA INGLESA (LIC) - D",
    "LETRAS - ESPANHOL (LICENCIATURA) N",
    "LETRAS- LÍNGUA PORTUGUESA (LIC) - D",
    "LETRAS - LÍNGUA PORTUGUESA (LIC) - N",
    "LETRAS - LIBRAS (LIC) - D",
    "CIÊNCIAS ECONÔMICAS - M",
    "CIÊNCIAS ECONÔMICAS - N",
    "CIÊNCIA DA COMPUTAÇÃO - D",
    "ENGENHARIA ELÉTRICA"
]
}
df = pd.DataFrame(data)
user_instruction = (
    "Considere o curso {Course Name}. Retorne apenas o nome do curso mais similar, "
    "priorizando similaridade com 'Ciência da Computação'. "
    "Responda somente com o nome do curso, sem explicações."
)
df = df.sem_map(user_instruction)
print(df)

for method in ["quick", "heap", "naive"]: 
    sorted_df, stats = df.sem_topk("Which {Course Name} most similar to ciencia da computacao?", K=2, method=method, return_stats=True)
    print(sorted_df)
    print(stats)


df = df.sem_index("Course Name", "index_dir").sem_search(
    "Course Name",
    "Qual o curso mais similar a ciencia da computação?",
    K=4,
    n_rerank=3,
)
print(df)