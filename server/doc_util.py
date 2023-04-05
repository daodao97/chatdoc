from PyPDF2 import PdfReader
import sys
import os
import logging
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, QuestionAnswerPrompt, QueryMode, LLMPredictor
from consts import BASE_DIR
import ebooklib
from ebooklib import epub
from epub2txt import epub2txt
from langchain.chat_models import ChatOpenAI
from llama_index import download_loader
import docx2txt

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0.2, model_name="gpt-3.5-turbo"))
CJKPDFReader = download_loader("CJKPDFReader")
SimpleWebPageReader = download_loader("SimpleWebPageReader")

QUESTION_ANSWER_PROMPT_TMPL_2 = """
You are an AI assistant providing helpful advice. You are given the following extracted parts of a long document and a question. Provide a conversational answer based on the context provided.
If you can't find the answer in the context below, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
Context information is below.
=========
{context_str}
=========
{query_str}
"""

QA_PROMPT_TMPL = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "{query_str}\n"
)


class Doc:
    def __init__(
            self,
            doc_id: str,
            filename: str = ""
    ) -> None:
        self.dir_name = doc_id

        full_dir = os.path.join(BASE_DIR, self.dir_name)
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)

        self.filename = filename
        self.file_path = os.path.join(BASE_DIR, self.dir_name, filename)
        self.data_file = os.path.join(BASE_DIR, self.dir_name, "data.txt")
        self.index_file = os.path.join(BASE_DIR, self.dir_name, "index.json")

    async def save(self, content: bytes):
        with open(self.file_path, "wb") as f:
            f.write(content)

    def build_txt(self, doc_type: str):
        if doc_type == 'application/epub+zip':
            self.extract_epub()
        if doc_type == 'application/pdf':
            self.extract_pdf()
        if doc_type == 'text/plain' or doc_type == 'text/markdown':
            self.data_file = self.file_path
        if doc_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            self.extra_docx()

    def extract_epub(self):
        res = epub2txt(self.file_path)
        with open(self.data_file, "a") as file:
            for i in range(len(res)):
                file.write(res[i])

    def extract_pdf(self):
        reader = PdfReader(self.file_path)
        print("total pages ", len(reader.pages))
        with open(self.data_file, "a") as file:
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                file.write(text)

    def extra_docx(self):
        res = docx2txt.process(self.file_path)
        with open(self.data_file, "a") as file:
            file.write(res)

    def build_index(self, doc_type: str):
        if doc_type == 'web':
            self.build_web()
            return

        documents = SimpleDirectoryReader(
            input_files=[self.data_file]).load_data()
        index = GPTSimpleVectorIndex(documents)
        index.save_to_disk(self.index_file)

    def build_web(self):
        loader = SimpleWebPageReader()
        documents = loader.load_data(urls=[self.filename])
        index = GPTSimpleVectorIndex(documents)
        index.save_to_disk(self.index_file)

    def query(self, question: str):
        print("query2", self.index_file, self.file_path)
        loader = CJKPDFReader()
        index_file = self.index_file

        if os.path.exists(index_file) == False:
            documents = loader.load_data(file=self.file_path)
            index = GPTSimpleVectorIndex(documents)
            index.save_to_disk(index_file)
        else:
            index = GPTSimpleVectorIndex.load_from_disk(index_file)

        QUESTION_ANSWER_PROMPT = QuestionAnswerPrompt(
            QUESTION_ANSWER_PROMPT_TMPL_2)

        return index.query(
            query_str=question,
            llm_predictor=llm_predictor,
            text_qa_template=QUESTION_ANSWER_PROMPT,
            # response_mode="tree_summarize",
            similarity_top_k=3,
        )

    def query2(self, question: str):
        print("query2", self.index_file, self.file_path)
        loader = CJKPDFReader()
        index_file = self.index_file

        if os.path.exists(index_file) == False:
            documents = loader.load_data(file=self.file_path)
            index = GPTSimpleVectorIndex(documents)
            index.save_to_disk(index_file)
        else:
            index = GPTSimpleVectorIndex.load_from_disk(index_file)

        QUESTION_ANSWER_PROMPT = QuestionAnswerPrompt(
            QUESTION_ANSWER_PROMPT_TMPL_2)

        return index.query(
            query_str=question,
            llm_predictor=llm_predictor,
            text_qa_template=QUESTION_ANSWER_PROMPT,
            response_mode="tree_summarize",
            similarity_top_k=3,
        )
