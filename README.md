
# Games
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

its just a collection of different game files and their logo images, usefull for making cdn.jsdelivr.net links for your various gameloading jsons.


## Installation

Install the games into your workspace/repo using npx.

```npx
npx github:phant0m0567/games
cd games
```
or just use the cdn links to import the game code.
```
games: https://cdn.jsdelivr.net/gh/phant0m0567/games@main/${folder}/index.html
logos: https://cdn.jsdelivr.net/gh/phant0m0567/games@main/${folder}/index.png
```
Use the exact game folder name for `${folder}`, URL-encoding spaces and special
characters. For example, Geometry Dash is available at:
```
https://cdn.jsdelivr.net/gh/phant0m0567/games@main/Geometry%20Dash/index.html
https://cdn.jsdelivr.net/gh/phant0m0567/games@main/Geometry%20Dash/index.png
```
Duplicate game names use the ID in their folder name. The game list is at:
```
https://cdn.jsdelivr.net/gh/phant0m0567/games@main/zones.json
```

## Download assets from zones.json

Run the HTML and cover downloaders in separate virtual environments. Both scripts
read `zones.json` and write each matching asset to the game's `index.html` or
`index.png`. Duplicate game names get the ID appended to the folder name.

```bash
python3 -m venv .venv-html
source .venv-html/bin/activate
python download_html.py
deactivate

python3 -m venv .venv-covers
source .venv-covers/bin/activate
python -m pip install -r requirements-covers.txt
python download_covers.py
deactivate
```

## Authors

- [@phant0m0567](https://www.github.com/phant0m0567) - all i did was compile stuff
- [@J4Y](https://www.github.com/Chicken-Go-Crazy) -game ports hosted by him.
- [@genizy](https://www.github.com/genizy) -other game ports hosted by him.


