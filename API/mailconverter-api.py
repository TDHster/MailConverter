# uvicorn API.mailconverter-api:app --reload
# uvicorn API.mailconverter-api:app --host 0.0.0.0 --port 8000

from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from urllib.parse import quote

import shutil
import subprocess
import tempfile
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    # filename='app.log',
    # filemode='a'
)
logger = logging.getLogger()

app = FastAPI()

# MailConverterProX64.exe "<source>" "<destination>" <options>
# path_to_mailconverter = r'"C:\Program Files\CoolUtils\TotalMailConverterProX\MailConverterProX64.exe"'
path_to_mailconverter = Path("MailConverter/15-MailConverterX.32.exe")
source_path = r'"C:\Users\tdh\Downloads\На набережных Сочи щас ни-ко-го….eml"'
destination_path = r'"C:\Users\tdh\Downloads\На набережных Сочи щас ни-ко-го….eml.pdf"'
wine_path = 'wine'
def run_command(input_file_path: str, output_file_path: str, additional_params=''):

    # command = f'{wine_path} {path_to_mailconverter} "{input_file_path}" "{output_file_path}" -c PDF'
    command = [str(wine_path), str(path_to_mailconverter), str(input_file_path), str(output_file_path), additional_params]
    print(f'{command=}')
    try:
        subprocess.run(command, check=True)
        # subprocess.run(command)
    except subprocess.CalledProcessError as e:
        print(f'Error occured: {e}')
        logger.error(f"Command '{' '.join(command)}' failed with error: {e}")
        raise RuntimeError(f"Command '{' '.join(command)}' failed with error: {e}")

@app.post("/convert_file/")
async def convert_file_api(file: UploadFile = File(...), additional_params: str = ''):
    output_file_extension = '.pdf'
    try:
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            # file_path = f"{temp_dir}\\{file.filename}"
            file_path = Path(temp_dir, file.filename)
            # print(f'{file_path=}')
            # Save the uploaded file to the temporary directory
            with open(file_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Run the command-line program using the uploaded file and additional parameters
            output_filename = f'{file_path.stem}{output_file_extension}'
            output_file_path = Path(temp_dir, output_filename)
            logger.info(f"Received file: {file.filename}")
            print(f'{file_path=}')
            print(f'{output_file_path=}')
            print(f'{additional_params.split()=}')

            run_command(str(file_path), str(output_file_path))

            # Return the resulting file
            with open(output_file_path, "rb") as result_file:
                content = result_file.read()
                response = Response(content=content, media_type="application/octet-stream")
                # returned_filename = 'converted.pdf'
                encoded_filename = quote(output_filename.encode('utf-8'))

                response.headers["Content-Disposition"] = f"attachment; filename={encoded_filename}"

                return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process convert file: {str(e)}")
