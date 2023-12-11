import shutil
import tempfile
from pathlib import Path
import subprocess

path_to_mailconverterprox = r'"C:\Program Files\CoolUtils\TotalMailConverterProX\MailConverterProX64.exe"'
                             # .replace(" ", "` "))
# path_to_mailconverterprox = 'copy'

source_path = r'"C:\Users\tdh\Downloads\На набережных Сочи щас ни-ко-го….eml"'
destination_path = r'"C:\Users\tdh\Downloads\На набережных Сочи щас ни-ко-го….eml.copy"'

try:
    # Construct the command as a string
    command = f'{path_to_mailconverterprox} {source_path} {destination_path} -c PDF'

    # Run the command using subprocess with shell=True
    subprocess.run(command, shell=True, check=True)

except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
