import shutil
from collections import defaultdict
from pathlib import Path

import click
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def get_exif_data(
    image_path: Path,
) -> tuple[None | str, None | tuple[float, float, float]]:
    image = Image.open(image_path)
    exif_data = image._getexif()
    datetime_str = None
    gps_info = None

    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTime":
                datetime_str = value
            if tag_name == "GPSInfo":
                for t in value:
                    sub_tag_name = GPSTAGS.get(t, t)
                    if sub_tag_name == "GPSLatitude":
                        gps_info = value[t]

    return datetime_str, gps_info


def get_folder_name_from_datetime_and_gps(
    datetime_str: None | str, gps_info: None | tuple[float, float, float]
) -> str:
    if datetime_str is None:
        datetime_str = "Unknown"
    if gps_info is None:
        gps_str = "Unknown"
    else:
        gps_str = f"{gps_info[0]}_{gps_info[1]}_{gps_info[2]}"

    return datetime_str.replace(":", "-").replace(" ", "_") + "__" + gps_str


@click.command()
@click.option(
    "--source",
    default="./images",
    help="Source folder containing the images.",
)
@click.option(
    "--destination",
    default="./sorted_images",
    help="Destination folder to store sorted images.",
)
def cli(source: str, destination: str) -> None:
    source_folder = Path(source)
    destination_folder = Path(destination)

    destination_folder.mkdir(parents=True, exist_ok=True)

    image_files: list[Path] = [
        f
        for f in source_folder.iterdir()
        if f.suffix.lower() in [".png", ".jpg", ".jpeg"]
    ]

    folder_to_files = defaultdict(list)

    for image_path in image_files:
        datetime_str, gps_info = get_exif_data(image_path)
        folder_name = get_folder_name_from_datetime_and_gps(datetime_str, gps_info)
        folder_to_files[folder_name].append(image_path)

    for folder_name, files in folder_to_files.items():
        folder_path = destination_folder / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        for image_path in files:
            destination_path = folder_path / image_path.name
            shutil.move(str(image_path), str(destination_path))

    print("Images sorted.")


if __name__ == "__main__":
    cli()
