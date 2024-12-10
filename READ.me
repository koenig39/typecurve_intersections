# Wellbore Intersections Processor

## Overview
This Python script calculates the percentage of intersection between wellbore trajectories (boresticks) and specified geological regions defined in a GeoJSON file. The results are exported as a CSV file for further analysis.

---

## Features
- Filters wellbore data by basin (e.g., "WILLISTON BASIN").
- Processes wellbore trajectories in WKT (Well-Known Text) format.
- Reads geological region definitions from a GeoJSON file.
- Calculates intersection percentages between wellbore trajectories and regions.
- Exports detailed results, including metadata, to a timestamped CSV file.

---

## Requirements

### Python Libraries:
- `geopandas`
- `pandas`
- `shapely`
- `tqdm`

Install dependencies using:
```bash
pip install geopandas pandas shapely tqdm
```

### Input Files:
1. **CSV File** (`static/input/well_header.csv`):
   - Contains wellbore data with columns:
     - `uwi`: Unique wellbore identifier.
     - `borestick_3d`: WKT representation of boresticks.
     - `basin`: Basin name (e.g., "WILLISTON BASIN").

2. **GeoJSON File** (`static/input/willistonGeo84_2024.geojson`):
   - Defines geological regions with properties including:
     - `UniqueId`
     - `TypeId`
     - `CustomClr`
     - `TCA_SHORTN`
     - `PV_BASIN`
     - `FORMATION_`
     - `TCA_NAME`
     - `IsPartial`

---

## How It Works
1. **Data Filtering**:
   - Filters wellbore data to include only rows with a specified basin and valid `borestick_3d` values.

2. **Geometry Processing**:
   - Converts WKT strings to Shapely geometries.
   - Reads GeoJSON and applies optional filtering to exclude irrelevant regions (e.g., `TCA_SHORTN` values like `MB_NONEx`).

3. **Intersection Calculation**:
   - Uses bounding boxes for initial filtering with spatial indexing.
   - Calculates the percentage of intersection between boresticks and polygons.

4. **Result Export**:
   - Exports results to a CSV file in `static/output` with column names in lowercase.

---

## Output
### CSV File
- Generated in the `static/output` directory with a filename pattern: `intersection_results_<timestamp>.csv`
- Columns:
  - `uwi`: Unique wellbore identifier.
  - `pv_basin`, `formation_`, `tca_shortn`: Geological metadata.
  - `intersection_percentage`: Percentage of intersection.
  - `basin`: Wellbore basin.
  - Additional GeoJSON properties.

---

## Example Usage
### Running the Script
Execute the script with:
```bash
python main.py
```

### Example Input
#### well_header.csv
| uwi         | borestick_3d     | basin           |
|-------------|------------------|-----------------|
| 123456789   | LINESTRING(...)  | WILLISTON BASIN |
| 987654321   | LINESTRING(...)  | OTHER BASIN     |

#### willistonGeo84_2024.geojson
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "UniqueId": 1,
        "TCA_SHORTN": "MB_MID_MCKENZIE",
        "PV_BASIN": "WB",
        "FORMATION_": "MB",
        "TCA_NAME": "MB_MID_MCKENZIE",
        "IsPartial": "N"
      },
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [...]
      }
    }
  ]
}
```

### Example Output
#### intersection_results_<timestamp>.csv
| uwi         | pv_basin | formation_ | tca_shortn       | intersection_percentage | basin           | uniqueid | typeid     |
|-------------|----------|------------|------------------|--------------------------|-----------------|----------|------------|
| 123456789   | WB       | MB         | MB_MID_MCKENZIE  | 65.23                   | WILLISTON BASIN | 1        | 144184204  |

---

## Notes
- Ensure input files are correctly formatted.
- Modify filtering logic in `calculate_borestick_intersection_percentage` if necessary.

---

## Contact
For questions or improvements, feel free to reach out to the development team.

