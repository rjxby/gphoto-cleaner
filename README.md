# File Finder and Copier with Exclusion, Unique Prefix, and Progress Bar

This script traverses a root folder and all subfolders to find files grouped by their extensions, excluding files that contain specified substrings in their names. It then copies the selected files to a destination folder, adding a unique prefix to each copied file. The script also displays a progress bar and logs the process.

## How to Run

To run the script with command-line arguments, including optional exclusion substrings, use:

```bash
python3 file_finder.py /path/to/source/folder /path/to/destination/folder --exclude substring1 substring2
```

### Use Case: Cleaning Up Google Photos Metadata and Copying Media Files to Synology Photos

#### Overview

When managing a large collection of media files in Google Photos, maintaining an organized structure can be challenging. This use case involves automating the cleanup of metadata and organizing media files into specific directories on a Synology NAS. This process ensures that files migrated from Google Photos to Synology are well-organized and easily accessible.

#### Example

For instance, if you have a folder of media files exported from Google Photos located at `/Users/username/GooglePhotos`, and you want to organize and copy them to a directory on your Synology NAS at `/volume1/photos/Organized`, you can run the script as follows:

```sh
python cleanup_google_photos.py /Users/username/GooglePhotos /volume1/photos/Organized --exclude temp backup
```
