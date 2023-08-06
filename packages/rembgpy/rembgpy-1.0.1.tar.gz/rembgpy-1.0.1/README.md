# rembgpy

- A simple python api wrapper for remove.bg.

## Installation

```
pip install rembgpy
```

## Usage

```python
from rembgpy import RemBg
import base64

api = RemBg("api-key", "logged-error.log")
with open("titty.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
print(api.remove_b64(encoded_string))
```

## Usage 2

```python
from rembgpy import RemBg

api = RemBg("api-key", "logged-error.log")
print(api.remove_img("https://sample.com/img_url.jpg"))
```