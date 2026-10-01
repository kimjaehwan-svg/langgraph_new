from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

emb = OpenAIEmbeddings(model="text-embedding-3-small")

vec = emb.embed_query("환불규정이 굼금해요")

print("차원 수 : ", len(vec))

first_10 = []

for value in vec[:10]:
    first_10.append(round(value, 4))

print("10개 :", first_10)

# first_1536 = []

# for value in vec[:1536]:
#     first_1536.append(round(value, 2))

# print("1536개 :", first_1536)