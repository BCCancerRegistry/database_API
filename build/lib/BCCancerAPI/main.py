from fastapi import FastAPI, File, UploadFile, Request, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from BCCancerAPI.routes.userapi import userapp
from BCCancerAPI.applogging.middleware import RouterLoggingMiddleware
from BCCancerAPI.dbmodels.conn_manager import get_rw_eng
from BCCancerAPI.dbmodels.emarc import HL7Messages, MSH, OutputTable
from sqlalchemy import select, and_, not_, func
from BCCancerAPI.auth.validator import authapp
from BCCancerAPI.auth.validator import JWTBearer
import pandas as pd
from io import BytesIO
#from typing import Literal
#from dbmodels.config import Environ
#from applogging.middleware import RouterLoggingMiddleware
import logging
#Environ()
app = FastAPI()
print(app.openapi_schema)
app.include_router(authapp)
app.include_router(userapp)
rw_eng = get_rw_eng()
rw_session = Session(bind=rw_eng, autocommit=False, autoflush=False)
#Base.metadata.create_all(bind=rw_eng)
app.add_middleware(
    RouterLoggingMiddleware,
    logger=logging.getLogger(__name__)
)

@app.get("/", tags=["test"])
def read_root():
    # Example query to the database using SQLAlchemy
    db = rw_session
    #result = db.execute("SELECT 1")
    print(app.openapi_schema)
    return {"Hello": "World", "result": "Hurray"}


@app.get("/messages", tags=["MESSAGES"], dependencies=[Depends(JWTBearer())])
#@app.get("/messages", tags=["MESSAGES"])
async def get_messages(request: Request, from_date:str = None, to_date:str = None, limit: int = None):
    if limit is None:

        stmt = (
            select(
                HL7Messages.msgid.label('msgid'),
                HL7Messages.message
            )
            .distinct()
            .join(MSH, HL7Messages.msgid == MSH.msgid)
            .where(
                and_(
                    not_(HL7Messages.processingstatus.in_([3, 5])),
                    func.left(MSH.epathdatetimestamp, 8).between(from_date, to_date)
                )
            )
        )
    else:
        stmt = (
            select(
                HL7Messages.msgid.label('msgid'),
                HL7Messages.message
            )
            .distinct()
            .join(MSH, HL7Messages.msgid == MSH.msgid)
            .where(
                and_(
                    not_(HL7Messages.processingstatus.in_([3, 5])),
                    func.left(MSH.epathdatetimestamp, 8).between(from_date, to_date)
                )
            ).limit(limit)
        )
    result = rw_session.execute(stmt).fetchall()
    columns = ['MSGID',"MESSAGE"]  # Assuming the first Row has all the column names
    data = [dict(msgid=row[0],message=row[1]) for row in result]

    #df = pd.DataFrame(data, columns=columns)
    return data


@app.post("/save_output/", tags=["OUTPUT"], dependencies=[Depends(JWTBearer())])
#@app.post("/save_output/", tags=["OUTPUT"])

def save_output(file: UploadFile = File(...)):

    if file.filename.endswith(".csv"):
        # Read CSV using Pandas
        csv_content = pd.read_csv(BytesIO(file.file.read()), encoding="utf-8")
        print(csv_content)
        # Assuming the CSV columns match the model columns
        for _, row in csv_content.iterrows():
            # Create an instance of your SQLAlchemy model
            instance = OutputTable(**row.to_dict())

            # Add the instance to the session
            rw_session.add(instance)
        rw_session.commit()

        return {"status": "File uploaded successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")



if __name__ == "__main__":
    import uvicorn

    # Run the app using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)