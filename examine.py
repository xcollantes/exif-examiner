"""Scrub photos of metadata."""

import imghdr
import os
import logging
import urllib.parse

from absl import app, flags, logging
from exif import Image

logging.get_absl_handler().setFormatter(None)

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "target", "", "Target of photo or photos to scrub. If directory, all " +
    "contents will be recusively traversed and scrubbed.")
flags.DEFINE_string(
    "action", "show", "What to do with exif data in each photo. " +
    "Options are `show` for show exif data, `device` for device data, `remove` for cleaning of exif data.")


def main(_):
    """Determine if target is file or directory."""
    absolute_path: str = os.path.abspath(FLAGS.target)
    if not os.path.exists(absolute_path):
        logging.error("%s does not exist")

    if os.path.isdir(absolute_path):
        for dirpath, _, filenames in os.walk(absolute_path, topdown=True):
            for file in filenames:
                action_file(os.path.join(dirpath, file), FLAGS.action)
    else:
        action_file(absolute_path, FLAGS.action)


def action_file(path: str, selection: str) -> None:
    """Perform action depending on user."""
    if imghdr.what(path):
        selection: str = selection.strip().upper()
        if selection == "DEVICE":
            get_device(path)
        elif selection == "REMOVE":
            remove_metadata(path)
        else:
            show(path)
    else:
        logging.warning("Skipping non-image: %s", path)

    logging.info("")


def remove_metadata(path: str) -> None:
    """Clean the image file of metadata."""
    logging.info("Removing metadata for %s", path)
    with open(path, "rb") as image_file:
        img: Image = Image(image_file)

    logging.info("Found metadata for %s: %s",
                 os.path.basename(path), img.list_all())

    img.delete_all()
    logging.info("Removed exif data from %s", os.path.basename(path))

    with open(path, "wb") as write_file:
        write_file.write(img.get_file())


def get_device(path: str) -> None:
    """Show metadata fields for device related."""
    device_fields: list[str] = ["make", "model", "lens_make", "lens_model",
                                "datetime_original", "datetime_digitized",
                                "offset_time", "gps_longitude",
                                "gps_longitude_ref", "gps_latitude", "gps_latitude_ref"]
    with open(path, "rb") as image_file:
        img: Image = Image(image_file)
        meta: list[str] = img.list_all()

    for field in meta:
        if field in device_fields:
            logging.info("%s: %s", field, img.get(field))

    logging.info(path)
    logging.info(format_geo_link(img.get("gps_longitude"), img.get(
        "gps_longitude_ref"), img.get("gps_latitude"), img.get("gps_latitude_ref")))


def show(path: str) -> None:
    """Print out to terminal the metadata."""
    with open(path, "rb") as image_file:
        img: Image = Image(image_file)

    logging.info("%s", os.path.basename(path))
    for data in img.list_all():
        logging.info("%s: %s", data, img.get(data))


def format_geo_link(long: tuple[float, float, float], long_ref: str,
                    lat: tuple[float, float, float], lat_ref: str) -> str:
    """Returns a map link to open in browser for image location."""
    if not (long or long_ref or lat or lat_ref):
        return "Could not find GPS data."
    else:
        maps: str = "https://google.com/maps/place/"
        link = f"{long[0]:.0f}º{long[1]:.0f}'{long[2]}\"{long_ref} {lat[0]:.0f}º{lat[1]:.0f}'{lat[2]}\"{lat_ref}"
        return f"{maps}{urllib.parse.quote_plus(link)}"


if __name__ == "__main__":
    app.run(main)
