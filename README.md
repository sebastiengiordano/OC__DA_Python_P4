<p align="center">
    <a href="https://user.oc-static.com/upload/2020/09/22/16007793690358_chess%20club-01.png" class="oc-imageLink oc-imageLink--disabled"><img src="https://user.oc-static.com/upload/2020/09/22/16007793690358_chess%20club-01.png" alt="Logo"></a>
    <h1 align="center">Chess tournament</h1>
    <h2 align="center">(Swiss system)</h2>
    </br>
    <p align="left">
        This program aims to manage a chess tournament.
        You can :
<ul>
<li>Create a new tournament</li>
<li>Start or restart a tournament</li>
<li>Update the players ranking</li>
<li>Add player to your database</li>
<li>Generate lots of report (on players and tournaments)</li>
</ul>
    </p>
</p>

<br>
<br>

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

<br>
<br>

<!-- HOW RUN THIS PROGRAM -->
## How run this program

<br>

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

<br>

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

<br>

### Additional informations
In the terminal, you could see the home menu, which invit you to choose one of the following action:
* <a href="#Create-a-new-tournament">Create a new tournament</a>
* <a href="#Start-or-restart-a-tournament">Start or restart a tournament</a>
* <a href="#Update-the-players-ranking">Update the players ranking</a>
* <a href="#Add-player-to-your-database">Add player to your database</a>
* <a href="#Generate-lots-of-report">Generate reports</a>
* <a href="#Exit-application">Exit application</a>

<br>

<a name="Create-a-new-tournament"></a>
1. Create a new tournament:
<p align="justify">
  You can setup the tournament.
  During the setup, you can add new player to the database. But if the player is already in the database, when you enter its name, you can add directly a player of the list of players with the same name.
  Then you could see a tournament summary. And, if you not make mistake, you could validate the creation and so save this tournament in the database.
  Finally, you could start the tournament, go back to home menu or exit the application.
</p>

<br>

<a name="Start-or-restart-a-tournament"></a>
2. Start or restart a tournament:
<p align="justify">
  This option allow you to show filtered or sorted tournament.
  Then you can start one of them; or restart it if all rounds have'nt been played.
</p>

<br>

<a name="Update-the-players-ranking"></a>
3. Update the players ranking:
<p align="justify">
  This option allow you to show the list of player (sorted by ranking, name, age... or not).
  Then you can modified the ranking of one player.
</p>

<br>

<a name="Add-player-to-your-database"></a>
4. Add player to your database:
<p align="justify">
  Use this option to add a new player to the database.
  Note: during the tournament creation, you can also add new player in the database.
</p>

<br>

<a name="Generate-lots-of-report"></a>
5. Generate lots of report (on players and tournaments):
<p align="justify">
  By this way you can show:
<ul>
<li>All players sorted by name</li>
<li>All players sorted by ranking</li>
<li>All the tournament, select one of then and show:</li>
  <ul>
  <li>All players of this tournament sorted by name</li>
  <li>All players of this tournament sorted by ranking</li>
  <li>All the rounds of this tournament, the score of each player at the end of each round, and the final ranking</li>
  <li>All the matchs of this tournament with the number of point win by each player</li>
  </ul>
</ul>
</p>

<br>

<a name="Exit-application"></a>
6. Exit application:
<p align="justify">
  To stop the application programmatically
</p>

<br>
<br>

### Generate flak8 report
1. Open a terminal and go to the folder OC__DA_Python_P4 (if its not already the case):
```sh
cd "folder project path" & cd OC__DA_Python_P4
```
2. With the following command
```sh
py -m flake8 --format=html --htmldir=flake-report --exclude=.\ChessTournaments\env\
```
You will generate a flake8 report, which will be available in the following folder
```sh
"folder project path"\flake-report\index.html
```

<br>
<br>

<!-- FOLDER STRUCTURE -->
## Folder structure

From OC__DA_Python_P4\ChessTournaments folder, you will find the following folders:
* controllers
* models
* tools
* views
* env

<br>

### Folder controllers
In the folder controllers, you retreive all the controllers which aim to manage the application.

<br>

### Folder models
In the folder models, you have the subfolder "database" where the players and tournaments are saved.
There is also all objets link to tournamanent, player and menu which  aloow to manage them.

<br>

### Folder tools
In the folder tools, where is some boilerplate functions for this project.

<br>

### Folder views
In the folder views, you retreive the human machin interface.

<br>

### Folder env
This folder aim to manage the virtual environment where run this application.

<br>
