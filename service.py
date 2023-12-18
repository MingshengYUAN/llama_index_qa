import os
from llama_index import set_global_tokenizer
from transformers import AutoTokenizer
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import ServiceContext
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from langchain_llm import CustomLLM
import time
from log_info import logger
import numpy as np
import requests
import re 
from flask import Flask, request
from flasgger import Swagger
from flasgger.utils import swag_from
from swagger_template import template
from flask_session import *
from datetime import timedelta

#############

app = Flask(__name__)
swagger = Swagger(app, template=template)

#############

llm = CustomLLM(n=128)
set_global_tokenizer(AutoTokenizer.from_pretrained("../LLAMA2/model/llama-2-13b-chat-hg").encode)

embed_model = HuggingFaceEmbedding(model_name="all-mpnet-base-v2")
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

#############


@app.route("/upload_doc", methods=['POST'])
def upload_doc():
    start = time.time()
    file = request.file()['file']
    filename = request.get_json()['filename']

    save_path = os.path.join('./documents/', filename)
    save_path_share = './documents/share'
    if file:
        file.save(save_path)
        file.save(save_path_share)
    # print(data['text'])
    try:
        documents = SimpleDirectoryReader(f"./documents/{filename}").load_data()
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        index.storage_context.persist(persist_dir=f"./chroma_db/{filename}")
        try:
            if os.path.exists("./chroma_db/share"):
                os.system('rm -rf ./chroma_db/share')
            documents = SimpleDirectoryReader(f"./documents/share").load_data()
            index = VectorStoreIndex.from_documents(documents, service_context=service_context)
            index.storage_context.persist(persist_dir=f"./chroma_db/share")
            logger.info(f"Reload share db status: Success!")
            return {'response': "Upload document success!", "status": "Success!", "running_time": float{time.time() - start}}
        except Exception as e:
            logger.info(f"Reload share db status: Fail! Error: {e}")
            return {'response': "Upload document success! BUT SHARE DB FAIL", "status": "FAIL!", "running_time": float{time.time() - start}}
        logger.info(f"Load document status: Success!")
        logger.info(f"Save path: {save_path}")
    except Exception as e:
        logger.info(f"Load document Error: {e}")
        return {'response': f"Error: {e}", "status": "FAIL!", "running_time": float{time.time() - start}}

@app.route("/qa_from_doc", methods=['POST'])
def qa_from_doc():
    start = time.time()
    question = request.get_json()['question']
    filename = request.get_json()['filename']
    logger.info(f"Question: {question}")

    try:
        try:
            # rebuild storage context
            storage_context = StorageContext.from_defaults(persist_dir=f"./chroma_db/{filename}")
            # load index
            index = load_index_from_storage(storage_context)
        except Exception as e:
            return {"response":f"Load DB fail. Error: {e}", "status":"Faile!", "running_time": float(time.time() - start)}
            
        query_engine = index.as_query_engine()
        response = query_engine.query(question)

        logger.info(f"Answer from Doc Success! Response: {response}")
        return {"response":response, "status":"Success!", "running_time": float(time.time() - start)}

    except Exception as e:
        logger.info(f"Answer the doc error! Error: {e}")
        return {"response":f"Answer the doc error! Error: {e}", "status":"Faile!", "running_time": float(time.time() - start}






