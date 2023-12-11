# uvicorn main:app --reload


from fastapi import FastAPI, UploadFile, File, HTTPException, Response
import shutil
import subprocess
import tempfile
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)
logger = logging.getLogger()

app = FastAPI()

# MailConverterProX64.exe "<source>" "<destination>" <options>
path_to_mailconverterprox = r'"C:\Program Files\CoolUtils\TotalMailConverterProX\MailConverterProX64.exe"'

source_path = r'"C:\Users\tdh\Downloads\На набережных Сочи щас ни-ко-го….eml"'
destination_path = r'"C:\Users\tdh\Downloads\На набережных Сочи щас ни-ко-го….eml.copy"'

def run_command(input_file_path, output_file_path, additional_params):

    command = f'{path_to_mailconverterprox} "{input_file_path}" "{output_file_path}" -c PDF'
    print(f'{command=}')
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error occured: {e}')
        logger.error(f"Command '{' '.join(command)}' failed with error: {e}")
        raise RuntimeError(f"Command '{' '.join(command)}' failed with error: {e}")

@app.post("/convert_file/")
async def upload_file(file: UploadFile = File(...), additional_params: str = ""):
    try:
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}\\{file.filename}"
            # print(f'{file_path=}')
            # Save the uploaded file to the temporary directory
            with open(file_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Run the command-line program using the uploaded file and additional parameters
            output_file_path = f"{temp_dir}\\{file.filename}.pdf"
            logger.info(f"Received file: {file.filename}")
            print(f'{file_path=}')
            print(f'{output_file_path=}')
            print(f'{additional_params.split()=}')

            run_command(file_path, output_file_path, additional_params.split())

            # Return the resulting file
            with open(output_file_path, "rb") as result_file:
                # return {"result_file": result_file.read()}
                # return Response(content=result_file.read(), media_type="application/octet-stream")
                # response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
                content = result_file.read()
                response = Response(content=content, media_type="application/octet-stream")
                # Set Content-Disposition header to specify the filename
                # response.headers["Content-Disposition"] = f"attachment; filename={file.filename}.pdf"
                returned_filename = 'converted.pdf'
                response.headers["Content-Disposition"] = f"attachment; filename={returned_filename}"

                return response

            # return {"result_file": 'ы'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
