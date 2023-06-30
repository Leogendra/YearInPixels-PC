# YearInPixels-writer

A script for writing pixels on your computer and importing the file back through your phone.

Special thanks to [pTinosq](https://github.com/pTinosq) for their Pixels reader!

## How to Use It
- Export your pixels from the [Pixel app](https://teovogel.me/pixels/)
- Place your *PIXELS-BACKUP-xxxxxx.json* file, which contains your backup, in this directory. There's no need to rename it.
- Launch the script using `python pixels.py`
- Select if you want to write or view a pixel.

Enjoy!

### Additional Features
- A warning will appear if you attempt to overwrite an existing pixel.
- There are checks in place if you misspell a date.
- You can customize your palette in the `get_color_of_mood` function (line 70).