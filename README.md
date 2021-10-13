# mogtome-extract
Parses a promotional web page for Final Fantasy XIV's recurring Moogle Tomestone Events to generate a CSV file of each item and its associated cost in tomestones.

# Requirements
Python 3.9.7, BeautifulSoup4

# Usage
Run in a command-line environment. First argument should be a URL to a Moogle Tomestone Event page. Second argument should be the name of a CSV file to write data to.

```
python mogtome-extract.py https://na.finalfantasyxiv.com/lodestone/special/mogmog-collection/202110/7pBwXOpUFp output.csv
```

Use of a virtual environment is highly recommended.

```
cd mogtome-extract

python -m venv .venv

./.venv/Scripts/activate.ps1    # Will be different depending on your dev platform; this is Powershell on Windows

pip install -r requirements.txt

# (you are now free to run/develop/debug/etc....)

deactivate
```
