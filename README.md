# YearInPixels-PC v1.3,3

A script for writing pixels on your computer and see statistics about your entries.
You can write a pixel for any day, see the average mood of a given note/tag, and even generate a statistic file with your most used words!

Special thanks to [pTinosq](https://github.com/pTinosq) for his Pixels reader!

## How to Use It
- Export your pixels from the [Pixel app](https://teovogel.me/pixels/)
- Place your *PIXELS-BACKUP-xxxxxx.json* file, which contains your backup, in this directory. There's no need to rename it.
- Launch the script using `python pixels.py`
- Select if you want to write/view a pixel, search or see statistics.

### Additional Features
- A warning will appear if you attempt to overwrite an existing pixel.
- You can customize your palette in the `get_color_of_mood()` function (in styles.py, line 30).
- Choose between multiple JSON files in the directory.
- Add excluded words that you don't want to show in statistics in the `excluded_words.txt` file.

#### Upcoming Features
- GUI