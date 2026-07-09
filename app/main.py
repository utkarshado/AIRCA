from config import PDF_PATH, PDF_STORE, CODEBASE_PATH, CODEBASE_STORE
#llm
from llm.client import OLLAMAClient
#history
from memory.conversation_memory import ChatHistory
#pdf
from rag.ingestion import PDFIngestor
from rag.rag_service import PDFRAGService
from agents.pdf_agent import PDFAgent
#code
from rag.ingestion import CodeIngestor
from rag.rag_service import CODERAGService
from agents.coding_agent import CodingAgent
#agents
from agents.assistant import Assistant

def main():
    client= OLLAMAClient()
    history= ChatHistory()

    print("Loading PDF...")
    pdf_ingestor=PDFIngestor()

    pdf_vector_store= pdf_ingestor.ingest(PDF_PATH, PDF_STORE)
    pdf_rag= PDFRAGService(pdf_vector_store)

    pdf_agent= PDFAgent(client, history, pdf_rag)

    print("Loading Codebase...")
    code_ingestor= CodeIngestor()

    code_vector_store= code_ingestor.ingest(CODEBASE_PATH, CODEBASE_STORE) 
    code_rag= CODERAGService(code_vector_store)

    code_agent= CodingAgent(client, history, code_rag)

    assistant= Assistant(client, history, pdf_agent, code_agent)
    print("Current Mode : Chat")

    while True:
        user_input=input("You : ")
        if user_input.strip().lower()=="exit":
            break
        
        elif user_input.strip().lower()=="clear":
            history.clear()
            print("cleared")
            continue

        elif user_input.strip().lower()=="list":
            history.list()
            continue

        elif user_input.strip().lower()=="chat":
            assistant.set_mode("chat")
            print("Switched to Chat Mode.")
            continue

        elif user_input.strip().lower()=="pdf":
            assistant.set_mode("pdf")
            print("Switched to PDF Mode.")
            continue

        elif user_input.strip().lower()=="code":
            assistant.set_mode("code")
            print("Switched to Code Mode.")
            continue

        response= assistant.handle_request(user_input)

        print(response)
      
    
if __name__=="__main__":
    main()