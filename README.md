# 🥗 NutriScrape

**An intelligent web scraping system that extracts, processes, and structures nutritional information from online food databases for diet analysis and meal planning.**

NutriScrape automates the collection of comprehensive food nutrition data, transforming raw web content into clean, analyzable datasets for health-conscious individuals and developers building diet-related applications.

---

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![BeautifulSoup](https://img.shields.io/badge/Web_Scraping-BeautifulSoup-4B8BBE?style=for-the-badge&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)
[![Data Analysis](https://img.shields.io/badge/Data_Analysis-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

---

## 📖 Quick Navigation

- [What is NutriScrape?](#-what-is-nutriscrape)
- [Core Capabilities](#-core-capabilities)
- [Technology Stack](#-technology-stack)
- [Project Blueprint](#-project-blueprint)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Configuration](#configuration)
- [System Workflow](#-system-workflow)
- [Data Pipeline](#-data-pipeline)
- [Applications](#-applications)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License & Author](#-license--author)

---

## 🎯 What is NutriScrape?

NutriScrape is a Python-powered **web scraping framework** designed to systematically extract nutritional information from online food databases. It bridges the gap between raw web data and structured nutritional insights, making it an ideal foundation for:

- 🥑 Personalized diet tracking systems
- 📊 Nutritional research and analysis
- 🤖 Machine learning training datasets
- 📱 Health and fitness mobile applications

---

## ⚡ Core Capabilities

### Data Extraction Engine
- **Multi-source scraping**: Extract data from multiple food databases simultaneously
- **Dynamic content handling**: Support for both static HTML and JavaScript-rendered content
- **Intelligent parsing**: Smart extraction of nutritional values with unit detection
- **Error resilience**: Graceful handling of missing data and site structure changes

### Data Processing Pipeline
- **Automated cleaning**: Remove duplicates, handle outliers, and standardize formats
- **Value validation**: Range checking for nutritional values (calories 0-1000, protein ≥ 0)
- **Unit standardization**: Convert between measurement systems (g, mg, mcg, IU)
- **Data enrichment**: Add metadata like food categories and serving sizes

### Export Capabilities
- 📄 **CSV Export**: Structured spreadsheet format for analysis
- 📊 **JSON Export**: Hierarchical format for web applications
- 🗄️ **Database Integration**: Direct export to SQLite/PostgreSQL
- 📈 **Visualization Ready**: Pre-aggregated data for charting tools

---

## 🛠️ Technology Stack

### Core Infrastructure

| Category | Technologies | Purpose |
|----------|--------------|---------|
| **Scraping Framework** | BeautifulSoup4, Selenium, Requests | Data extraction from websites |
| **Data Processing** | Pandas, NumPy, Regular Expressions | Data cleaning & manipulation |
| **Storage** | CSV, JSON, SQLite, PostgreSQL | Data persistence |
| **Orchestration** | Python 3.8+, Logging | Application logic & monitoring |
| **Visualization** | Matplotlib, Plotly (optional) | Data exploration |

### Key Python Libraries

```txt
beautifulsoup4>=4.12.0
selenium>=4.15.0
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
lxml>=4.9.0
python-dotenv>=1.0.0
```

---

## 📂 Project Blueprint

```
nutriscrape/
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── scraper.py              # Main scraping orchestrator
│   │   ├── parser.py               # HTML parsing utilities
│   │   └── config_manager.py       # Configuration handler
│   │
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── cleaner.py              # Data cleaning & validation
│   │   ├── normalizer.py           # Unit & format standardization
│   │   └── aggregator.py           # Data aggregation & stats
│   │
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── base_source.py          # Abstract source interface
│   │   ├── nutrition_db.py         # Source 1: Nutrition database
│   │   └── food_data.py            # Source 2: Food data platform
│   │
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── csv_exporter.py         # CSV export handler
│   │   ├── json_exporter.py        # JSON export handler
│   │   └── db_exporter.py          # Database export handler
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py           # Data validation utilities
│       ├── helpers.py              # Common helper functions
│       └── logger.py               # Logging configuration
│
├── data/
│   ├── raw/                        # Unprocessed scraped data
│   ├── interim/                    # Partially cleaned data
│   └── processed/                  # Final structured datasets
│
├── examples/
│   ├── basic_scrape.py             # Minimal scraping example
│   ├── custom_processing.py        # Advanced processing example
│   └── export_to_db.py             # Database export example
│
├── tests/
│   ├── test_scraper.py
│   ├── test_processor.py
│   └── test_validators.py
│
├── .env.example                     # Environment variables template
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development dependencies
├── setup.py                         # Package installation script
├── pyproject.toml                   # Modern Python project config
└── README.md                        # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed on your system
- **pip** package manager
- **Chrome/Chromium** browser (for Selenium-based scraping)
- Internet connection for scraping operations

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/Maryam535-projects/nutriscrape.git
cd nutriscrape

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Verify installation
python -c "import nutriscrape; print('✅ Successfully installed!')"
```

### Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Scraping Configuration
SCRAPING_DELAY=2                    # Seconds between requests
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
MAX_RETRIES=3
REQUEST_TIMEOUT=30

# Data Sources
NUTRITION_DATA_URL=https://example-nutrition-database.com
FOOD_DATABASE_URL=https://example-food-database.com

# Output Configuration
OUTPUT_DIR=./data/processed/
OUTPUT_FORMATS=csv,json             # Comma-separated formats
COMPRESS_OUTPUT=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/nutriscrape.log
```

### Quick Start

```python
# basic_usage.py
from nutriscrape.core import Scraper
from nutriscrape.processors import DataProcessor
from nutriscrape.exporters import CSVExporter

# Initialize scraper
scraper = Scraper()

# Scrape nutrition data
raw_data = scraper.scrape_food_items(["apple", "banana", "chicken"])

# Process the data
processor = DataProcessor()
cleaned_data = processor.process(raw_data)

# Export results
exporter = CSVExporter()
exporter.export(cleaned_data, "nutrition_data.csv")

print("✅ Data extraction complete!")
```

---

## 🔄 System Workflow

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                  (CLI / Web App / API)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATION LAYER                         │
│                   (Scraper Manager)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SOURCE ADAPTERS                             │
│         NutritionDB  │  FoodData  │  CustomSource              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA EXTRACTION                             │
│         Requests  │  Selenium  │  API Calls                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PROCESSING PIPELINE                         │
│    Parse → Clean → Validate → Normalize → Enrich → Aggregate   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EXPORT LAYER                                │
│         CSV  │  JSON  │  SQLite  │  PostgreSQL                │
└─────────────────────────────────────────────────────────────────┘
```

### Data Processing Pipeline

#### 1. Collection Phase
```
Start → Load Source Configuration → Fetch HTML → Parse Content → Extract Values → Store Raw
```

#### 2. Cleaning Phase
```
Load Raw Data → Remove Duplicates → Handle Missing Values → Correct Format → Validate Ranges
```

#### 3. Normalization Phase
```
Standardize Units → Normalize Names → Convert Categories → Create Metadata → Flag Anomalies
```

#### 4. Export Phase
```
Build Dataset → Create Aggregations → Format Output → Export Files → Generate Report
```

---

## 📊 Data Pipeline Example

### Input (Raw Scraped Data)
```json
{
    "item": "Apple",
    "calories": "52 kcal",
    "protein": "0.3g",
    "carbs": "14g",
    "fiber": "2.4g",
    "fat": "0.2g",
    "source": "nutritiondata.com"
}
```

### Processed Output (Standardized)
```csv
food_name,calories_kcal,protein_g,carb_g,fiber_g,fat_g,serving_size,unit
apple,52,0.3,14.0,2.4,0.2,100,grams
banana,89,1.1,22.8,2.6,0.3,100,grams
chicken_breast,165,31.0,0.0,0.0,3.6,100,grams
```

---

## 💡 Applications

### 🥗 Personal Health Tracking
- Build custom food diaries
- Track daily nutritional intake
- Monitor macro/micronutrient goals

### 🏋️ Sports Nutrition
- Plan pre/post workout meals
- Optimize protein and carbohydrate timing
- Track dietary supplements

### 📊 Data Science Research
- Train machine learning models
- Analyze food consumption patterns
- Identify nutritional trends

### 📱 App Development
- Power diet recommendation systems
- Enable food search features
- Build meal planning applications

---

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- [x] Basic scraping functionality
- [x] Data cleaning pipeline
- [x] CSV and JSON export
- [x] Documentation

### Phase 2: Enhancement 🚧
- [ ] API integration (USDA Food Data Central)
- [ ] Docker containerization
- [ ] Automated scheduling
- [ ] Web dashboard

### Phase 3: Advanced 🔮
- [ ] AI-powered data validation
- [ ] Real-time data updates
- [ ] Mobile application
- [ ] Advanced analytics

---

## 🤝 Contributing

We welcome all contributions! Here's how to get involved:

### 🐛 Reporting Issues
1. Check existing issues
2. Create detailed bug report
3. Include code samples and error logs

### 💻 Code Contributions
1. Fork the repository
2. Create branch: `git checkout -b feature/your-feature-name`
3. Write code and tests
4. Run tests: `pytest tests/`
5. Commit: `git commit -m "Description"`
6. Push: `git push origin feature/your-feature-name`
7. Open Pull Request

### 📝 Documentation
- Update README for configuration changes
- Add docstrings for new functions
- Create examples for new features

---

## 📄 License

```
MIT License

Copyright (c) 2024 Maryam Shuaib

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👩‍💻 Author

**Maryam Shuaib**

[![GitHub](https://img.shields.io/badge/GitHub-Maryam535--projects-181717?style=flat-square&logo=github)](https://github.com/Maryam535-projects)
[![Email](https://img.shields.io/badge/Email-maryamshuaib934@gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:maryamshuaib934@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Maryam_Shuaib-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/maryamshuaiib535)

---

## ⚠️ Legal Disclaimer

This project is intended for **educational and research purposes only**. Users are responsible for:

- Complying with website terms of service and robots.txt policies
- Obtaining proper permissions before scraping any website
- Using scraped data responsibly and ethically
- Not overloading target servers with excessive requests

The author assumes no liability for misuse of this software or violation of any laws or terms of service.

---

**Happy Scraping & Healthy Eating!** 🥗✨
