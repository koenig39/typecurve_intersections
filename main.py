import geopandas as gpd
import pandas as pd
from shapely.wkt import loads
from tqdm import tqdm

class WellboreDetails:
    def process_wellbore_intersections(self, csv_file, geojson_file):
        # Read the CSV file
        well_data = pd.read_csv(csv_file)

        # Filter data for the specified basin
        well_data = well_data[well_data['basin'] == "WILLISTON BASIN"]

        # Extract WKT boresticks, uwi, and basin
        well_data = well_data.dropna(subset=['borestick_3d'])
        wkt_boresticks = well_data[['uwi', 'borestick_3d', 'basin']].values.tolist()

        # Load GeoJSON file and calculate intersections
        results = self.calculate_borestick_intersection_percentage(wkt_boresticks, geojson_file)

        return results

    def calculate_borestick_intersection_percentage(self, wkt_boresticks, geojson_file):
        try:
            gdf = gpd.read_file(geojson_file)
        except Exception as e:
            raise RuntimeError(f"Error reading GeoJSON file: {e}")

        # Optionally filter the GeoDataFrame
        gdf_filtered = gdf[~gdf['TCA_SHORTN'].isin(['MB_NONEx', 'TF1_NONEx', 'TF2_NONEx'])]

        # Create spatial index
        gdf_filtered['bbox'] = gdf_filtered.geometry.apply(lambda x: x.bounds)
        spatial_index = gdf_filtered.sindex

        results = []

        for uwi, wkt, basin in tqdm(wkt_boresticks, desc="Processing wellbores", unit="wellbore"):
            try:
                # Load the WKT for a 3D LineString
                borestick = loads(wkt)
            except Exception as e:
                print(f"Invalid WKT: {wkt}. Error: {e}")
                continue

            bbox = borestick.bounds
            possible_matches_index = list(spatial_index.intersection(bbox))
            possible_matches = gdf_filtered.iloc[possible_matches_index]

            intersections = []
            for _, row in possible_matches.iterrows():
                percentage = self.calculate_intersection_percentage(borestick, row.geometry)
                if percentage > 0:
                    intersections.append((row['TCA_SHORTN'], row['FORMATION_'], percentage))

            if intersections:
                results.append({'uwi': uwi, 'basin': basin, 'intersections': intersections})

        return results

    def calculate_intersection_percentage(self, borestick, polygon):
        if polygon.intersects(borestick):
            intersected_line = borestick.intersection(polygon)
            intersected_length = intersected_line.length if not intersected_line.is_empty else 0
            total_length = borestick.length
            return (intersected_length / total_length * 100) if total_length > 0 else 0
        return 0

    def check_uwi(self, uwi, csv_file, geojson_file):
        well_data = pd.read_csv(csv_file)

        # Filter for the specific UWI
        specific_well = well_data[(well_data['uwi'] == uwi) & (well_data['basin'] == "WILLISTON BASIN")]

        if specific_well.empty:
            print(f"No data found for UWI: {uwi} in WILLISTON BASIN")
            return []

        wkt_boresticks = specific_well[['uwi', 'borestick_3d', 'basin']].values.tolist()

        # Load GeoJSON file and calculate intersections
        return self.calculate_borestick_intersection_percentage(wkt_boresticks, geojson_file)

if __name__ == "__main__":
    geojson_file = './static/input/willistonGeo84_2024.geojson'  # Replace with your GeoJSON file path
    csv_file = './static/input/well_header.csv'  # Replace with your CSV file path

    wellbore_details = WellboreDetails()
    results = wellbore_details.process_wellbore_intersections(csv_file, geojson_file)

    for result in results:
        print(f"UWI: {result['uwi']}, Basin: {result['basin']}")
        for intersection in result['intersections']:
            print(f"  Polygon: {intersection[0]}, Formation: {intersection[1]}, Percentage: {intersection[2]:.2f}%")

    # Example of checking a specific UWI
    # uwi_to_check = "1234567890"  # Replace with the UWI you want to check
    # specific_results = wellbore_details.check_uwi(uwi_to_check, csv_file, geojson_file)

    # if specific_results:
    #     print(f"Results for UWI: {uwi_to_check}")
    #     for result in specific_results:
    #         print(f"  UWI: {result['uwi']}, Basin: {result['basin']}")
    #         for intersection in result['intersections']:
    #             print(f"    Polygon: {intersection[0]}, Formation: {intersection[1]}, Percentage: {intersection[2]:.2f}%")
