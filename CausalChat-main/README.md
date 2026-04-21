# CausalChat2

# Causal Network – Setup Guide

This project generates an interactive causal network visualization using **PyVis**.

---

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

---

## Installation

Install the required dependency:

```bash
pip install pyvis
```

If you are using a virtual environment, activate it before installing.

---


## Running the Script

From the project directory, run:

```bash
python file_name.py
```

---

## Output

After running the script:

- An HTML file will be generated: example

```
adhd_persona1_causal network.html
```

- The file will automatically open in your default browser.
- If it does not open automatically, manually open the generated HTML file.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'pyvis'`

Run:

```bash
python -m pip install pyvis
```

### Browser does not open automatically

Open the generated `.html` file directly from your project folder.

---

No additional configuration is required.
