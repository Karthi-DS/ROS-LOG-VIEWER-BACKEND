from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        content_str = content.decode("utf-8")
        
        with open('db/db.log','a') as file:
            file.write("\n"+content_str)

        return JSONResponse(content={"status":"File Uploaded Successfully."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@router.delete("/deleteFile")
async def delete_file():
    try:
        with open('db/db.log','w') as file:
            file.write("")

        return JSONResponse(content={"status":"File deleted Successfully."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/getFile")
async def get_file_contents():
    try:
        content =  ""
        with open("db/db.log",'r') as file:
            content = file.read()
        parsed_data = []
        for line in content.splitlines():
            if line.strip(): 
                parts = line.split(" ",4)
                if len(parts) >= 4:
                    timestamp = parts[0].strip("[]") + " T " + parts[1].strip("[]")
                    severity = parts[2].strip("[]")
                    node = parts[3].strip("[]/")
                    message = parts[4]
                    parsed_data.append({
                        "timestamp": timestamp,
                        "severity": severity,
                        "node": node,
                        "message": message
                    })
        return JSONResponse(content={"data":parsed_data}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error":str(e)},status_code=500)