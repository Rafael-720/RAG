import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
#from langchain_community.llms.ollama import Ollama
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from get_embedding_function import get_embedding_function
from dotenv import load_dotenv
import os

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")
    

    #model = Ollama(model="mistral")
    response_text = model.invoke(prompt)
    # Parse the response
    #parser = SimpleJsonOutputParser()
    #parsed_response = parser.parse(response_text)

    #complete_response = parsed_response.get("answer", "")
    #followup_question = parsed_response.get("followup_question", "")


    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(response_text)
    return response_text


if __name__ == "__main__":
    main()
