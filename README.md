# Plex-Automatic-Preroll
## Dev branch
This branch should be stable but you have been warned!

This new branch contains an almost fully rewritten code base. This now allows for Pre-rolls by Month, Week, Day, Misc, and Master list. The config is now based on yaml instead of a ini file for easier reading and data config data storage.

Thanks to [@agrider]( https://github.com/agrider ) for masterlist re-ordering and empty path error handling

## Requirements
-[Python 3.7+](https://www.python.org/)
(Probably works on a lower version haven't tested)

-[PlexAPI](https://github.com/pkkid/python-plexapi)



## Installation
First make sure you have Python installed version 3.7 and above. Next run:


```
pip install -r requirements.txt
```
That will install all the needed packages 

## Step by step instructions by Danny at smarthomepursuits.com

https://smarthomepursuits.com/configure-plex-automatic-prerolls-on-windows/

## Settings
The config.yaml file is created through the script for ease of use. Optionaly you can just create it by hand by filling in the exampleconfig.ini file and then renaming it to config.yaml. If you need to update it than you can edit the config.yaml file.

Below is an example of the config file:

```
---
global:
  file_types: ['.mp4', '.mkv']
  path: /my/path/to/videos  # The path that i have to the pre-roll videos

plex:
  url: https://url:32400
  token: asdasdasdasdasd
  path: /plex/path/to/videos  # The path plex uses to access the pre-roll videos

schedule:
  - name: Winter
    module:
      month: dec,jan,feb
    path: relative/path/to/videos  # CANNOT BEGIN WITH /
    mode: random
```


**If you want multiple random pre-roll videos to play in a specific month, week, or day all you need to do is seperate the paths with a semi-colon for the master list you need to specify random or not if allowing the script to make it automatically**
Example when it ask you to add the December trailer path and you want to play two videos randomly for that month type:

```
/path/to/file1.mp4;/path/to/file2.mp4
```
**Example config will be provided**

**The order of which it chooses the trailer list goes Misc, Daily, Weekly, Monthly, and then Master **

For example you could have your monthly list set up to play a specific set of pre-rolls for 3 months of the year leave the rest blank and those empty months will use the masterlist. While also set it using the Daily section to play a specific pre-roll on Dec 25th and then even have it so for 2 weeks during Dec it rotates through a set of pre-rolls defined in the Weekly pre-roll section.

## Usage

### Setting Plex Preroll

You need to schedule a job for updating the preroll each day, week, or month depending how you want your pre-rolls updated.

**macOS or Linux:**
Ex: Monthly

```
crontab -e
0 0 * 1-12 * python /path/to/scripts/Plex_Trailers.py 2>&1
```

**Windows:**

Verify python is added to the PATH environmental variable
Search for task schedular and open it. Click "Create Basic Task" and enter a name and description. Then set the task to run monthly. Choose "Start a program" then for "Program/script" add the full path of the Plex_Trailers.py script Click "Finish" and you are done!


## Running For The First Time

Since you just downloaded the script the first time you run if you don't already have a config file you will be prompted to fill in some information to create the config file.

```
python /path/to/scripts/Plex_Trailers.py
```

I hope this is useful for some people and feel free to modify it for your own use!
