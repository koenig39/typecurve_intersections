import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
from tqdm import tqdm

class AssignToSiros:
    def __init__(self):
        self.snp_well_header = "static/input/well_header.csv"
        self.api10_siros_file = "static/input/api10_siros_formation_wb.csv"
        self.intersection_file = "static/output/intersection_results_20241210_125005.csv"
        self.geojson_file = "static/input/willistonGeo84_2024.geojson"
    
    def load_api10_full_list(self):
        try:
            columns_to_read = ["uwi", "basin", "target_formation"]
            
            # Force 'target_formation' to be a string when loading
            api10_full_df = pd.read_csv(self.snp_well_header, usecols=columns_to_read, dtype={'target_formation': str})
            
            # Filter rows where 'basin' equals "WILLISTON BASIN"
            api10_full_df = api10_full_df[api10_full_df['basin'] == "WILLISTON BASIN"]
            distinct_values = api10_full_df['target_formation'].unique()
            print(distinct_values)  
            return api10_full_df
        except Exception as e:
            raise RuntimeError(f"Error loading API10 Siros file: {e}")



    def load_api10_siros_data(self):
        try:
            api10_siros_df = pd.read_csv(self.api10_siros_file)
            return api10_siros_df
        except Exception as e:
            raise RuntimeError(f"Error loading API10 Siros file: {e}")

    def load_intersection_data(self):
        try:
            intersection_df = pd.read_csv(self.intersection_file)
            intersection_df['uwi'] = intersection_df['uwi'].astype(str).str[:10]  # Truncate UWI to 10 digits
            columns = ['uwi', 'pv_basin', 'formation_', 'tca_shortn', 'intersection_percentage']
            return intersection_df[columns]
        except Exception as e:
            raise RuntimeError(f"Error loading intersection results file: {e}")

    def calculate_surface_area(self):
        try:
            # Read the GeoJSON file into a GeoDataFrame
            gdf = gpd.read_file(self.geojson_file)
            
            # Calculate surface area and add it as a new column
            gdf['surface_area'] = gdf.geometry.apply(lambda geom: geom.area)
            
            # Standardize the column name
            gdf.rename(columns={'TCA_SHORTN': 'tca_shortn'}, inplace=True)
            
            # Create a dictionary with "tca_shortn" as keys and "surface_area" as values
            result = dict(zip(gdf['tca_shortn'], gdf['surface_area']))
            
            return result
        except Exception as e:
            # Raise an error with a descriptive message
            raise RuntimeError(f"Error processing GeoJSON file: {e}")


    def assign_tca_shortn(self, intersection_df, surface_area_dict):
        assigned_data = []

        for _, row in tqdm(intersection_df.iterrows(), total=len(intersection_df), desc="Assigning TCA_SHORTN", unit="intersection"):
            uwi = row['uwi']
            formation = row['formation_']

            # Add surface_area column by looking up tca_shortn in the surface_area_dict
            row['surface_area'] = row['tca_shortn'].map(surface_area_dict)

            # Select the row with the highest intersection percentage
            max_intersection = intersection_df.loc[intersection_df['intersection_percentage'].idxmax()]

            # If multiple rows have the highest intersection percentage, choose the one with the smallest area
            filtered_matches = intersection_df[intersection_df['intersection_percentage'] == max_intersection['intersection_percentage']]
            best_match = filtered_matches.loc[filtered_matches['surface_area'].idxmin()]

            assigned_data.append({
                'uwi': uwi,
                'formation': formation,
                'tca_shortn': best_match['tca_shortn']
            })

        return pd.DataFrame(assigned_data)



        return pd.DataFrame(assigned_data)

    def export_assigned_data(self, assigned_df):
        output_file = "static/output/assigned_tca_shortn.csv"
        try:
            assigned_df.to_csv(output_file, index=False)
            print(f"Assigned data exported to {output_file}")
        except Exception as e:
            raise RuntimeError(f"Error exporting assigned data: {e}")

    def process(self):
        surface_area_df = self.calculate_surface_area()
        api10_siros_df = self.load_api10_siros_data()
        intersection_df = self.load_intersection_data()
        assigned_df = self.assign_tca_shortn(intersection_df, surface_area_df)
        self.export_assigned_data(assigned_df)

# Execution example
if __name__ == "__main__":
    assigner = AssignToSiros()
    

    # res = assigner.load_intersection_data()
    # print(res)
    res2 = assigner.load_api10_full_list()
    print(res2)
