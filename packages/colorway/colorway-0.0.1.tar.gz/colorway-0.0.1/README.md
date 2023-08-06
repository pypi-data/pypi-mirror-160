# 🎨 Colorway

Python package to change the text color of the python console.  

## 📦 Installation

Run the following to install:  

```python
pip install colorway
```

## 🚀 Usage

### Foreground

```python
from colorway_foreground import *

# Generate red text with default background
print(red_fg("Hello, World!"))

# Generate bold red text with default background
print(bold_red_fg("Hello, World!"))

# Generate high-intensity red text with default background
print(highintensity_red_fg("Hello, World!"))

# Generate high-intensity bold red text with default background
print(highintensity_bold_red_fg("Hello, World!"))
```

### Background

```python
from colorway_background import *

# Generate text with red background
print(red_bg("Hello, World!"))

# Generate text with high-intensity red background
print(highintensity_red_bg("Hello, World!"))
```

### Available colors
The colors available to use are:  
- ⬛ Black
- 🟥 Red
- 🟩 Green
- 🟨 Yellow
- 🟦 Blue
- 🟪 Purple
- 🟦 Cyan
- ⬜ White

## 👨‍💻 Developing Colorway

To install colorway, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```

## 🚦 Development Progress

Unstable Development  
