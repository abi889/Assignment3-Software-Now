# Spot the Difference — HIT137 Group Assignment 3

A desktop "Spot the Difference" game built with Python, Tkinter, and OpenCV.

---

## Team — SoftwareNow

| Name | Student ID |
|---|---|
| Diwan Paija | s396523 |
| Abichal Paudel | s404281 |
| Anuj Jung Karki | s403813 |
| Krishna Dev Bhatta | s405010 |

---

## Overview

Load any image and the app automatically generates a modified copy with five hidden differences for you to find.
Each round allows a maximum of 3 mistakes, and the goal is to spot all differences before losing your chances.

This project demonstrates image processing, GUI design, and object-oriented programming principles in an interactive way.

---

## Features

- Load any JPG, PNG, or BMP image from disk
- View original (left) and modified (right) images side by side
- Automatically generated 5 non-overlapping differences
- Red circle drawn on both images when a difference is correctly found
- Blue circles reveal all unfound differences via the Reveal button
- Maximum of 3 mistakes per image before the round ends
- Live display of remaining differences and mistakes used
- Win notification when all 5 differences are found

---

## Project Structure


```
Assignment3-SoftwareNow/
│
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
├── github_link.txt          # GitHub repository URL
│
└── game/
    ├── __init__.py
    ├── gui.py               # Tkinter GUI
    ├── controller.py        # Game logic and state management
    └── difference.py        # Image alteration strategies
```


---

## OOP Design

The codebase is organised into three core classes demonstrating encapsulation, inheritance, and polymorphism.

**DifferenceStrategy (Abstract Base Class)** — defines the interface for all image alteration strategies. Each subclass implements `apply(image, region)` and `get_name()`.

| Subclass | Alteration |
|---|---|
| ColorShiftStrategy | Boosts one RGB channel by a random amount |
| BlurStrategy | Applies Gaussian blur to the region |
| NoiseStrategy | Adds random pixel-level noise |
| BrightnessStrategy | Increases brightness across the region |
| ContrastStrategy | Scales pixel values to increase contrast |

**DifferenceGenerator** — selects 5 non-overlapping regions and applies randomly chosen strategies when an image loads.

**GameController** — manages all game state including images, differences found, mistakes, and win/loss conditions.

**SpotTheDifferenceApp** — builds the Tkinter interface and connects controller + generator.

---

## Requirements

- opencv-python
- numpy
- Pillow

---

## Installation

Clone the repository:

```bash
git clone https://github.com/abi889/Assignment3-Software-Now
cd Assignment3-Software-Now

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to Run

```bash
python main.py
```

---

## How to Play

1. Click **Load Image** and select a JPG, PNG, or BMP file.
2. The original image appears on the left; the modified image appears on the right.
3. Click on the right image where you think a difference is hidden.
   - Correct click — a red circle marks the difference on both images.
   - Wrong click — a mistake is recorded. You have 3 mistakes per round.
4. Find all 5 differences to win, or make 3 mistakes and the round ends.
5. Press **Reveal** to show all remaining differences in blue and end the round.
6. Load a new image to play again.

## Future Enhancements

- Add difficulty levels (Easy, Medium, Hard)
- Include a timer and leaderboard system
- Add sound effects or visual feedback when differences are found
- Option to load next image automatically after each round
- Save user progress and game statistics

## Technical Summary

- Uses **OpenCV** for image processing (blurring, brightness, contrast, and color shifting).
- **NumPy** supports efficient pixel-level operations.
- **Pillow (PIL)** helps handle image loading and conversions.
- **Tkinter** provides the GUI for displaying images and handling user clicks.
- The design follows **object-oriented principles**, separating logic, interface, and difference generation for modularity and clarity.


