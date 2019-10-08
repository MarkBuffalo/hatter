# About Hatter.

![Mad Hatter Picture](https://i.imgur.com/AjlFcy1.jpg)

This project is **Mad as a Hatter**! It's used for [Empires and Puzzles](https://www.smallgiantgames.com/empires-and-puzzles) game to gather raid data from screenshots. 

I have used this data to help reach #1 in the world several times in a row.

# Is this cheating?

- I don't believe  so. You're simply collecting data on what your top colors are so you can maximize your chances of winning through simple statistics. 
- To prove the point, I reached #1 globally multiple times with the least likely color combinations, meaning the deck was stacked against me the whole way. You still need to know how to play, how to counteract, and you absolutely need good heroes. 

# Installation:

```
git clone https://github.com/MarkBuffalo/hatter.git
cd hatter
pip3 install -r requirements.txt
mkdir shots
```

# Additional program requirements

- For this to work, you must put all pre-fight raid screenshots in the `/shots/` directory. 
- Pre-fight means you take a screenshot of the first screen after the raid starts, and before anyone fights. You must not move any tiles.
- You will need to build up thousands of screenshots to get any meaningful data.

An example full-sized anonymous screenshot is placed below:

![Empires and Puzzles: First-screen Raid Tiles](https://i.imgur.com/GYU1gxh.jpg)

Example `/shots/` directory structure:

```
$ pwd
/Users/derp/projects/hatter/shots
$ ls -la 
-rwxr-xr-x@  1 mad as  a hatter   9868724 Feb 09 22:26 IMG_1255.png
-rwxr-xr-x@  1 mad as  a hatter   9860067 Feb 09 22:26 IMG_1256.png
-rwxr-xr-x@  1 mad as  a hatter   9651928 Feb 09 22:26 IMG_1257.png
-rwxr-xr-x@  1 mad as  a hatter   9724532 Feb 09 22:26 IMG_1258.png
-rwxr-xr-x@  1 mad as  a hatter   9861563 Feb 09 22:26 IMG_1259.png
[...]
```

Once you have enough screenshots in the `/shots/` directory, you can run the python script:

```
python3 hatter.py
```

This will give you an output like so:

![Output](https://i.imgur.com/XpSB55u.png)

...which you're free to analyze using your own data science tomfoolery. Note that I'm aware the output is a dictionary. An earlier iteration of hatter used a list.

# Warning

- If you get anything other than `BLUE`, `PURPLE`, `RED`, `YELLOW`, `GREEN`, send me the values and I'll fix the program. 
