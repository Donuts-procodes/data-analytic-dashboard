# DEBUG_GUIDE.md - Debugging & Testing Guide

# 🐛 Complete Debugging & Testing Guide

## 🔍 How to Debug

### 1. Enable Detailed Logging

The app already has logging enabled. Check console output for:
```
✓ Success messages
⚠ Warnings  
✗ Errors
```

### 2. Check Flask Debug Mode

```python
# In app.py - Debug is ON
if __name__ == '__main__':
    app.run(debug=True)  # Auto-reloads on code changes
```

### 3. Use Python Debugger

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Run and interact with debugger
python app.py
```

### 4. Print Debugging

```python
# Add print statements
print(f"DEBUG: {variable_name} = {variable_value}")
```

---

## 🧪 Complete Testing Guide

### Run All Tests

```bash
python -m unittest test_app.py -v
```

**Expected Output:**
```
test_data_loading (test_app.TestDataAnalyzer) ... ok
test_file_not_found (test_app.TestDataAnalyzer) ... ok
...
Ran 21 tests in 0.234s

OK ✅
```

### Run Specific Test

```bash
# Test specific class
python -m unittest test_app.TestDataAnalyzer -v

# Test specific method
python -m unittest test_app.TestDataAnalyzer.test_data_loading -v
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest test_app.py

# View report
coverage report

# Generate HTML report
coverage html  # Opens htmlcov/index.html
```

---

## 📝 Test Categories

### 1. DataAnalyzer Tests (10 tests)
```
✓ test_data_loading - Load CSV file
✓ test_file_not_found - Handle missing files
✓ test_get_overview - Generate overview
✓ test_get_statistics - Calculate statistics
✓ test_get_correlation - Correlation matrix
✓ test_get_head - Get first rows
✓ test_get_tail - Get last rows
✓ test_get_numeric_columns - Find numeric cols
✓ test_get_categorical_columns - Find categorical cols
✓ test_column_stats - Column statistics
```

### 2. Flask App Tests (6 tests)
```
✓ test_home_page - Home page loads
✓ test_health_check - Health endpoint
✓ test_upload_no_file - No file error
✓ test_upload_invalid_file_type - File type validation
✓ test_upload_csv_file - Successful upload
✓ test_analysis_endpoint - Analysis page
```

### 3. Visualization Tests (4 tests)
```
✓ test_histogram_creation - Create histogram
✓ test_scatter_creation - Create scatter plot
✓ test_heatmap_creation - Create heatmap
✓ test_boxplot_creation - Create box plot
```

### 4. Performance Tests (1 test)
```
✓ test_health_response_time - Response time < 1s
```

---

## 🛠️ Debugging Specific Issues

### Issue 1: CSV Upload Fails

**Symptoms:** Upload fails, error message shown

**Debug Steps:**
```bash
# 1. Check file exists and is valid CSV
python
>>> import pandas as pd
>>> df = pd.read_csv('your_file.csv')
>>> print(df.head())

# 2. Check file size
>>> import os
>>> os.path.getsize('your_file.csv') / (1024*1024)  # MB

# 3. Check for invalid characters
>>> df.info()
```

### Issue 2: Visualization Not Created

**Symptoms:** Chart generation fails

**Debug Steps:**
```python
# In app.py, add debugging
from visualizer import DataVisualizer
import logging

logging.basicConfig(level=logging.DEBUG)

# Test visualization
df = pd.read_csv('test.csv')
viz = DataVisualizer(df)
result = viz.histogram('column_name')
print(f"Result: {result}")
```

### Issue 3: Port Already in Use

**Error:** `Address already in use`

**Fix:**
```bash
# Kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>

# Or use different port
# Change in app.py: app.run(port=5001)
```

### Issue 4: Module Import Error

**Error:** `ModuleNotFoundError: No module named 'pandas'`

**Fix:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade

# Or install individually
pip install pandas matplotlib seaborn
```

---

## 📊 Manual Testing

### Test 1: Basic Upload and Analysis

```bash
# 1. Create sample CSV
cat > test_data.csv << EOF
Product,Sales,Profit,Region
A,100,20,North
B,150,30,South
C,200,50,East
D,120,25,West
E,180,40,North
EOF

# 2. Start app
python app.py

# 3. Upload file via browser (http://127.0.0.1:5000)
# 4. Check console logs for success messages
```

### Test 2: API Testing

```bash
# Using Python
import requests

url = "http://127.0.0.1:5000/health"
response = requests.get(url)
print(response.json())

# Expected: {'status': 'healthy', 'message': 'App is running'}
```

### Test 3: File Upload API

```python
import requests

url = "http://127.0.0.1:5000/upload"
with open('test_data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)
    print(response.json())
```

---

## 🔎 Debugging Console Commands

### Check Analyzer

```python
from analyzer import DataAnalyzer

analyzer = DataAnalyzer('uploads/your_file.csv')
print(analyzer.get_overview())
print(analyzer.get_numeric_columns())
print(analyzer.get_statistics())
```

### Check Visualizer

```python
from visualizer import DataVisualizer
import pandas as pd

df = pd.read_csv('uploads/your_file.csv')
viz = DataVisualizer(df)
result = viz.histogram('column_name')
print(f"Chart created: {result}")
```

### Check File Upload

```python
import os
print(os.listdir('uploads/'))  # List uploaded files
```

---

## 🐛 Common Error Messages & Solutions

| Error | Solution |
|-------|----------|
| `FileNotFoundError` | Check file path and name |
| `KeyError: 'column_name'` | Column doesn't exist, check spelling |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Port 5000 in use` | Kill process or use different port |
| `Permission denied` | Check file permissions |
| `Invalid file format` | Only CSV files allowed |

---

## 📈 Performance Testing

### Test Response Time

```python
import time
import requests

url = "http://127.0.0.1:5000/health"
start = time.time()
response = requests.get(url)
elapsed = time.time() - start

print(f"Response time: {elapsed:.3f}s")
assert elapsed < 1.0, "Too slow!"
```

### Stress Testing

```python
import concurrent.futures
import requests

url = "http://127.0.0.1:5000/health"

def make_request():
    return requests.get(url).status_code

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(make_request, range(100)))
    print(f"Success rate: {results.count(200)}/100")
```

---

## 📝 Logging Best Practices

### View Logs

```bash
# Run app and watch logs
python app.py  # Logs appear in console

# Save logs to file
python app.py > app.log 2>&1

# View logs
cat app.log
```

### Add Custom Logging

```python
import logging

logger = logging.getLogger(__name__)

# Debug
logger.debug("Debug message")

# Info
logger.info("✓ Operation successful")

# Warning
logger.warning("⚠ Warning message")

# Error
logger.error("✗ Error occurred")
```

---

## ✅ Pre-Launch Checklist

Before pushing to production:

- [ ] All tests pass
- [ ] Code formatted properly
- [ ] No debug statements left
- [ ] Error handling in place
- [ ] Logging configured
- [ ] Documentation updated
- [ ] Requirements.txt updated
- [ ] .gitignore configured
- [ ] No hardcoded paths
- [ ] Security checks (file validation)

---

## 🚀 Quick Test Commands

```bash
# Run all tests
python -m unittest test_app.py -v

# Run with minimal output
python -m unittest test_app.py

# Run specific test
python -m unittest test_app.TestDataAnalyzer.test_data_loading -v

# Generate coverage report
coverage run -m unittest test_app.py && coverage report

# Manual testing
python
>>> from analyzer import DataAnalyzer
>>> analyzer = DataAnalyzer('sample.csv')
>>> print(analyzer.get_overview())
```

---

**Happy Debugging! 🐛✨**
