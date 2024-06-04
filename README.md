# KranNet - Text Encoding Project
*Alberto Saponaro, Francesca Carlon*

## Description

### Phases
1. Collect
2. Prepare
3. Access

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

### Virtual Env

1. Install Virtual Env:
```
python3 -m venv .venv
```

2. Activate Virtual Env:
```
. .venv/bin/activate # for Linux, macOS
.venv\Scripts\activate # for Windows
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

