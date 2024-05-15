# Cam scanner

A college project in Python using OpenCV.<br>
Description: a simple app that takes an photo of a paper, and outputs an edited image with the paper properly aligned as though it was scanned.

<details>
  <summary><h3>Content</h3></summary>

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)

</details>
<hr>

# Dependencies

1. Python 3.7.0

The app could work with different versions, but this is the one that was tested.

# Installation

1. Create a new directory, for example `scanner`, and place `app.py` inside of it.
2. Open the directory in your Terminal:

```
cd scanner
```

3. Create a virtual environment:

```
python -m venv opencv-env
```

4. Activate the environment :

```
.\opencv-env\Scripts\activate
```

5. Install needed packages:

```
pip install opencv-contrib-python matplotlib
```

# Usage

1. Run the app using the following syntax:

```
python app.py path_input_img path_output_img
```

While:

- `path_input_img` - path to your scanned image.
- `path_output_img` - path to save the edited image, if none is provided it'll be displayed instead.
