# NYC For-Hire Vehicles (FHV) Active Dataset Tools

This repository contains tools for analyzing the NYC TLC For-Hire Vehicles Active dataset from the NYC Open Data portal.

## Dataset Information

- **Source:** NYC Open Data Portal
- **Dataset ID:** 8wbx-tsch
- **URL:** https://data.cityofnewyork.us/Transportation/For-Hire-Vehicles-FHV-Active/8wbx-tsch
- **Records:** ~104,874 active vehicles (as of September 2025)
- **Update Frequency:** Daily (4-7 PM)
- **Description:** All TLC-licensed for-hire vehicles currently active and in good standing

## Files

### Core Analysis Tools
- `fhv_data_analyzer.py` - Main analyzer class with comprehensive data analysis capabilities
- `demo_analysis.py` - Demo script showing basic usage examples
- `requirements.txt` - Python package dependencies

### Data Files (Generated)
- `fhv_data.csv` - Cached full dataset
- `demo_fhv_data.csv` - Sample dataset for testing
- Various filtered CSV exports

### Analysis Outputs
- `*_analysis_report.txt` - Text-based analysis reports
- `wheelchair_accessible_vehicles.csv` - Filtered WAV vehicles
- `new_vehicles_2020_plus.csv` - Vehicles from 2020 and newer

## Quick Start

### Install Dependencies
```bash
# System packages (Ubuntu/Debian)
sudo apt update
sudo apt install -y python3-pandas python3-matplotlib python3-seaborn python3-requests python3-numpy

# Or using pip in a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run demo analysis
python3 demo_analysis.py

# Full analysis with visualizations
python3 fhv_data_analyzer.py

# Download specific number of records
python3 fhv_data_analyzer.py --limit 5000

# Force refresh cached data
python3 fhv_data_analyzer.py --refresh

# Skip plots (for headless environments)
python3 fhv_data_analyzer.py --no-plots

# Export analysis to custom file
python3 fhv_data_analyzer.py --export my_report.txt
```

### Python API Usage

```python
from fhv_data_analyzer import FHVDataAnalyzer

# Initialize analyzer
analyzer = FHVDataAnalyzer()

# Download data (cached automatically)
data = analyzer.download_data(limit=1000)  # or limit=None for full dataset

# Get basic statistics
stats = analyzer.get_basic_stats()
print(f"Total vehicles: {stats['total_vehicles']}")

# Print summary
analyzer.print_summary()

# Search for specific vehicles
uber_vehicles = analyzer.search_vehicles(base_name='UBER')
wav_vehicles = analyzer.search_vehicles(wheelchair_accessible='WAV')
new_vehicles = analyzer.search_vehicles(vehicle_year=2023)

# Generate visualizations
analyzer.analyze_base_types()
analyzer.analyze_vehicle_age()

# Export results
analyzer.export_analysis("my_analysis.txt")
```

## Dataset Fields

The dataset contains the following key fields:

- `vehicle_license_number` - Unique vehicle license number
- `name` - Owner/operator name
- `license_type` - Type of license (FOR HIRE VEHICLE)
- `expiration_date` - License expiration date
- `dmv_license_plate_number` - DMV license plate
- `vehicle_vin_number` - Vehicle identification number
- `vehicle_year` - Vehicle model year
- `base_number` - Base license number
- `base_name` - Operating base name
- `base_type` - Type of base (BLACK-CAR, LIVERY, etc.)
- `wheelchair_accessible` - Accessibility status (WAV, PILOT, etc.)
- `base_address` - Base operating address
- `last_date_updated` - Last update timestamp

## Analysis Features

### Basic Statistics
- Total vehicle count
- Active vehicle count
- Unique bases and owners
- Base type distribution
- Wheelchair accessibility stats
- Vehicle age analysis

### Search and Filtering
- Search by base name, type, year
- Filter by accessibility status
- Geographic filtering (by borough)
- License status filtering

### Visualizations
- Base type distribution (pie chart)
- Vehicle age distribution (histogram)
- Top bases by fleet size (bar chart)
- Geographic distribution (bar chart)
- License expiration timeline
- Fleet composition analysis

### Export Options
- CSV exports of filtered data
- Text-based analysis reports
- Multiple visualization formats

## Data Quality Notes

- Dataset is updated daily and maintained by NYC TLC
- Missing values are present in some optional fields
- Vehicle years range from 2004 to 2025
- Geographic information extracted from base addresses
- Wheelchair accessibility uses multiple status codes

## API Information

The dataset is accessible via the Socrata Open Data API (SODA):
- Base URL: `https://data.cityofnewyork.us/resource/8wbx-tsch.json`
- Supports filtering, sorting, and pagination
- No authentication required for basic access
- Rate limits apply for high-volume usage

## Contact

For dataset-related inquiries: licensinginquiries@tlc.nyc.gov