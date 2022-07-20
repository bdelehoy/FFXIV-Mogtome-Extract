# mogtome-extract
Parses a promotional web page for Final Fantasy XIV's recurring Moogle Tomestone Events to generate a CSV file of each item and its associated cost in event tomestones.

# Requirements
Python >= 3.9.7

# Usage
```
python mogtome-extract.py [-h] -u URL [-o OUTPUT_FILE] [-v]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to a 'mogmog-collection' page on the FFXIV Lodestone.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        CSV file in the script's directory to write results to. Will be created if it doesn't exist.
  -v, --verbose         If provided, prints out each tome reward to the console.
```

Example usage:

```
python mogtome-extract.py -u https://na.finalfantasyxiv.com/lodestone/special/mogmog-collection/202110/7pBwXOpUFp
```

Use of a virtual environment is highly recommended:
```
cd ffxiv-mogtome-extract

python -m venv .venv

./.venv/Scripts/activate.ps1    # Will be different depending on your dev platform; this is PowerShell on Windows

python -m pip install -r requirements.txt

# (you are now free to run/develop/debug/etc.)
python mogtome-extract.py {args ... }

deactivate
```
