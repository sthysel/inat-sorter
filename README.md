# iNaturalist Photo sorter (Version 0.1.0)


[Cyanicula sericea](https://inaturalist-open-data.s3.amazonaws.com/photos/316378631/original.jpg)

I will go for a walk and take a bunch of photos of interesting shit along the
way. Sometime after, I would download the previous few day's photos to a machine
to upload to iNaturalist, as Google Photos has fucked the API to iNaturalist, as
google does.

By this time the only cue to cluster photos together into observations would be
visual and manual time and position values. This tool attempts to remove that
manual burden by clustering a set of photos taken on a excursion into a set of
observations, each observation containing a set of photos of the subject sorted
by GPS proximity and a time window. This generally results in a generally
accurate approximation of a observation.

Recording a bunch of observations close together in time and space, with current
GPS accuracy on cellphones and contemporary GPS implementations ~5m at best,
will all result in less than stellar clustering. So keep that in mind while
recording. For me, at least, this is not usually a issue, and even when
clustering is not perfect, it does do 90%+ of the work for me.

# Usage

```sh
$ inat-sort --help
Usage: inat-sort [OPTIONS]

Options:
  -i, --source TEXT         Source folder containing the images.
  -o, --destination TEXT    Destination folder to store sorted images.
  --gps-threshold FLOAT     GPS accuracy threshold in radius meters
  --time-threshold INTEGER  Time window withing which a observation may
                            reasonably be done
  --help                    Show this message and exit.
```

Resulting in the flat input set to be sorted into

```sh
$ tree inat-out
inat-out/
├── cluster_1/
│   ├── 20230902_104910.jpg
│   ├── 20230902_104912.jpg
│   ├── 20230902_104917.jpg
│   ├── 20230902_104922.jpg
│   ├── 20230902_104927.jpg
│   └── 20230902_104931.jpg
├── cluster_10/
│   ├── 20230902_094123.jpg
│   ├── 20230902_094131.jpg
│   ├── 20230902_094135.jpg
│   └── 20230902_094146.jpg
├── cluster_11/
│   ├── 20230902_091553.jpg
│   ├── 20230902_091600.jpg
│   ├── 20230902_091605.jpg
│   └── 20230902_091610.jpg
├── cluster_12/
│   └── 20230902_105334.jpg
├── cluster_13/

```
