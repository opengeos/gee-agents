from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple, Union

try:
    # Prefer real Strands decorator if available
    from strands import tool  # type: ignore
except Exception:  # pragma: no cover - fallback for environments without strands

    def tool(func):  # type: ignore
        return func


import ee  # type: ignore


BBox = List[float]  # [minx, miny, maxx, maxy]
GeoJSON = Dict[str, Any]


@tool
def ee_initialize() -> bool:
    """Initialize the Earth Engine API if not already initialized."""
    try:
        ee.Initialize()
        return True
    except Exception:
        # Attempt interactive auth if running in a notebook; callers may handle auth externally
        return False


def _to_ee_geometry(aoi: Union[BBox, GeoJSON]) -> ee.Geometry:
    if isinstance(aoi, (list, tuple)) and len(aoi) == 4:
        minx, miny, maxx, maxy = aoi
        return ee.Geometry.Rectangle([minx, miny, maxx, maxy])
    if isinstance(aoi, dict) and aoi.get("type") == "Polygon":
        return ee.Geometry.Polygon(aoi["coordinates"])  # type: ignore[arg-type]
    raise ValueError(
        "Unsupported AOI format. Provide bbox [minx,miny,maxx,maxy] or GeoJSON Polygon."
    )


@tool
def load_sentinel2(
    aoi: Union[BBox, GeoJSON],
    start_date: str,
    end_date: str,
    cloud_pct: int = 20,
) -> Dict[str, Any]:
    """Load and prefilter Sentinel-2 SR images for the AOI and date range.

    Returns a dict with the median image and count.
    """
    geom = _to_ee_geometry(aoi)
    col = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(geom)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
    )
    count = col.size()
    image = col.median().clip(geom)
    return {"image": image, "count": count}


@tool
def compute_ndwi(
    image: ee.Image, green_band: str = "B3", nir_band: str = "B8"
) -> ee.Image:
    """Compute NDWI = (G - NIR) / (G + NIR) for the provided image."""
    g = image.select(green_band)
    n = image.select(nir_band)
    ndwi = g.subtract(n).divide(g.add(n)).rename(["NDWI"]).clamp(-1, 1)
    return ndwi


@tool
def get_ndwi_tile_url(image: ee.Image, vis: Dict[str, Any] | None = None) -> str:
    """Return a public tile URL for visualizing the NDWI image."""
    vis = vis or {"min": -0.2, "max": 0.8, "palette": ["#0000FF", "#00FFFF", "#FFFFFF"]}
    try:
        m = image.getMapId(vis)
        return m["tile_fetcher"].url_format  # type: ignore[index]
    except Exception:
        # Fallback to raw visualization-less map id
        m = image.visualize(**vis).getMapId({})
        return m["tile_fetcher"].url_format  # type: ignore[index]
