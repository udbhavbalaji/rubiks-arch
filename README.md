
# Rubiks Cube Architecture

This project is an object-oriented model of a Rubik's Cube architecture, implemented in Python. It provides users with the ability to generate a virtual Rubik's Cube and perform various operations on it, including rotations, inversions, and shifts. Additionally, the architecture offers functionality to shuffle and unshuffle the cube, allowing users to practice solving algorithms or explore cube states.


## Documentation

[Documentation](https://linktodocumentation)
## Features

- The following operations are defined and can be performed on the rubiks cube:
    - **Rotations:** The cube can be rotated up & down, or left & right (horizontally & vertically)
    - **Inversions:** The cube can be inverted (horizontally & vertically)
    - **Shifts:** The left & right columns can be shifted up & down. Additionally, the top & bottom rows can be shifted left & right
- **Resetting Perspective:** Resets the cube perspective to defualt orientation, no matter the state of the cube.
- **Shuffle:** Performs a random number of operations (between 100 and 200) to get a completely shuffled cube. Optionally, user can supply an input to set the number of operations done.
- **Unshuffle:** Reverses all operations done on the rubiks cube since its creation.


## Screenshots

Since it's quite hard to make a simple visualization of a 3D cube, I've gone ahead and made a simple 2D representation. The following image shows the visual format of the cube representation.

![Cube Representation](https://i.imgur.com/diCm6fQ.png)

Following the instructions mentioned below launches the simple command line app to interact with the architecture. If you've done everything right, you should see something like this.

![Command Line App](https://i.imgur.com/4MtGxqV.png)


## Run Locally

Interacting with the rubiks cube could be helpful to explore the operations and definitions of the architecture. Instructions to clone and run the program can be seen below.

Clone the project

```zsh
  git clone https://github.com/udbhavbalaji/rubiks-arch.git
```

Go to the project directory

```zsh
  cd rubiks-arch
```

Install dependencies

```zsh
  pip install -r requirements.txt
```

Run the file run.py

```zsh
  python run.py
```

