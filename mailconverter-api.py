#!/.venv/bin/python

# uvicorn API.mailconverter-api:app --reload
# uvicorn API.mailconverter-api:app --host 0.0.0.0 --port 8000

from uvicorn import run
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from urllib.parse import quote

import shutil
import subprocess
import tempfile
from pathlib import Path
import logging
import os

# Configure logging to print debug messages to the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = FastAPI()

# MailConverterProX64.exe "<source>" "<destination>" <options>
path_to_mailconverter = str(Path("MailConverter/15-MailConverterX.32.exe"))
wine_path = 'wine'
current_directory = os.getcwd()
temporary_dir = Path(current_directory, 'temp')    
output_file_extension = '.pdf'

def run_command(input_file_path: str, output_file_path: str, additional_params=''):

    # subprocess.run('pwd')
    command = [wine_path, path_to_mailconverter, input_file_path, output_file_path]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error occured: {e}')
        logger.error(f"Command '{' '.join(command)}' failed with error: {e}")
        raise RuntimeError(f"Command '{' '.join(command)}' failed with error: {e}")


@app.post("/convert_file/")
async def convert_file_api(file: UploadFile = File(...), additional_params: str = ''):
    # logger.info(f"Entering convert_file_api function")
    try:
        with tempfile.TemporaryDirectory(dir=temporary_dir) as temp_dir:
            # logger.info(f"temp_dir: {temp_dir=}")
            file_path = Path(temp_dir, file.filename)
            # print(f'{file_path=}')
            with open(file_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)
            # print(f'\t{temp_file=}')
            # logger.info(f"Saved file: {file_path=}")
            output_filename = f'{file_path.stem}{output_file_extension}'
            output_file_path = Path(temp_dir, output_filename)
            logger.info(f"Received file: {file.filename}")

            relative_file_path = file_path.relative_to(current_directory)
            relative_output_file_path = output_file_path.relative_to(current_directory)

            run_command(str(relative_file_path), str(relative_output_file_path))

            # Return the resulting file
            with open(output_file_path, "rb") as result_file:
                content = result_file.read()
                response = Response(content=content, media_type="application/octet-stream")
                encoded_filename = quote(output_filename.encode('utf-8'))
                response.headers["Content-Disposition"] = f"attachment; filename={encoded_filename}"
                return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert file: {str(e)}")


if __name__ == "__main__":
    run("mailconverter-api:app", host="0.0.0.0", port=8000, log_level="debug")