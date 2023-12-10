
#uvicorn main:app --reload


from fastapi import FastAPI, UploadFile, File, HTTPException
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

# path_to_mailconverterprox = "C:\Program Files\CoolUtils\TotalMailConverterProX\MailConverterProX64.exe"
path_to_mailconverterprox = "C:\\Program Files\\CoolUtils\\TotalMailConverterProX\\MailConverterProX64.exe"
# path_to_mailconverterprox = Path("C:\\","Program Files","CoolUtils","TotalMailConverterProX","MailConverterProX64.exe")
# MailConverterProX64.exe "<source>" "<destination>" <options>

def run_command(input_file_path, output_file_path, additional_params):
    # Replace 'your_program' with the actual command line program and arguments
    command = [str(path_to_mailconverterprox), input_file_path, output_file_path] + additional_params

    try:
        print(path_to_mailconverterprox)
        print(str(" ".join(command)))

        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{' '.join(command)}' failed with error: {e}")
        raise RuntimeError(f"Command '{' '.join(command)}' failed with error: {e}")


@app.post("/convert_file/")
async def upload_file(file: UploadFile = File(...), additional_params: str = ""):
    try:
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}\\{file.filename}"

            # Save the uploaded file to the temporary directory
            with open(file_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)

            # Run the command-line program using the uploaded file and additional parameters
            output_file_path = f"{temp_dir}\\{file.filename}.pdf"
            logger.info(f"Received file: {file.filename}")

            run_command(file_path, output_file_path, additional_params.split())

            # Return the resulting file
            with open(output_file_path, "rb") as result_file:
                return {"result_file": result_file.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

