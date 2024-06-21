# KranNet - Text Encoding Project
*Alberto Saponaro, Francesca Carlon*

## Description
The project focuses on text encoding and is based on the Carniolan Provincial Assembly corpus Kranjska 1.0. 

The corpus contains meeting proceedings of the Carniolan Provincial Assembly from 1861 to 1913, with a total of 694 sessions.

Its main goal is to encode XML into SQL and access the data for social network analysis.
The analysis of network interactions among the participants gives an overview of the social network within the meetings.


### Phases
1. Collect
    - The corpus is in XML format. 
    - A DOM parser is used to load the corpus. 
    - Creates the meeting ID.
    - Extract from Corpus:
        - Meetings titles
        - Years
        - Speakers name
        - Number of speakers’ interventions
    - Makes cache after collect phase

2. Prepare
    - Creates SQL database
    - Creates tables
        - Meeting table (title and year)
        - Speaker table (name and number of interventions)
    - Populate the tables 

3. Access
    - SQL query to access data needed for the network analysis 

*we used Notebooks for test porpuses, take a look at them ;)

## Download datasets

### Carniolan Provincial Assembly corpus Kranjska 1.0:

1. **Download** `Kranjaska-xml.zip` in the `/datasets` folder.

    url: https://www.clarin.si/repository/xmlui/handle/11356/1824

    CMD: 
    ```
    cd datasets

    curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1824{/Kranjska-xml.zip}

    ```

2. unzip `Kranjaska-xml.zip` in the `/datasets` folder.


## Setup

### PostgresSQL
 - version: 16.3


### Virtual Env

1. Install Virtual Env:
```
python3 -m venv .venv
```

2. Activate Virtual Env:
```
# For Linux and MacOS
. .venv/bin/activate 

# For Windows
.venv\Scripts\activate 
```

3. Install dependencies:
```
pip install -r requirements.txt
```


___

- Deactivate Virtual Env:
```
deactivate
```

## How To Run

**!!!Before running the code!!!** Make sure the database is online.

The project is divided in three parts. To run them individually execute:

1. Collect:
    ```
    # For Linux and MacOS
    bash collect.sh

    # Windows
    cmd.exe /c collect.bat

    ```
2. Prepare:
    ```
    # For Linux and MacOS
    bash prepare.sh

    # For Windows
    cmd.exe /c prepare.bat

    ```
3. Access:
    ```
    # Mac/Linux
    bash access.sh
    
    # For Windows
    cmd.exe /c access.bat
    
    ````

To run the whole pipeline:
```
# Mac/Linux
bash run.sh

# Windows
cmd.exe /c run.bat

```

