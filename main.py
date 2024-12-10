import geopandas as gpd
import pandas as pd
from shapely.wkt import loads
from tqdm import tqdm
from datetime import datetime
import os

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

        # Export results to CSV
        self.export_results_to_csv(results)

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

    def export_results_to_csv(self, results):
        output_data = []
        for result in results:
            uwi = result['uwi']
            basin = result['basin']
            for intersection in result['intersections']:
                output_data.append({
                    'uwi': uwi,
                    'basin': basin,
                    'formation': intersection[0],
                    'formation_name': intersection[1],
                    'intersection_percentage': intersection[2]
                })

        # Create output directory if it doesn't exist
        output_dir = 'static/output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'static/output/intersection_results_{timestamp}.csv'

        # Export to CSV
        pd.DataFrame(output_data).to_csv(filename, index=False)
        print(f"Results exported to {filename}")

# Execution example
if __name__ == "__main__":
    wellbore_processor = WellboreDetails()
    results = wellbore_processor.process_wellbore_intersections('static/input/well_header.csv', 'static/input/willistonGeo84_2024.geojson')
