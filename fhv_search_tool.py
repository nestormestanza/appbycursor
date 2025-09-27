#!/usr/bin/env python3
"""
Interactive search tool for NYC FHV dataset
"""

import argparse
import sys
from fhv_data_analyzer import FHVDataAnalyzer
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Search NYC FHV dataset")
    parser.add_argument("--base-name", help="Search by base name (partial match)")
    parser.add_argument("--base-type", help="Filter by base type")
    parser.add_argument("--wheelchair", help="Filter by wheelchair accessibility status")
    parser.add_argument("--min-year", type=int, help="Minimum vehicle year")
    parser.add_argument("--max-year", type=int, help="Maximum vehicle year")
    parser.add_argument("--borough", help="Filter by borough (BROOKLYN, QUEENS, MANHATTAN, BRONX, STATEN ISLAND)")
    parser.add_argument("--limit", type=int, default=10, help="Limit results (default: 10)")
    parser.add_argument("--export", help="Export results to CSV file")
    parser.add_argument("--full-dataset", action="store_true", help="Use full dataset instead of cached sample")
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = FHVDataAnalyzer()
    
    # Load data
    if args.full_dataset:
        print("Loading full dataset... this may take a moment.")
        data = analyzer.download_data()
    else:
        print("Loading cached data...")
        try:
            data = analyzer.download_data(limit=5000)  # Use sample for faster searches
        except:
            print("No cached data found. Downloading sample...")
            data = analyzer.download_data(limit=5000)
    
    # Build search criteria
    search_criteria = {}
    
    if args.base_name:
        search_criteria['base_name'] = args.base_name
    
    if args.base_type:
        search_criteria['base_type'] = args.base_type
    
    if args.wheelchair:
        search_criteria['wheelchair_accessible'] = args.wheelchair
    
    # Apply search
    results = analyzer.search_vehicles(**search_criteria)
    
    # Apply additional filters
    if args.min_year and 'vehicle_year' in results.columns:
        results = results[results['vehicle_year'] >= args.min_year]
    
    if args.max_year and 'vehicle_year' in results.columns:
        results = results[results['vehicle_year'] <= args.max_year]
    
    if args.borough and 'base_address' in results.columns:
        results['borough'] = results['base_address'].str.extract(r'(BROOKLYN|QUEENS|MANHATTAN|BRONX|STATEN ISLAND|LIC)', expand=False)
        results['borough'] = results['borough'].replace({'LIC': 'QUEENS'})
        results = results[results['borough'].str.contains(args.borough, case=False, na=False)]
    
    # Display results
    print(f"\n=== SEARCH RESULTS ===")
    print(f"Found {len(results)} matching vehicles")
    
    if len(results) == 0:
        print("No vehicles match your search criteria.")
        return
    
    # Show limited results
    display_results = results.head(args.limit)
    
    # Select key columns for display
    display_columns = ['vehicle_license_number', 'name', 'base_name', 'base_type', 'vehicle_year', 'wheelchair_accessible']
    available_columns = [col for col in display_columns if col in display_results.columns]
    
    print(f"\nShowing first {len(display_results)} results:")
    print("-" * 80)
    
    for idx, row in display_results.iterrows():
        print(f"Vehicle License: {row.get('vehicle_license_number', 'N/A')}")
        print(f"Owner: {row.get('name', 'N/A')}")
        print(f"Base: {row.get('base_name', 'N/A')}")
        print(f"Type: {row.get('base_type', 'N/A')}")
        print(f"Year: {row.get('vehicle_year', 'N/A')}")
        print(f"Wheelchair Accessible: {row.get('wheelchair_accessible', 'N/A')}")
        if 'base_address' in row:
            print(f"Base Address: {row.get('base_address', 'N/A')}")
        print("-" * 40)
    
    # Export if requested
    if args.export:
        results.to_csv(args.export, index=False)
        print(f"\nResults exported to {args.export}")
    
    # Summary statistics
    if len(results) > 0:
        print(f"\n=== SUMMARY STATISTICS ===")
        if 'base_type' in results.columns:
            print("Base Types in results:")
            for base_type, count in results['base_type'].value_counts().items():
                print(f"  {base_type}: {count}")
        
        if 'vehicle_year' in results.columns:
            print(f"\nVehicle Years: {results['vehicle_year'].min()} - {results['vehicle_year'].max()}")
            print(f"Average Age: {2025 - results['vehicle_year'].mean():.1f} years")
        
        if 'wheelchair_accessible' in results.columns:
            accessible_count = results['wheelchair_accessible'].notna().sum()
            print(f"Vehicles with accessibility info: {accessible_count}")

if __name__ == "__main__":
    main()