## Otodom.pl Data Analysis


Analysis second market Warsaw apartments data from oto-dom.pl website. Including scrapping data, which has been done at the end of May 2024.

### Introduction

This project is designed to automate web scraping oto-dom.pl website, data cleaning, analysis, visualization, and potentially regression modeling. It utilizes Python libraries like Selenium, pandas, NumPy, Scikit-learn, and Dash for interactive dashboards.

### Project Structure

otodom-data-scraping.py:  Contains Python scripts to scrape data from websites using Selenium.
data_cleaning.py:         Python scripts for cleaning and preprocessing the scraped data.
data_analysis.ipynb:      Includes Jupyter Notebook files (*.ipynb) for exploratory data analysis and visualization using libraries like pandas, NumPy, Seaborn, Matplotlib, Plotly Express, etc.
Dashboard:                Encompasses Python scripts and HTML files to create interactive dashboards using Dash and Dash Bootstrap Components.
regression_model.py:      Contains Python scripts for building a regression model using Scikit-learn's LinearRegression.
requirements.txt:         Contains the project dependencies (Python libraries).


### Requirements

Install libraries by using `pip`:

```bash
pip install -r requirements.txt
```

## Instructions

### Set Up Environment:

Create a virtual environment to isolate project dependencies (recommended).
Install the required libraries using pip install -r requirements.txt (if the file exists).
Ensure you have compatible browser drivers installed for Selenium to work. Refer to Selenium documentation for details.

### Data Scraping:

Run the otodom-web-scraping.py scripts to scrape the desired data.

### Data Cleaning:

Open the Jupyter Notebooks in the data_cleaning directory.
Execute the code cells to clean the data.

### Data Analysis:
.
Run the code cells to perform data analysis.

### Dashboard Creation:

Run the script to generate an interactive dashboard.

### Regression Modeling:

Open the Python regression_model.py script.
Run the script to build and evaluate the regression model.

