#!/usr/bin/env python3
"""
Quick statistics script for NYC FHV dataset
"""

import argparse
from fhv_data_analyzer import FHVDataAnalyzer
import pandas as pd
from datetime import datetime

def show_quick_stats():
    """Show quick statistics about the dataset."""
    analyzer = FHVDataAnalyzer()
    
    try:
        # Try to load cached data first
        data = analyzer.download_data(limit=None)
    except:
        print("Downloading sample data...")
        data = analyzer.download_data(limit=5000)
    
    stats = analyzer.get_basic_stats()
    
    print("🚗 NYC FOR-HIRE VEHICLES QUICK STATS")
    print("=" * 50)
    print(f"📊 Total Active Vehicles: {stats['total_vehicles']:,}")
    print(f"🏢 Unique Operating Bases: {stats['unique_bases']:,}")
    print(f"👥 Unique Vehicle Owners: {stats['unique_owners']:,}")
    print(f"📅 Last Updated: {stats['last_updated']}")
    
    if stats['vehicle_years_range']['min'] and stats['vehicle_years_range']['max']:
        print(f"🗓️  Vehicle Years: {int(stats['vehicle_years_range']['min'])} - {int(stats['vehicle_years_range']['max'])}")
    
    print("\n🚙 BASE TYPES:")
    for base_type, count in stats['base_types'].items():
        percentage = (count / stats['total_vehicles']) * 100
        print(f"   {base_type}: {count:,} ({percentage:.1f}%)")
    
    if stats['wheelchair_accessible']:
        print("\n♿ WHEELCHAIR ACCESSIBILITY:")
        total_with_info = sum(stats['wheelchair_accessible'].values())
        for status, count in stats['wheelchair_accessible'].items():
            percentage = (count / total_with_info) * 100
            print(f"   {status}: {count:,} ({percentage:.1f}%)")
    
    # Additional interesting stats
    if 'vehicle_year' in data.columns:
        current_year = datetime.now().year
        data['vehicle_age'] = current_year - data['vehicle_year']
        avg_age = data['vehicle_age'].mean()
        print(f"\n📈 Average Vehicle Age: {avg_age:.1f} years")
        
        # Fleet modernization stats
        new_vehicles = len(data[data['vehicle_year'] >= 2020])
        old_vehicles = len(data[data['vehicle_year'] < 2015])
        print(f"🆕 New Vehicles (2020+): {new_vehicles:,} ({(new_vehicles/len(data))*100:.1f}%)")
        print(f"🔧 Older Vehicles (<2015): {old_vehicles:,} ({(old_vehicles/len(data))*100:.1f}%)")
    
    # Top 5 largest fleets
    top_fleets = data['base_name'].value_counts().head(5)
    print(f"\n🏆 TOP 5 LARGEST FLEETS:")
    for i, (base, count) in enumerate(top_fleets.items(), 1):
        percentage = (count / len(data)) * 100
        base_short = base[:40] + "..." if len(base) > 40 else base
        print(f"   {i}. {base_short}: {count:,} ({percentage:.1f}%)")

def main():
    parser = argparse.ArgumentParser(description="Quick FHV dataset statistics")
    parser.add_argument("--detailed", action="store_true", help="Show detailed statistics")
    
    args = parser.parse_args()
    
    try:
        show_quick_stats()
        
        if args.detailed:
            print("\n" + "="*50)
            print("DETAILED ANALYSIS")
            print("="*50)
            analyzer = FHVDataAnalyzer()
            analyzer.print_summary()
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())