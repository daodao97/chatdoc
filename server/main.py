from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import time
from doc_util import Doc
import hashlib
from db_docs import Docs
from db_msg import Msg
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

app = FastAPI()
origins = ["http://127.0.0.1", "http://localhost:5173", "http://10.23.172.12:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  # 允许跨域的headers，可以用来鉴别来源等作用。


app.mount("/static", StaticFiles(directory="data"), name="static")


@app.get("/my_docs")
async def handle():
    docs = Docs.get_all()
    return {"data": docs}


@app.delete("/del/{doc_id}")
async def handle(doc_id):
    Docs.del_by_doc_id(doc_id=doc_id)
    return {"data": "success"}


@app.post("/upload")
async def handle(background_task: BackgroundTasks, file: UploadFile = File(...)):
    start = time.time()
    try:
        size = file.size
        data = await file.read()
        doc_id = hashlib.md5(data).hexdigest()
        doc = Doc(doc_id=doc_id, filename=file.filename)
        await doc.save(content=data)
        Docs(uid=0, doc_id=doc_id, doc_name=file.filename, doc_type=file.content_type, size=size).insert()
        background_task.add_task(file_task, doc_id)
        return {"message": "success", 'time': time.time() - start, 'filename': file.filename}
    except Exception as e:
        return {"message": str(e), 'time': time.time() - start, 'filename': file.filename}

class AddLink(BaseModel):
    link : str

@app.post("/add_link")
async def handle(background_task: BackgroundTasks,link: AddLink):
    start = time.time()
    try:
        print(link)
        doc_id = hashlib.md5(link.link.encode('utf8')).hexdigest()
        Docs(uid=0, doc_id=doc_id, doc_name=link.link, doc_type='web', size=0).insert()
        background_task.add_task(file_task, doc_id)
        return {"message": "success", 'time': time.time() - start}
    except Exception as e:
        return {"message": str(e), 'time': time.time() - start}


@app.get("/ask/{doc_id}")
async def handle(doc_id, question):
    try:
        res = Docs.get_by_doc_id(doc_id=doc_id)
        doc = Doc(doc_id=doc_id,filename=res['doc_name'])
        Msg(uid=0, doc_id=doc_id, role="user", content=question).insert()
        res = doc.query(question=question)
        Msg(uid=0, doc_id=doc_id, role="chatdoc", content=res).insert()
        return {"data": res, "doc_id": doc_id}
    except Exception as e:
        return {"message": str(e), "code": 500}


@app.get("/msg/{doc_id}")
async def handle(doc_id):
    res = Msg.get_by_doc_id(doc_id=doc_id, uid=0)
    return {"data": res, "doc_id": doc_id}


def file_task(doc_id: str):
    res = Docs.get_by_doc_id(doc_id=doc_id)
    if res == None:
        return

    doc = Doc(doc_id=res['doc_id'], filename=res['doc_name'])
    doc.build_txt(res['doc_type'])
    res['state'] = 1
    Docs(**res).update()

    doc.build_index(res["doc_type"])
    res['state'] = 2
    Docs(**res).update()


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", reload=True)
