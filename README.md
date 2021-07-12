# Generate working Instagram/Twitter RSS links

## What it does
Finds the Instagram id of the user and inserts it to an rss-bridge url that works with RSS readers

For Twitter it checks if user exists and gives a nitter.net RSS url

## Usage

### Run script with:
  ```
  python main.py [-i | -t] [username]
  ```
  Omitting arguments returns Instagram by default
  
### Install dependencies with:
```
pip install -r requirements.txt
```

## Dependencies
```
beautifulsoup4==4.9.1
certifi==2020.6.20
chardet==3.0.4
clipboard==0.0.4
idna==2.10
pyperclip==1.8.0
requests==2.25.1
soupsieve==2.0.1
urllib3==1.26.6
```

## Configuration
To change from Atom type to Json or Html edit:
```
rssBridgeUrl = "...format=Atom"
```
