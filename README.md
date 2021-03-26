<p align="center">
    <br />
    <h1 align="center">Chess tournament</h1>
    <h2 align="center">(Swiss system)</h2>
    </br>
    <p align="left">
        This program aims to manage a chess tournament.
        You can :
* create a new tournament
* start or restart a tournament
* add player to your database
* Update the players ranking
* Generate lots of report (on players and tournaments)
    </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [How run this program](#how-run-this-program)
  * [Installation](#installation)
  * [Run the program](#run-the-program)
  * [Additional informations](#additional-informations)
  * [Generate flak8 report](#generate-flak8-report)
* [Folder structure](#folder-structure)
  * [Folder controllers](#folder-controllers)
  * [Folder models](#folder-models)
  * [Folder tools](#folder-tools)
  * [Folder views](#folder-views)


<!-- HOW RUN THIS PROGRAM -->
## How run this program

### Installation

1. Created a folder for this project. Then, open a terminal and go to this folder:
```sh
cd "folder project path"
```
2. Clone the repository:
```sh
git clone https://github.com/sebastiengiordano/OC__DA_Python_P4
```
3. Go to folder OC__DA_Python_P4:
```sh
cd OC__DA_Python_P4
```
4. Create a virtual environment:
```sh
python -m venv env
```
5. Activate the virtual environment :
```sh
.\env\Scripts\activate
```
6. From the "requirements.txt" file, install needed packets:
```sh
python -m pip install -r requirements.txt
```

### Run the program
1. Open a terminal and go to the folder OC__DA_Python_P4 (if its not already the case):
```sh
cd "folder project path" & cd OC__DA_Python_P4
```
2. Activate the virtual environment (if its not already the case):
```sh
.\env\Scripts\activate
```
3. Run the program
```sh
python -m ChessTournaments
```

### Additional informations
In the terminal, you could see the home menu which invit you to choose one of the following action:
* create a new tournament
* start or restart a tournament
* add player to your database
* Update the players ranking
* Generate reports

2. create a new tournament
3. start or restart a tournament
4. add player to your database
5. Update the players ranking
6. Generate lots of report (on players and tournaments)

### Generate flak8 report
1. Open a terminal and go to the folder OC__DA_Python_P4 (if its not already the case):
```sh
cd "folder project path" & cd OC__DA_Python_P4
```
2. With the following command
```sh
py -m flake8 --format=html --htmldir=flake-report --exclude=.\ChessTournaments\env\
```
You will generate a flake8 report which will be available with the following command
```sh
.\flake-report\index.html
```


<!-- FOLDER STRUCTURE -->
## Folder structure

From OC__DA_Python_P4\ChessTournaments folder, you will find the following folders:
* controllers
* models
* tools
* views

### Folder controllers
In the folder controllers, you retreive 

### Folder models

### Folder tools

### Folder views
