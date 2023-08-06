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

# Generate custom colored text (red: 150, green: 78, blue: 120) with default background
print(custom_fg(150,78,120,"Hello, World!"))
```

### Background

```python
from colorway_background import *

# Generate text with red background
print(red_bg("Hello, World!"))

# Generate text with high-intensity red background
print(highintensity_red_bg("Hello, World!"))

# Generate text with custom colored background (red: 150, green: 78, blue: 120)
print(custom_bg(150,78,120,"Hello, World!"))
```

### Foreground & Background

You can use foreground formatting and background formatting by placing them in each other.  

```python
from colorway_foreground import *
from colorway_background import *

# Generate red text with blue background
print(red_fg(blue_bg("Hello, World!")))
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

Stable Development 
