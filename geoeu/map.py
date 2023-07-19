#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def read_map(country: str, level: int = 0) -> gpd.GeoDataFrame():
    country_path = f"../geoeu/content/data/{country}"
    map_path = "/".join([
        country_path,
        f"adm{level}",
        f"{country.upper()}_ADM{level}.shp"])
    gdf: gpd.GeoDataFrame() = gpd.read_file(map_path)
    gdf.columns = map(str.lower, gdf.columns)
    gdf = gdf.rename(columns={"iso": "iso_code"})
    return gdf

def union_maps(*gdfs) -> gpd.GeoDataFrame():
    gdfs_out = pd.DataFrame()
    for gdf in gdfs:
        gdfs_out = pd.concat([gdfs_out, gdf])
    gdfs_out = gdfs_out.reset_index(drop=True)
    return gpd.GeoDataFrame(gdfs_out)


def read_countries() -> gpd.GeoDataFrame():
    eu_countries = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST",
                    "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA",
                    "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK",
                    "SVN", "ESP", "SWE"]
    eu_countries = [country.lower() for country in eu_countries]
    all_countries = read_map(eu_countries[0], level=0)
    for c in eu_countries:
        country = read_map(c, level=0)
        all_countries = union_maps(all_countries, country)
    return all_countries

def get_map_infos(country: str, level: int):
    gdf = read_map(country, level)
    n = gdf.shape[0]
    print(f"{n} entities of this type found in for this map of {country}.")
    print("Example:")
    print(gdf.head(1))
    print("Illustration:")
    gdf.plot()
    plt.show()
