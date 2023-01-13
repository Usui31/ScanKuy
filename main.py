from fastapi import FastAPI, Request, Depends
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import datetime
from database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# class User(BaseModel):
#     id: int

# class Image(BaseModel):
#     image_id : int
#     name : str
#     format : str

# class Scanner(BaseModel):
#     scan_id : int
#     user_id : int
#     image_id : int
#     data_time : str

# class Text(BaseModel):
#     text_id : int
#     scan_id : int
#     jumlah_huruf : int
#     text : str
class Inputan(BaseModel):
    text: str
    nama: str
    extensi: str
    dateTime: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/test")
async def get_users(db:Session=Depends(get_db)):
    return db.execute("SELECT * FROM user_scankuy").fetchall()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about_us", response_class=HTMLResponse)
async def about_us(request: Request):
    return templates.TemplateResponse("about-us.html", {"request": request})

@app.post("/extract_text")
async def extract(req : Inputan, db:Session=Depends(get_db)):
    req_dict = req.dict()
    x = datetime.datetime.now()
    count = len([ele for ele in req.text if ele.isalpha()])
    try:
        db.execute("INSERT INTO image VALUES(null, '%s', '%s')"%(req.nama, req.extensi))
        db.commit()
        db.close()
    except:
        return "ERROR"
    try:

        db.execute("INSERT INTO user_scankuy VALUES(null)")
        db.commit()
        db.close()
    except:
        return "EROR"
    hasil = db.execute("SELECT User_ID from user_scankuy ORDER BY User_ID DESC").fetchone()
    for i in hasil:
        user_id = i
        db.close()
        hasil_image_id = db.execute("SELECT Image_ID from image ORDER BY Image_ID DESC").fetchone()
        for j in hasil_image_id:
            image_id = j
            db.execute("INSERT INTO scanner VALUES(null, %d, %d, '%s')"%(image_id, user_id, x))
            db.commit()
            db.close()
    
    hasil_scan_id = db.execute("SELECT Scan_ID from scanner ORDER BY Scan_ID DESC").fetchone()
    for k in hasil_scan_id:
        scan_id = k
        db.execute("INSERT INTO text_digital VALUES(null, %d, %d, '%s')"%(scan_id, count, req.text))
        db.commit()
        db.close()
    return req_dict