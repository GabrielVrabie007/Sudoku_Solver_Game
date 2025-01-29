# 🎮 Sudoku Solver: Where Logic Meets Fun! 🧩

> *"Life is like Sudoku - sometimes you need to take a step back to move forward!"* 🌟

## 📑 Table of Contents

- [✨ Overview](#overview)
- [🎯 Features](#features)
- [🔧 Installation](#installation)
- [🎪 Usage](#usage)
- [📊 Dataset](#dataset)
- [🤝 Contributing](#contributing)
- [📜 License](#license)


## ✨ Overview
Welcome to our magical **Sudoku Game**! 🎩✨ 

Get ready to embark on a brain-teasing adventure where productivity meets entertainment. Challenge yourself with:
- 🎲 Classic manual solving
- 🤖 Three powerful solving algorithms:
  - 🔄 Backtracking
  - 🧠 Constraint-Propagation
  - 📋 Rule-Based

*Remember: Every number you place is a step toward victory!* 🏆

## 🎯 Features

🎮 **Game Controls:**
- ⬆️⬇️ Select difficulty using arrow keys
- 🎲 Press "N" to generate a new puzzle
- 🖥️ Standard 9x9 grid in a sleek Pygame window
- 🤖 Choose between human wisdom or algorithmic brilliance

### 🖼️ Showcase

![solved_sudoku](https://github.com/user-attachments/assets/f0431d6d-b90a-4b36-8295-f6e66a23a74b)
*Victory has never looked so satisfying!* ✨

![difficulty](https://github.com/user-attachments/assets/a5ea398d-a986-4e0d-9a16-bdc050a3b8c6)
*Choose your challenge!* 💪

## 🔧 Installation

### 🌟 Method 1: Traditional Setup

```bash
# Clone the magical repository ✨
git clone "https://github.com/0DVD0/IAFPS_Sudoku.git"

# Create your mystical environment 🔮
python -m venv venv
venv\Scripts\activate

# Summon the dependencies 📦
poetry install
```

### 🐳 Method 2: Docker Magic

> *For those who prefer containerized adventures!*

#### Prerequisites:
- 🐋 Docker ([Install Here](https://docs.docker.com/desktop/setup/install/windows-install/))
- 🖥️ X Server ([Download VcXsrv](https://sourceforge.net/projects/vcxsrv/))

#### 🚀 Setup Steps:

1. 🖥️ **Launch XLaunch with:**
   - "Multiple windows"
   - Display number: -1
   - "Start no client"
   - ✅ "Disable access control"
   - ❌ Uncheck "Native opengl"

2. 🔮 **In administrator terminal:**
```bash
set DISPLAY=host.docker.internal:0.0
docker run -it --env="DISPLAY=host.docker.internal:0.0" --env="SDL_VIDEODRIVER=x11" --env="LIBGL_ALWAYS_INDIRECT=1" --env="PYTHONUNBUFFERED=1" gabriel385/sudoku_solver_v2:latest
```

## 🎪 Usage
For who have choosen to use poetry:
launch your adventure with: `python sudoku.py` 🚀

## 🤝 Contributing

Join our quest to make this game even better! 🌟

1. 🍴 Fork the repository
2. 🌿 Create your feature branch: `git checkout -b feature-name`
3. 💫 Commit your changes: `git commit -m 'Add some feature'`
4. 🚀 Push to the branch: `git push origin feature-name`
5. 🎯 Open a pull request

## 👨‍💻 The Dream Team

Meet the wizards behind the magic:

- 🧙‍♂️ Gabriel Vrabie - [GitHub](https://github.com/GabrielVrabie007)
- 🧙‍♂️ Istrati David - [GitHub](https://github.com/0DVD0)
- 🧙‍♂️ Ceaglei Daniil - [GitHub](https://github.com/danik169/danik169)
- 🧙‍♂️ Tuluc Paul - [GitHub](https://github.com/PaulT2004)

---




We hope this project brings joy to your coding journey! Whether you're a puzzle enthusiast or an algorithm aficionado, there's something here for everyone. Questions? Ideas? We'd love to hear from you! 🌈

*May your grid always be solvable!* 🍀