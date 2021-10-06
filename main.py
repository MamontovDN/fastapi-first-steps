from typing import Optional, List

from fastapi import (
    FastAPI,
    Query,
    Path,
    Body,
    Cookie,
    Header,
    status,
    File,
    UploadFile,
    Form,
    HTTPException,
)
from models import ModelName, Post, UserIn, UserDB, UserOut, Item


app = FastAPI()

@app.get("/exception/{param}")
async def excep(param: bool):
    if param:
        raise HTTPException(status_code=400, detail="You want this")
    return {"message": "and what ... ?"}


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploads/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.post("/file")
async def create_file(file: bytes = File(...)):
    return {'file_size': len(file)}


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    return {'filename': file.filename}


def hash_pass(password: str) -> str:
    return ''.join([chr(ord(ch)+1) for ch in password])


def save_user(user: UserIn) -> UserDB:
    password = hash_pass(user.password)
    user_db = UserDB(**user.dict(), hash_password=password)
    print(user_db)
    return user_db


@app.post("/auth", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def auth(user: UserIn):
    new_user = save_user(user)
    return new_user


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


@app.get('/headers')
async def read_headers(
        user_agent: Optional[str] = Header(None),
        admin_agent: Optional[str] = Header(None, convert_underscores=False),
        band_agent: Optional[List[str]] = Header(None),
):
    return {
        "user-agent": user_agent,
        "admin_agent": admin_agent,
        "band-agent": band_agent,
    }


@app.get("/cookies")
async def read_cookie(cookie_2: Optional[str] = Cookie(None)):
    return {'cookie_2': cookie_2}


@app.put("/body_params/{item_id}")
async def update_item(item_id: int,
                      item: Item = Body(...),
                      user: UserIn = Body(..., embed=True),
                      ):
    results = {"item_id": item_id, "user": user}
    return results


@app.get('/path_params/{item_id}')
async def read_items(
        item_id: int = Path(
            ...,
            title="The ID of the item to get",
            description="Description of item's id to get",
            ge=1,
        ),
        q: Optional[str] = Query(None, alias='item-query'),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results











@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get('/enum/{name}')
async def enums(name: ModelName):
    if name == ModelName.alexnet:
        return {"model_name": name, "message": "Deep Learning FTW!"}

    if name.value == "lenet":
        return {"model_name": name, "message": "LeCNN all the images"}

    return {"model_name": name, "message": "Have some residuals"}


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/items/{pk}")
async def items(pk: int):
    return pk
