# pySteg

```
                     _____ __               
        ____  __  __/ ___// /____  ____ _   
       / __ \/ / / /\__ \/ __/ _ \/ __ `/   
      / /_/ / /_/ /___/ / /_/  __/ /_/ /    
     / .___/\__, //____/\__/\___/\__, /     
    /_/    /____/               /____/      
                                             
```

Embed/Extract data to/from images using LSB (Least Significant Bit) image steganography

## Installation

```
# Clone the project locally
git clone https://github.com/basedBaba/pySteg

# Create a virtual environment and install the required packages
cd pySteg
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make the script executable
chmod +x pysteg.py

./pysteg.py -h
```

## Usage

### Help

```
usage: pysteg.py [-h] [-s SECRET] command image

Embed/Extract data to/from images

positional arguments:
  command               embed/extract
  image                 image for embedding/extracting data to/from

options:
  -h, --help            show this help message and exit
  -s SECRET, --secret SECRET
                        secret text to be embedded
```

### Embedding

```
./pysteg.py embed [image] -s [secret]
```

### Extraction

```
./pysteg extract [image]
```