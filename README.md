
# Rubiks Cube Architecture

This project is an object-oriented model of a Rubik's Cube architecture, implemented in Python. It provides users with the ability to generate a virtual Rubik's Cube and perform various operations on it, including rotations, inversions, and shifts. Additionally, the architecture offers functionality to shuffle and unshuffle the cube, allowing users to practice solving algorithms or explore cube states.


## Documentation

### models.py

This module contains the model definitions for the rubiks cube, its face, and a piece in the face. These definitions include defining the structure, as well as relevant properties and operations that exist for these models.

#### models.RubiksCube

This is a class representing the Rubiks Cube. A cube has 6 faces (type=Face). It is initialized with the blue face in front, red face on the left, orange face on the right, green face on the back, white face on top and yellow face on the bottom (referred to as 'default perspective').

##### Attributes
- current_front
- blue_face
- red_face
- orange_face
- green_face
- white_face
- yellow_face
- op_stack

##### Properties
- faces

##### Methods
- define_cube
- assign_complements
- rotate
- invert
- shift
- reset_perspective
- shuffle
- unshuffle

#### models.Face

This is a class representing a face of a rubiks cube (type=RubiksCube) as part of the rubiks cube architecture. Each face has a 3 X 3 grid, representing the 9 pieces (type=Piece |  EdgePiece | CornerPiece) present on a rubiks cube's face. The face instance's colour attribute is always set to be the colour of the face's center piece.

##### Attributes
- left
- right
- top
- bottom
- front
- back
- grid

##### Properties
- colour
- opposite
- is_copy

##### Methods
- copy
- initialize_grid
- update_grid_attrs
- init_face_complements
- print_attrs

#### models.Piece

This is a class that represents each piece on each face instance of a rubiks cube instance.

##### Attributes
- face
- face_position

##### Properties
- colour
- piece_type

#### models.EdgePiece

This is a class that represents an edge piece in the rubiks architecture. Inherits models.Piece.

##### Attributes
- face
- face_position

##### Properties
- colour
- piece_type
- complement

#### models.CornerPiece

This is a class that represents an corner piece in the rubiks architecture. Inherits from the Piece class.

##### Attributes
- face
- face_position

##### Properties
- colour
- piece_type
- complements

### transformations.py

This modules contains the definitions of transformations that are done on each face for each operation defined within the rubiks cube architecture.

#### transformations.RotateUp

This class contains transformation methods for the rotation up operation of a rubiks cube instance within the rubiks cube architecture.

#### transformations.RotateLeftVertical

This class contains transformation methods for the left vertical rotation operation of a rubiks cube instance within the rubiks cube architecture.

#### transformations.RightColUp

This class contains transformation methods for the shift right column up operation of a rubiks cube instance within the rubiks cube architecture.

#### transformations.LeftColUp

This class contains transformation methods for the shift left column up operation of a rubiks cube instance within the rubiks cube architecture.

#### transformations.TopRowLeft

This class contains transformation methods for the shift top row left operation of a rubiks cube instance within the rubiks cube architecture.

#### transformations.BottomRowLeft

This class contains transformation methods for the shift bottom row left operation of a rubiks cube instance within the rubiks cube architecture.

### operations.py

This module contains the definitions of operations that can be performed on the rubiks cube. These operations have been partitioned into rotations, inversions & shifts.

#### operations.Rotations

This class contains rotation operation methods for a rubiks cube instance within the rubiks cube architecture.

#### operations.Inversions

This class contains inversion operation methods for a rubiks cube instance within the rubiks cube architecture.

#### operations.Shifts

This class contains shift operation methods for a rubiks cube instance within the rubiks cube architecture.

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

