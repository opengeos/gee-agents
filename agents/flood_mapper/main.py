from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union

try:
    from strands import Agent  # type: ignore
except Exception:  # pragma: no cover - minimal fallback when strands is unavailable

    class Agent:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:
            pass


import ee  # type: ignore

from tools.gee_tools import (
    ee_initialize,
    load_sentinel2,
    compute_ndwi,
    get_ndwi_tile_url,
)


BBox = List[float]
GeoJSON = Dict[str, Any]


class FloodMapperAgent(Agent):
    """Strands-style agent that computes NDWI for a given AOI and date range."""

    def run(
        self,
        aoi: Union[BBox, GeoJSON],
        start_date: str,
        end_date: str,
        cloud_pct: int = 20,
        green_band: str = "B3",
        nir_band: str = "B8",
    ) -> Dict[str, Any]:
        if not ee_initialize():
            # If not initialized, try default ee.Initialize; this may require prior auth in notebooks
            try:
                ee.Initialize()
            except Exception as e:  # surface a helpful error to the caller
                raise RuntimeError(
                    "Earth Engine is not initialized. Run geemap.ee_initialize() or ee.Authenticate() first."
                ) from e

        data = load_sentinel2(
            aoi=aoi, start_date=start_date, end_date=end_date, cloud_pct=cloud_pct
        )
        image = data["image"]
        count = data["count"].getInfo()  # number of images used

        ndwi = compute_ndwi(image=image, green_band=green_band, nir_band=nir_band)
        tile_url = get_ndwi_tile_url(ndwi)

        # Compute simple stats over the AOI
        geom = _to_ee_geometry(aoi)
        stats = ndwi.reduceRegion(
            reducer=ee.Reducer.mean().combine(ee.Reducer.minMax(), None, True),
            geometry=geom,
            scale=30,
            maxPixels=1_000_000,
        ).getInfo()

        return {
            "images_used": count,
            "ndwi_tile_url": tile_url,
            "ndwi_stats": stats,
        }

    def run_demo(self) -> Dict[str, Any]:
        """Run a small demo over SF Bay bbox."""
        aoi = [-122.6, 37.6, -122.2, 37.9]
        return self.run(
            aoi=aoi, start_date="2023-01-01", end_date="2023-02-01", cloud_pct=20
        )


def _to_ee_geometry(aoi: Union[BBox, GeoJSON]) -> ee.Geometry:
    if isinstance(aoi, (list, tuple)) and len(aoi) == 4:
        minx, miny, maxx, maxy = aoi
        return ee.Geometry.Rectangle([minx, miny, maxx, maxy])
    if isinstance(aoi, dict) and aoi.get("type") == "Polygon":
        return ee.Geometry.Polygon(aoi["coordinates"])  # type: ignore[arg-type]
    raise ValueError(
        "Unsupported AOI format. Provide bbox [minx,miny,maxx,maxy] or GeoJSON Polygon."
    )
