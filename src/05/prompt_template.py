from langchain_core.prompts import PromptTemplate

template =  """
다음 문서를 읽고 지;ㄹ문에 답하ㅣ오.
문서 : {doc}
질문 : {q}
답변 : 
"""

prompt = PromptTemplate(
    input_variables=["doc", "q"],
    template=template
)

result = prompt.format(
    
)