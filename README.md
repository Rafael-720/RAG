# RAG de IA Generativa para Respostas a Perguntas sobre Documentos usando LLMs e NLP

🚀 Bem-vindo ao repositório do nosso projeto que combina IA generativa com a técnica de Retrieval-Augmented Generation (RAG) para processar e responder perguntas baseadas em documentos PDF. Este sistema utiliza tanto modelos de LLMs open source (rodando local) quanto o poderoso GPT-4o da OpenAI, garantindo uma solução versátil e eficiente.

## 🌟 O que é RAG?

O RAG é uma técnica que combina métodos de recuperação de informações (retrieval) com geração de respostas (generation). Primeiro, o sistema busca documentos relevantes ou trechos de textos que possuem informações chave. Em seguida, essas informações são usadas como contexto para gerar respostas precisas e informativas. Este método é particularmente útil para criar sistemas de resposta a perguntas que podem dinamicamente utilizar conhecimento armazenado em uma base de dados vasta e diversificada.

## 🛠️ Características Principais

- **Embeddings de Texto com OpenAI**: Utilização dos embeddings da OpenAI(text-embedding-3-small-OpenAi) para transformar textos em representações vetoriais que podem ser eficientemente buscadas e comparadas.
- **Embeddings alternativo**: Flexibilidade para utilizar embeddings gerados por modelos locais open source(OllamaEmbeddings) ou através de serviços proprietarios(BedrockEmbeddings-AWS), baseados nas necessidades de precisão e relevância dos seguimentos.
- **Chroma para Armazenamento Vetorial**: Utilização eficaz do banco de dados vetorial Chroma para armazenamento e recuperação rápida de documentos.
- **RAG com LLMs Offline e GPT-4**: Combinação de modelos de linguagem open source e o poderoso GPT-4o para geração de respostas baseadas no contexto extraído dos documentos.

## Estrutura do Projeto

- **get_embedding_function.py**: Script para configurar e obter a função de embeddings utilizando a OpenAI.
- **populate_database.py**: Script para popular o banco de dados com documentos PDF, permitindo resetar o banco e listar documentos.
- **query_data.py**: Script para consultar o banco de dados utilizando um modelo de linguagem para responder perguntas baseadas no contexto dos documentos.
- **query_data_gpt.py**: Variante do script de consulta utilizando o modelo GPT da OpenAI.

## Requisitos

- Python 3.8+
- Ollama
- LLM baixado
- Key api da OpenAi
- Bibliotecas listadas no arquivo `requirements.txt`

## 📦 Configuração e Instalação

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/Rafael-720/RAG.git
    cd RAG
    ```

2. **Prepare o ambiente virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: `venv\Scripts\activate`
    ```

3. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure as variáveis no `.env`** para acesso ao GPT-4:
    ```env
    OPENAI_API_KEY=sua_chave_api_openai
    ```

## 🚀 Uso do Sistema

### Gerenciamento de Dados

- **Adicionar documentos**: `python populate_database.py --add caminho/para/documento.pdf`
- **Listar documentos**: `python populate_database.py --list`
- **Resetar o banco de dados**: `python populate_database.py --reset`

### Consultas Dinâmicas

- **Usando LLM local** Antes de iniciar, execute `ollama serve` e assegure que o modelo LLM desejado como Mistral ou Llama3, esteja operacional na sua máquina:
    ```bash
    python query_data.py "Insira aqui sua pergunta sobre o documento?"
    ```

- **Usando GPT-4** Certifique-se de que a chave API da OpenAI está configurada corretamente:
    ```bash
    python query_data_gpt.py "Insira aqui sua pergunta sobre o documento"
    ```

## 🤝 Contribuições

Sinta-se livre para contribuir! Melhore a funcionalidade ou documentação enviando pull requests ou abrindo issues.

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 📞 Contato

Rafael Oliveira - [LinkedIn](https://linkedin.com/in/rafael-oliveira720)

---

💡 Projeto dedicado ao avanço e aplicação prática de tecnologias de IA em processamento de linguagem natural.
