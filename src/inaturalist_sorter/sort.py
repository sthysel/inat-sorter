import shutil
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import click
from geopy.distance import geodesic
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def get_exif_data(
    image_path: Path,
) -> tuple[datetime | None, tuple[float, float] | None]:
    image = Image.open(image_path)
    exif_data = image._getexif()

    datetime_str: datetime | None = None
    gps: tuple[float, float] | None = None

    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTime":
                datetime_str = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
            if tag_name == "GPSInfo":
                gps_info = {GPSTAGS.get(t, t): value[t] for t in value}
                if gps_info:
                    latitude = gps_info.get("GPSLatitude", [0, 0, 0])
                    latitude = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
                    if gps_info.get("GPSLatitudeRef") == "S":
                        latitude = -latitude

                    longitude = gps_info.get("GPSLongitude", [0, 0, 0])
                    longitude = longitude[0] + longitude[1] / 60 + longitude[2] / 3600
                    if gps_info.get("GPSLongitudeRef") == "W":
                        longitude = -longitude

                    gps = (latitude, longitude)

    return datetime_str, gps


def cluster_images(
    image_data,
    time_threshold: int = 30,
    distance_threshold: int = 3,
):
    clusters = []
    for img, (timestamp, coordinates) in image_data.items():
        added = False
        for cluster in clusters:
            representative_img = list(cluster.keys())[0]
            rep_timestamp, rep_coordinates = cluster[representative_img]

            time_difference = abs((timestamp - rep_timestamp).total_seconds())
            distance_difference = (
                geodesic(coordinates, rep_coordinates).meters
                if coordinates and rep_coordinates
                else float("inf")
            )

            if (
                time_difference <= time_threshold
                and distance_difference <= distance_threshold
            ):
                cluster[img] = (timestamp, coordinates)
                added = True
                break

        if not added:
            clusters.append({img: (timestamp, coordinates)})

    return clusters


@click.command()
@click.option(
    "-i",
    "--source",
    default="./images",
    help="Source folder containing the images.",
)
@click.option(
    "-o",
    "--destination",
    default="./sorted_images",
    help="Destination folder to store sorted images.",
)
def cli(source: str, destination: str):
    source_folder = Path(source)
    destination_folder = Path(destination)

    destination_folder.mkdir(parents=True, exist_ok=True)

    image_files = [
        f
        for f in source_folder.iterdir()
        if f.suffix.lower() in [".png", ".jpg", ".jpeg"]
    ]

    image_data = {}
    for image_path in image_files:
        datetime_str, gps_info = get_exif_data(image_path)
        image_data[image_path] = (datetime_str, gps_info)

    clustered_images = cluster_images(image_data)

    for idx, cluster in enumerate(clustered_images):
        folder_path = destination_folder / f"Cluster_{idx+1}"
        folder_path.mkdir(parents=True, exist_ok=True)

        for image_path in cluster:
            destination_path = folder_path / image_path.name
            shutil.copy(str(image_path), str(destination_path))

    print("Images sorted.")


if __name__ == "__main__":
    cli()
