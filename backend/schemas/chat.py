from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template='''
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know. 
      \n {content}
      \n {query}''',
    input_variables=['content', 'query']
)

