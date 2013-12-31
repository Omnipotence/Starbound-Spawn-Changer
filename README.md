Starbound Spawn Changer
=======================

Command line application which is able to modify the spawn coordinates of a specific world file.

It is based on [the official documentation.](http://seancode.com/galileo/format/wrldb.html)

Make sure to ceate a **backup** of your world befure using this script. There are no guarantees it will not break your world.

Tested with version: **Angry Koala**


Usage
-----

Run `python main.py someworld.world` to print some information about the world.

Run `python main.py -x -1000 -y 1500 someworld.world` to set the spawn at location -1000,1500. It is possible to only modify X or Y.


Notes
-----

* I have not been able to determine the location of ingame objects, you will have find the desired spawn location through trial and error. 
* Some world files contain multiple world headers, this seems to be normal. The script will modify them all.
* It might break some worlds because the script works by searching for a specific byte pattern, there is a chance this byte pattern occurs randomly in a world file, which would lead to data corruption.