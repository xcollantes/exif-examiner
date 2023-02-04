# EXIF examiner

Quick command line script to show or delete image metadata.

## Getting started

1. Download repo: `git clone https://github.com/xcollantes/exif-examiner`
1. Navigate into repo: `cd exif-examiner`
1. Create local environment for dependencies: `python3 -m venv env`
1. Install dependencies:

   ```shell
   $ env/bin/pip install -r requirements.txt
   ```

## Usage

```shell
$ env/bin/python3 examine.py --target FILE_OR_DIRECTORY_PATH --action [show|device|remove]
```

Flags:

`--target` The file or directory path. Directories will be traversed
recursively and all image files only underneath the target will be targeted.

`--action` Operation to perform. Choose one of the following:

- `show` Show all exif metadata.
- `device` Show only device related exif metadata with Google Maps link for GPS
  coordinates.
- `remove` Clear all exif metadata.

## Example

### Show device related exif metadata for all images given a path

```shell
$ env/bin/python3 examine.py --target my/directory/path/ --action device
```

Result:

```
model: iPhone SE
make: Apple
datetime_original: 2021:03:03 17:26:18
datetime_digitized: 2021:03:03 17:26:18
gps_latitude: (57.0, 18.0, 4.6606)
gps_latitude_ref: N
gps_longitude_ref: W
gps_longitude: (4.0, 28.0, 9.2424)
/mnt/c/Users/xcollantes/Documents/exif-examiner/example.jpg
https://google.com/maps/place/57%C2%BA18%274.6606%22N+4%C2%BA28%279.2424%22W
```

### Clear all exif metadata for one image file

```shell
$ env/bin/python3 examine.py --target myimage.png --action remove
```

### Clear all exif metadata for one all image files given a path

```shell
$ env/bin/python3 examine.py --target my/directory/path/ --action remove
```
