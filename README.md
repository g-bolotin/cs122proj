# Meow Mayhem

A 2D top-down shooter game where a cat throws yarn balls at fish enemies.

## Prerequisites
- **Python 3.7 or higher** 
- **Pip** (python package installer)
- **Git** (to clone the repository)

## Installation
### 1. Clone the Repository
Use the command prompt or another command line interface
```bash
git clone https://github.com/g-bolotin/cs122proj.git
````

### 2. Navigate to the Project Directory

```
cd cs122proj
```

### 3. Create Virtual Environment (Optional)
#### If `virtualenv` is not installed
```bash
pip install virtualenv
```

#### Create a virtual environment called `.venv`
```bash
python -m venv .venv
```

#### Activate the virtual environment
Windows
```bash
.venv\Scrits\activate
```
macOS/Linux
```bash
source .venv/bin/activate
```

### 4. Install Python Arcade
```bash
pip install -r requirements.txt
```

## Running the Game
While in the project root directory (cs122proj), run the command:
```bash
python -m src.main
```

## Controls
- **Movement**: WASD
  - Move the cat
- **Attack**: Space
  - Throw yarn balls at your enemies

## Gameplay
Defeat the fish monsters before losing all your lives!

## Acknowledgements
- **Python Arcade Library**: [Python Arcade](api.arcade.academy)
- **Aseprite**: [Sprite editor & pixel art tool](aseprite.org)
- **Contributors**: 
  - Galit Bolotin
  - Jeremy Chan