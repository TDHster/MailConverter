# uvicorn main:app --reload


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

path_to_mailconverterprox = r'C:\Program Files\CoolUtils\TotalMailConverterProX\MailConverterProX64.exe'
path_to_mailconverterprox = path_to_mailconverterprox.replace(" ", "` ")


# path_to_mailconverterprox = '"C:\\Program Files\\CoolUtils\\TotalMailConverterProX\\MailConverterProX64.exe"'
# path_to_mailconverterprox = Path("C:\\","Program Files","CoolUtils","TotalMailConverterProX","MailConverterProX64.exe")
# MailConverterProX64.exe "<source>" "<destination>" <options>
# "C:\Program Files\CoolUtils\TotalMailConverterProX\MailConverterProX.exe"

# "C:\Program Files\CoolUtils\TotalMailConverterProX\MailConverterProX64.exe"
# "C:\Users\tdh\Downloads\На набережных Сочи щас ни-ко-го….eml" "C:\Users\tdh\Downloads\output.pdf" -c PDF

def run_command(input_file_path, output_file_path, additional_params):
    # Replace 'your_program' with the actual command line program and arguments
    # command = [str(path_to_mailconverterprox), f'"{input_file_path}"', f'"{output_file_path}"'] + additional_params
    command = [path_to_mailconverterprox, input_file_path.replace(" ", "` "),
               output_file_path.replace(" ", "` ")] + additional_params

    try:
        # 'C:\Users\tdh\Downloads\mail.eml'

        command = [r'C:\Program` Files\CoolUtils\TotalMailConverterProX\MailConverterProX64.exe']
                   # r'C:\Users\tdh\Downloads\mail.eml',
                   # r'C:\Users\tdh\Downloads\mail.eml.pdf',
                   # r'-c PDF']
        # print(path_to_mailconverterprox)
        print(str(" ".join(command)))

        # subprocess.run(command, encoding='cp1251')
        subprocess.run(command, check=True)
        # subprocess.call(command)
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
            print(f'{file_path=}')
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
            # with open(output_file_path, "rb") as result_file:
            #     return {"result_file": result_file.read()}
            return {"result_file": 'ы'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
