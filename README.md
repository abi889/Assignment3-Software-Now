# 🔍 Spot the Difference Game

## HIT137 Group Assignment 3

---

## 👥 Team Members

| Name | Student ID |
|------|-----------|
| Diwan Paija | s396523 |
| Abichal Paudel | s404281 |
| Anuj Jung Karki | s403813 |
| Krishna Dev Bhatta | s405010 |

---

## 🎮 About the Game

A desktop application where players find **5 differences** between two nearly identical images. Built with Python, Tkinter GUI, and OpenCV image processing.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📁 **Image Loading** | Supports JPG, PNG, BMP formats |
| 🎲 **Random Differences** | 5 differences at random locations each time |
| 🎨 **5 Alteration Types** | Color Shift, Blur, Noise, Brightness, Contrast |
| 🔴 **Visual Feedback** | Red circles on found differences |
| 📊 **Score Tracking** | Remaining differences & mistakes counter |
| ❌ **3 Mistakes Limit** | Game ends after 3 wrong clicks |
| 🔵 **Reveal Button** | Blue circles show all remaining differences |
| 🏆 **Win Condition** | Victory message when all 5 found |

---

## 🚀 How to Run

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Installation Steps

```bash
# 1. Clone or download the repository
git clone https://github.com/diwanpaijapun-coder/spot-the-difference-game.git
cd spot-the-difference-game

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
python3 main.py