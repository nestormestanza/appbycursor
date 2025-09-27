#!/usr/bin/env python3
"""
Demo script showing how to use the FHV Data Analyzer
"""

from fhv_data_analyzer import FHVDataAnalyzer
import pandas as pd
from datetime import datetime

def main():
    print("=== NYC FHV DATA ANALYSIS DEMO ===\n")
    
    # Initialize analyzer
    analyzer = FHVDataAnalyzer(cache_file="demo_fhv_data.csv")
    
    # Download sample data
    print("1. Downloading sample data...")
    data = analyzer.download_data(limit=2000)  # Sample of 2000 records
    
    # Show basic summary
    print("\n2. Basic Dataset Summary:")
    analyzer.print_summary()
    
    # Show data structure
    print("\n3. Dataset Structure:")
    print(f"Columns: {list(data.columns)}")
    print(f"\nData types:")
    print(data.dtypes)
    
    # Search examples
    print("\n4. Search Examples:")
    
    # Find wheelchair accessible vehicles
    wav_vehicles = analyzer.search_vehicles(wheelchair_accessible='WAV')
    print(f"Wheelchair Accessible Vehicles (WAV): {len(wav_vehicles)}")
    
    # Find vehicles by base type
    black_cars = analyzer.search_vehicles(base_type='BLACK-CAR')
    livery_cars = analyzer.search_vehicles(base_type='LIVERY')
    print(f"Black Cars: {len(black_cars)}")
    print(f"Livery Cars: {len(livery_cars)}")
    
    # Find newer vehicles
    if 'vehicle_year' in data.columns:
        new_vehicles = data[data['vehicle_year'] >= 2020]
        print(f"Vehicles 2020 or newer: {len(new_vehicles)}")
        
        # Calculate average age
        current_year = datetime.now().year
        data['vehicle_age'] = current_year - data['vehicle_year']
        avg_age = data['vehicle_age'].mean()
        print(f"Average vehicle age: {avg_age:.1f} years")
    
    # Show top bases
    print("\n5. Top 10 Largest Bases:")
    top_bases = data['base_name'].value_counts().head(10)
    for i, (base, count) in enumerate(top_bases.items(), 1):
        print(f"{i:2d}. {base[:50]}{'...' if len(base) > 50 else ''}: {count} vehicles")
    
    # Geographic distribution
    if 'base_address' in data.columns:
        print("\n6. Geographic Distribution:")
        data['borough'] = data['base_address'].str.extract(r'(BROOKLYN|QUEENS|MANHATTAN|BRONX|STATEN ISLAND|LIC)', expand=False)
        data['borough'] = data['borough'].replace({'LIC': 'QUEENS'})
        borough_counts = data['borough'].value_counts()
        for borough, count in borough_counts.items():
            if pd.notna(borough):
                percentage = (count / len(data)) * 100
                print(f"  {borough}: {count} vehicles ({percentage:.1f}%)")
    
    # Export analysis
    print("\n7. Exporting Analysis Report...")
    analyzer.export_analysis("demo_analysis_report.txt")
    
    print("\n=== DEMO COMPLETE ===")
    print("Files created:")
    print("- demo_fhv_data.csv (cached dataset)")
    print("- demo_analysis_report.txt (analysis report)")
    print("- fhv_data_analyzer.py (main analyzer class)")

if __name__ == "__main__":
    main()