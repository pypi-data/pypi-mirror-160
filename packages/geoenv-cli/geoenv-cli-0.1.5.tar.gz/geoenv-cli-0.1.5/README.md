GeoEnv
------

GeoEnv is for those that don't want to create a geospatial development environment before you can test out some code you wrote, convert some spatial data or hack on an idea. The cli reduces the steps needed to spin up this working environment by using a docker image that already has a bunch of geospatial tools and libraries preloaded.


## Geospatial Working Environment

The docker environment uses [GeoEnv Docker image](https://github.com/gridcell/geoenv-docker) a preloaded ubuntu docker image that includes:

* gdal cli
* proj cli
* aws cli
* jupyter lab
* python packages: gdal, cartopy, numpy, rasterio, shapley, pystac, dask and [more](https://github.com/gridcell/geoenv-docker/blob/main/Dockerfile)


## Getting Started

`python -m "pip" install geoenv-cli`

OR

`python -m "pip" install --user geoenv-cli`


### Using GeoEnv

<img src="https://user-images.githubusercontent.com/915189/171786260-42fb5f9b-b83d-4284-88b7-36a8a97826c2.gif" width="100%"></img> 


## Contribute

If you find a bug or missing that library or application you always use, please file an issue or submit a pull request!