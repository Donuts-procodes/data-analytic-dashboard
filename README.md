# README.md - Data Analytics Project

# 📊 Data Analytics Dashboard

A powerful web-based data analytics tool built with Flask, Pandas, and Matplotlib. Upload CSV files, explore data, and generate beautiful visualizations.

---

## ✨ Features

✅ **CSV Upload** - Drag-and-drop file upload  
✅ **Data Exploration** - View first/last rows, column info, statistics  
✅ **Statistical Analysis** - Descriptive stats, correlation, groupby  
✅ **Beautiful Visualizations** - Histograms, scatter plots, heatmaps, box plots, bar charts, line charts  
✅ **Data Cleaning** - Handle missing values, remove duplicates  
✅ **Responsive UI** - Works on desktop and mobile  
✅ **Comprehensive Testing** - 20+ unit tests  
✅ **Detailed Logging** - Full debug and error tracking  

---

## 📁 Project Structure

```
data-analytics/
├── venv/
├── templates/
│   ├── index.html
│   ├── analysis.html
│   └── base.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
├── uploads/
├── analyzer.py              # Data analysis module
├── visualizer.py            # Visualization module
├── app.py                   # Flask application
├── test_app.py              # Test suite
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Setup

```bash
# Create project folder
mkdir data-analytics
cd data-analytics

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Run

```bash
python app.py
```

Open browser: http://127.0.0.1:5000

### 3. Test

```bash
python -m unittest test_app.py -v
```

---

## 📊 How to Use

1. **Upload CSV** - Click to upload or drag-and-drop
2. **Explore Data** - View overview, statistics, first/last rows
3. **Analyze** - Check correlation, group by analysis
4. **Visualize** - Create charts and graphs
5. **Export** - Download visualizations

---

## 🛠️ Python Modules

### `analyzer.py`
```python
analyzer = DataAnalyzer('data.csv')
overview = analyzer.get_overview()
stats = analyzer.get_statistics()
corr = analyzer.get_correlation()
```

### `visualizer.py`
```python
visualizer = DataVisualizer(df)
visualizer.histogram('column_name')
visualizer.scatter_plot('x_col', 'y_col')
visualizer.correlation_heatmap()
```

### `app.py`
Flask application with endpoints:
- `GET /` - Home page
- `POST /upload` - Upload CSV
- `GET /analysis/<filename>` - Analysis page
- `POST /api/visualize` - Generate charts
- `GET /health` - Health check

---

## 📈 Supported Visualizations

- 📊 **Histogram** - Distribution of numeric data
- 📍 **Scatter Plot** - Relationship between two variables
- 🔥 **Heatmap** - Correlation matrix
- 📦 **Box Plot** - Statistical summary
- 📈 **Line Chart** - Time series or sequential data
- 📊 **Bar Chart** - Categorical data
- 📉 **Distribution Plot** - Probability distribution

---

## 🧪 Testing

```bash
# Run all tests
python -m unittest test_app.py -v

# Run specific test class
python -m unittest test_app.TestDataAnalyzer -v

# Run specific test
python -m unittest test_app.TestDataAnalyzer.test_data_loading -v

# Test with coverage
pip install coverage
coverage run -m unittest test_app.py
coverage report
```

### Test Coverage

- **DataAnalyzer Tests** - 10 tests
- **Flask App Tests** - 6 tests
- **DataVisualizer Tests** - 4 tests
- **Performance Tests** - 1 test
- **Total: 21 tests**

---

## 🔍 Debugging

### Enable Debug Logging

```python
# In app.py - logging is already configured
# Check console for detailed logs
```

### Common Issues

**ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Port 5000 in use**
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

**File upload fails**
- Check file is CSV format
- Check file size < 16MB
- Check 'uploads' folder exists

---

## 📝 Sample Data

Create `sample_data.csv`:
```csv
Name,Age,Salary,Department
Alice,25,50000,HR
Bob,30,60000,IT
Charlie,35,75000,Finance
David,28,55000,IT
Eve,32,65000,HR
```

---

## 🎯 Features to Add

- [ ] Multiple file support
- [ ] Data filtering & sorting
- [ ] Export to Excel/PDF
- [ ] Advanced statistics (regression, hypothesis testing)
- [ ] Time series analysis
- [ ] Database integration
- [ ] User authentication
- [ ] Dark mode

---

## 💡 Use Cases

✅ Business Analytics  
✅ Data Science Learning  
✅ Portfolio Projects  
✅ Data Exploration  
✅ Quick Insights  
✅ Presentation Data  

---

## 📞 Technology Stack

- **Backend**: Flask, Python
- **Data**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Frontend**: HTML, CSS, JavaScript
- **Testing**: Python unittest
- **Logging**: Python logging

---

## 🚀 Deployment Ready

- ✅ Error handling
- ✅ Input validation
- ✅ Security (file validation, secure filenames)
- ✅ Logging
- ✅ Tests
- ✅ Performance optimized

---

## 📄 License

MIT License - Free to use!

---

**Happy Analyzing! 📊✨**
# data-analytic-dashboard
