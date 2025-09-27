#!/usr/bin/env python3
"""
NYC For-Hire Vehicles (FHV) Active Dataset Analyzer

This script provides tools to analyze the NYC TLC For-Hire Vehicles Active dataset.
Dataset ID: 8wbx-tsch
URL: https://data.cityofnewyork.us/Transportation/For-Hire-Vehicles-FHV-Active/8wbx-tsch

Features:
- Download and cache dataset
- Basic statistics and analysis
- Data visualization
- Search and filter capabilities
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import os
from typing import Dict, List, Optional
import argparse


class FHVDataAnalyzer:
    """Analyzer for NYC For-Hire Vehicles Active dataset."""
    
    def __init__(self, cache_file: str = "fhv_data.csv"):
        """Initialize the analyzer.
        
        Args:
            cache_file: Path to cache file for storing downloaded data
        """
        self.base_url = "https://data.cityofnewyork.us/resource/8wbx-tsch"
        self.cache_file = cache_file
        self.data: Optional[pd.DataFrame] = None
        
        # Set up plotting style
        plt.style.use('default')
        sns.set_palette("husl")
    
    def download_data(self, limit: Optional[int] = None, force_refresh: bool = False) -> pd.DataFrame:
        """Download FHV data from NYC Open Data API.
        
        Args:
            limit: Maximum number of records to download (None for all)
            force_refresh: Force refresh even if cache exists
            
        Returns:
            DataFrame containing the FHV data
        """
        if not force_refresh and os.path.exists(self.cache_file):
            print(f"Loading cached data from {self.cache_file}")
            self.data = pd.read_csv(self.cache_file)
            return self.data
        
        print("Downloading FHV data from NYC Open Data API...")
        
        # Build API URL
        url = f"{self.base_url}.json"
        params = {}
        if limit:
            params['$limit'] = limit
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise ValueError("No data received from API")
            
            self.data = pd.DataFrame(data)
            
            # Convert date columns
            date_columns = ['expiration_date', 'certification_date', 'hack_up_date', 'last_date_updated']
            for col in date_columns:
                if col in self.data.columns:
                    self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
            
            # Convert numeric columns
            if 'vehicle_year' in self.data.columns:
                self.data['vehicle_year'] = pd.to_numeric(self.data['vehicle_year'], errors='coerce')
            
            # Cache the data
            self.data.to_csv(self.cache_file, index=False)
            print(f"Data saved to {self.cache_file}")
            
            return self.data
            
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download data: {e}")
        except Exception as e:
            raise RuntimeError(f"Error processing data: {e}")
    
    def get_basic_stats(self) -> Dict:
        """Get basic statistics about the dataset.
        
        Returns:
            Dictionary containing basic statistics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call download_data() first.")
        
        stats = {
            'total_vehicles': len(self.data),
            'active_vehicles': len(self.data[self.data['active'] == 'YES']),
            'unique_bases': self.data['base_name'].nunique() if 'base_name' in self.data.columns else 0,
            'unique_owners': self.data['name'].nunique() if 'name' in self.data.columns else 0,
            'base_types': self.data['base_type'].value_counts().to_dict() if 'base_type' in self.data.columns else {},
            'vehicle_years_range': {
                'min': self.data['vehicle_year'].min() if 'vehicle_year' in self.data.columns else None,
                'max': self.data['vehicle_year'].max() if 'vehicle_year' in self.data.columns else None
            },
            'wheelchair_accessible': self.data['wheelchair_accessible'].value_counts().to_dict() if 'wheelchair_accessible' in self.data.columns else {},
            'last_updated': self.data['last_date_updated'].max() if 'last_date_updated' in self.data.columns else None
        }
        
        return stats
    
    def print_summary(self) -> None:
        """Print a summary of the dataset."""
        stats = self.get_basic_stats()
        
        print("\n" + "="*60)
        print("NYC FOR-HIRE VEHICLES (FHV) ACTIVE DATASET SUMMARY")
        print("="*60)
        print(f"Total Vehicles: {stats['total_vehicles']:,}")
        print(f"Active Vehicles: {stats['active_vehicles']:,}")
        print(f"Unique Bases: {stats['unique_bases']:,}")
        print(f"Unique Owners: {stats['unique_owners']:,}")
        print(f"Last Updated: {stats['last_updated']}")
        
        if stats['vehicle_years_range']['min'] and stats['vehicle_years_range']['max']:
            print(f"Vehicle Years: {int(stats['vehicle_years_range']['min'])} - {int(stats['vehicle_years_range']['max'])}")
        
        print("\nBase Types:")
        for base_type, count in stats['base_types'].items():
            print(f"  {base_type}: {count:,}")
        
        if stats['wheelchair_accessible']:
            print("\nWheelchair Accessible:")
            for status, count in stats['wheelchair_accessible'].items():
                print(f"  {status}: {count:,}")
        
        print("="*60)
    
    def analyze_base_types(self) -> None:
        """Analyze and visualize base types distribution."""
        if self.data is None:
            raise ValueError("No data loaded. Call download_data() first.")
        
        plt.figure(figsize=(12, 8))
        
        # Base types distribution
        plt.subplot(2, 2, 1)
        base_counts = self.data['base_type'].value_counts()
        plt.pie(base_counts.values, labels=base_counts.index, autopct='%1.1f%%')
        plt.title('Distribution of Base Types')
        
        # Vehicle years by base type
        plt.subplot(2, 2, 2)
        if 'vehicle_year' in self.data.columns:
            self.data.boxplot(column='vehicle_year', by='base_type', ax=plt.gca())
            plt.title('Vehicle Years by Base Type')
            plt.suptitle('')
        
        # Top 10 bases by vehicle count
        plt.subplot(2, 2, 3)
        top_bases = self.data['base_name'].value_counts().head(10)
        top_bases.plot(kind='barh')
        plt.title('Top 10 Bases by Vehicle Count')
        plt.xlabel('Number of Vehicles')
        
        # Wheelchair accessibility
        plt.subplot(2, 2, 4)
        if 'wheelchair_accessible' in self.data.columns:
            wheelchair_counts = self.data['wheelchair_accessible'].value_counts()
            wheelchair_counts.plot(kind='bar')
            plt.title('Wheelchair Accessibility')
            plt.xlabel('Accessibility Status')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def analyze_vehicle_age(self) -> None:
        """Analyze vehicle age distribution."""
        if self.data is None:
            raise ValueError("No data loaded. Call download_data() first.")
        
        if 'vehicle_year' not in self.data.columns:
            print("Vehicle year data not available")
            return
        
        current_year = datetime.now().year
        self.data['vehicle_age'] = current_year - self.data['vehicle_year']
        
        plt.figure(figsize=(15, 10))
        
        # Age distribution
        plt.subplot(2, 3, 1)
        self.data['vehicle_age'].hist(bins=30, edgecolor='black')
        plt.title('Vehicle Age Distribution')
        plt.xlabel('Vehicle Age (years)')
        plt.ylabel('Count')
        
        # Age by base type
        plt.subplot(2, 3, 2)
        base_types = self.data['base_type'].unique()
        for base_type in base_types:
            subset = self.data[self.data['base_type'] == base_type]
            plt.hist(subset['vehicle_age'], alpha=0.6, label=base_type, bins=20)
        plt.title('Vehicle Age by Base Type')
        plt.xlabel('Vehicle Age (years)')
        plt.ylabel('Count')
        plt.legend()
        
        # Vehicle year trends
        plt.subplot(2, 3, 3)
        year_counts = self.data['vehicle_year'].value_counts().sort_index()
        year_counts.plot(kind='line', marker='o')
        plt.title('Vehicles by Model Year')
        plt.xlabel('Vehicle Year')
        plt.ylabel('Count')
        
        # Average age by base type
        plt.subplot(2, 3, 4)
        avg_age = self.data.groupby('base_type')['vehicle_age'].mean().sort_values()
        avg_age.plot(kind='barh')
        plt.title('Average Vehicle Age by Base Type')
        plt.xlabel('Average Age (years)')
        
        # Age statistics
        plt.subplot(2, 3, 5)
        age_stats = self.data['vehicle_age'].describe()
        plt.text(0.1, 0.5, f"""
        Age Statistics:
        Mean: {age_stats['mean']:.1f} years
        Median: {age_stats['50%']:.1f} years
        Std Dev: {age_stats['std']:.1f} years
        Min: {age_stats['min']:.0f} years
        Max: {age_stats['max']:.0f} years
        """, transform=plt.gca().transAxes, fontsize=12,
        verticalalignment='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        plt.axis('off')
        plt.title('Age Statistics')
        
        plt.tight_layout()
        plt.show()
    
    def search_vehicles(self, **kwargs) -> pd.DataFrame:
        """Search for vehicles based on criteria.
        
        Args:
            **kwargs: Search criteria (e.g., base_name='UBER', vehicle_year=2020)
            
        Returns:
            Filtered DataFrame
        """
        if self.data is None:
            raise ValueError("No data loaded. Call download_data() first.")
        
        result = self.data.copy()
        
        for column, value in kwargs.items():
            if column in result.columns:
                if isinstance(value, str):
                    result = result[result[column].str.contains(value, case=False, na=False)]
                else:
                    result = result[result[column] == value]
        
        return result
    
    def export_analysis(self, filename: str = "fhv_analysis_report.txt") -> None:
        """Export analysis results to a text file.
        
        Args:
            filename: Output filename
        """
        stats = self.get_basic_stats()
        
        with open(filename, 'w') as f:
            f.write("NYC FOR-HIRE VEHICLES (FHV) ACTIVE DATASET ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("BASIC STATISTICS:\n")
            f.write(f"Total Vehicles: {stats['total_vehicles']:,}\n")
            f.write(f"Active Vehicles: {stats['active_vehicles']:,}\n")
            f.write(f"Unique Bases: {stats['unique_bases']:,}\n")
            f.write(f"Unique Owners: {stats['unique_owners']:,}\n")
            f.write(f"Last Updated: {stats['last_updated']}\n\n")
            
            f.write("BASE TYPES:\n")
            for base_type, count in stats['base_types'].items():
                f.write(f"  {base_type}: {count:,}\n")
            
            if stats['wheelchair_accessible']:
                f.write("\nWHEELCHAIR ACCESSIBILITY:\n")
                for status, count in stats['wheelchair_accessible'].items():
                    f.write(f"  {status}: {count:,}\n")
        
        print(f"Analysis report exported to {filename}")


def main():
    """Main function to run the analyzer."""
    parser = argparse.ArgumentParser(description="NYC FHV Data Analyzer")
    parser.add_argument("--limit", type=int, help="Limit number of records to download")
    parser.add_argument("--refresh", action="store_true", help="Force refresh cached data")
    parser.add_argument("--no-plots", action="store_true", help="Skip generating plots")
    parser.add_argument("--export", type=str, help="Export analysis to file")
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = FHVDataAnalyzer()
    
    try:
        # Download data
        analyzer.download_data(limit=args.limit, force_refresh=args.refresh)
        
        # Print summary
        analyzer.print_summary()
        
        # Generate plots if requested
        if not args.no_plots:
            print("\nGenerating analysis plots...")
            analyzer.analyze_base_types()
            analyzer.analyze_vehicle_age()
        
        # Export analysis if requested
        if args.export:
            analyzer.export_analysis(args.export)
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())