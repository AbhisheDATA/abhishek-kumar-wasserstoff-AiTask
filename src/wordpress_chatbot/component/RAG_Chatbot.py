import os
from dotenv import load_dotenv
from wordpress_chatbot.helper import read_yaml,load_api_key
from wordpress_chatbot.component.vectorstore import DocumentProcessor 
from wordpress_chatbot import CONFIG_FILE_PATH
from langchain_community.vectorstores import FAISS

#######################################################################
#           for LLM based service  Import openai and google_genai 
####################################################################### 
from langchain_openai import  ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

######################################################################
#            langchain prompts, memory, chains...
######################################################################
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory

class Chatbot:
    def __init__(self, llm_provider):
        load_dotenv()
        config_filepath = CONFIG_FILE_PATH
        self.store=DocumentProcessor(llm_provider)
        self.embedding=self.store.load_embedding_model()
        self.config = read_yaml(config_filepath)
        self.llm_provider = llm_provider

    def initialize_llm(self):
        """
        This function initializes the LLM based on the specified LLM provider.
        It retrieves the API key for the LLM provider and creates instances of the LLM for standalone query generation and response generation.

        Returns:
            tuple: A tuple containing instances of the LLM for standalone query generation and response generation.
        Raises:
            ValueError: If the specified LLM provider is not supported.
        """
        # Load the API key based on the specified LLM provider
        if self.llm_provider == "OpenAI":
            OPENAI_API_KEY = load_api_key("OpenAI")
            standalone_query_generation_llm = ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model=self.config.OpenAI_model,
                temperature=0.4,
            )
            response_generation_llm = ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model=self.config.OpenAI_model,
                temperature=0.4,
                model_kwargs={"top_p": self.config.top_p.openai},
            )
        elif self.llm_provider == "GoogleAI":
            GOOGLE_API_KEY = load_api_key("GoogleAI")
            standalone_query_generation_llm = ChatGoogleGenerativeAI(
                google_api_key=GOOGLE_API_KEY,
                model=self.config.googleAI_model,
                temperature=0.4,
                convert_system_message_to_human=True,
            )
            response_generation_llm = ChatGoogleGenerativeAI(
                google_api_key=GOOGLE_API_KEY,
                model=self.config.googleAI_model,
                temperature=0.4,
                top_p=self.config.top_p.googleai,
                convert_system_message_to_human=True,
            )
        else:
            raise ValueError("Unsupported LLM provider:", self.llm_provider)

        # Return instances of the LLM for standalone query generation and response generation
        return standalone_query_generation_llm, response_generation_llm
    
    def vectorstore_retriver(self):
        """
        Retrieve the vector store and create a retriever.

        This function loads the local vector store using the specified embedding model.
        It then creates a retriever from the loaded vector store with search parameters.

        Returns:
            faiss_retriever: A retriever object created from the loaded vector store.

        Raises:
            Exception: If there is an error in loading the local vector store.
        """
        try:
            # Get the path to the local vector store
            local_vector_dir = self.config.VECTOR_STORE_DIR
            
            # Load the local vector store using the specified embedding model
            local_db = FAISS.load_local(local_vector_dir, self.embedding)
            
            # Create a retriever from the loaded vector store with search parameters
            retriever = local_db.as_retriever(search_kwargs={'k': 6})
            
            return retriever
        except Exception as e:
            # Raise an exception if there is an error in loading the local vector store
            raise Exception("Error in loading local vector store: " + str(e))
        
    def answer_template(self):
        """Pass the standalone question along with the chat history and context
        to the `LLM` wihch will answer."""

        template = f"""you are conversational chatbot agent which Answer the  question using the provided context and chat history. 
                 using only the following context (delimited by <context></context>) and give the answer at end.
         
                <context>
                {{chat_history}}

                {{context}} 
                </context>

                Question: {{question}}

                answer:
                """
        return template

    def conversational_qa_chain(self, retriever):
        """
        Create a conversational QA chain.
        This function constructs a chain for conversational question answering using retrieval-based models.
        It sets up prompts for rephrasing questions and generating answers, initializes language models,
        and configures the conversation memory.

        Args:
            retriever: A retriever object used for retrieving relevant documents.

        Returns:
            ConversationalRetrievalChain: A chain for conversational question answering.

        Raises:
            Exception: If there is an error in initializing the language models or constructing the chain.
        """
        # Define prompt templates for rephrasing questions and generating answers
        condense_question_prompt = PromptTemplate(
            input_variables=["chat_history", "question"],
            template="""Given the following conversation and a follow-up question, 
            rephrase the follow-up question to be a standalone question.\n\n
            Chat History:\n{chat_history}\n
            Follow-Up Input: {question}\n
            Standalone Question:""",
        )
        
        answer_prompt = ChatPromptTemplate.from_template(self.answer_template())

        # Define memory configuration for conversation history
        memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="answer",
            input_key="question",
        )

        # Initialize standalone query generation LLM and response generation LLM
        self.standalone_query_generation_llm, self.response_generation_llm = self.initialize_llm()

        try:
            # Create the conversational QA chain
            chain = ConversationalRetrievalChain.from_llm(
                condense_question_prompt=condense_question_prompt,
                combine_docs_chain_kwargs={"prompt": answer_prompt},
                condense_question_llm=self.standalone_query_generation_llm,
                llm=self.response_generation_llm,
                memory=memory,
                retriever=retriever,
                chain_type="stuff",
                verbose=False,
                return_source_documents=True
            )

            return chain
        except Exception as e:
            # Raise an exception if there is an error in initializing the language models or constructing the chain
            raise Exception("Error in initializing conversational QA chain: " + str(e))
        
'''
# Initialize the Chatbot instance
chatbot = Chatbot(llm_provider="GoogleAI")

# Retrieve the vector store and create a retriever
retriever = chatbot.vectorstore_retriver()
chain=chatbot.conversational_qa_chain(retriever)
response=chain.invoke({"question": " Getting Python "})
answer = response["answer"]
print(answer)
'''