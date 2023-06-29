# YearInPixels-writer

A script for writing pixels on your computer, and import back the file through your phone

Thanks to [pTinosq](https://github.com/pTinosq) for it's Pixels reader !

## How to use it
- Export your pixels from the [Pixel app](https://teovogel.me/pixels/)
- place your *PIXELS-BACKUP-xxxxxx.json* file containing your backup in this directory, don't need to rename it.
- lauch the script using `python pixels.py`
- select if you want to write or view a pixel.

Enjoy!

### Additional features
- Warning if you try to overwrite an existing pixel
- Some checks if you misspelled a date
- You can customize your palette in the `get_color_of_mood` function (line 62)
