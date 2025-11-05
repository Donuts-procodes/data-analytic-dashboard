# test_app_fixed.py - Fixed Test Suite

import unittest
import os
import json
import tempfile
import shutil
from app import app
from analyzer import DataAnalyzer
from visualizer import DataVisualizer
import pandas as pd
import numpy as np

class TestDataAnalyzer(unittest.TestCase):
    """Test DataAnalyzer class"""
    
    def setUp(self):
        """Setup test data"""
        self.test_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.test_dir, 'test_data.csv')
        
        # Create sample CSV
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Age': [25, 30, 35, 28, 32],
            'Salary': [50000, 60000, 75000, 55000, 65000],
            'Department': ['HR', 'IT', 'Finance', 'IT', 'HR']
        })
        df.to_csv(self.csv_file, index=False)
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)
    
    def test_data_loading(self):
        """Test data loading"""
        analyzer = DataAnalyzer(self.csv_file)
        self.assertIsNotNone(analyzer.df)
        self.assertEqual(len(analyzer.df), 5)
    
    def test_file_not_found(self):
        """Test file not found error"""
        analyzer = DataAnalyzer('nonexistent.csv')
        self.assertIsNone(analyzer.df)
    
    def test_get_overview(self):
        """Test overview generation"""
        analyzer = DataAnalyzer(self.csv_file)
        overview = analyzer.get_overview()
        
        self.assertIsNotNone(overview)
        self.assertEqual(overview['rows'], 5)
        self.assertEqual(overview['columns'], 4)
        self.assertEqual(len(overview['column_names']), 4)
    
    def test_get_statistics(self):
        """Test statistics generation"""
        analyzer = DataAnalyzer(self.csv_file)
        stats = analyzer.get_statistics()
        
        self.assertIsNotNone(stats)
        self.assertIn('Age', stats)
        self.assertIn('Salary', stats)
    
    def test_get_correlation(self):
        """Test correlation calculation"""
        analyzer = DataAnalyzer(self.csv_file)
        corr = analyzer.get_correlation()
        
        self.assertIsNotNone(corr)
        self.assertIn('Age', corr)
    
    def test_get_head(self):
        """Test getting first rows"""
        analyzer = DataAnalyzer(self.csv_file)
        head = analyzer.get_head(3)
        
        self.assertEqual(len(head), 3)
        self.assertEqual(head[0]['Name'], 'Alice')
    
    def test_get_tail(self):
        """Test getting last rows"""
        analyzer = DataAnalyzer(self.csv_file)
        tail = analyzer.get_tail(2)
        
        self.assertEqual(len(tail), 2)
        self.assertEqual(tail[-1]['Name'], 'Eve')
    
    def test_get_numeric_columns(self):
        """Test getting numeric columns"""
        analyzer = DataAnalyzer(self.csv_file)
        numeric = analyzer.get_numeric_columns()
        
        self.assertIn('Age', numeric)
        self.assertIn('Salary', numeric)
        self.assertNotIn('Name', numeric)
    
    def test_get_categorical_columns(self):
        """Test getting categorical columns"""
        analyzer = DataAnalyzer(self.csv_file)
        categorical = analyzer.get_categorical_columns()
        
        self.assertIn('Name', categorical)
        self.assertIn('Department', categorical)
        self.assertNotIn('Age', categorical)
    
    def test_column_stats(self):
        """Test column statistics"""
        analyzer = DataAnalyzer(self.csv_file)
        stats = analyzer.get_column_stats('Age')
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['unique'], 5)
        self.assertEqual(stats['null_count'], 0)


class TestFlaskApp(unittest.TestCase):
    """Test Flask app endpoints"""
    
    def setUp(self):
        """Setup test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create test CSV
        self.test_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.test_dir, 'test_data.csv')
        
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': ['x', 'y', 'z', 'x', 'y']
        })
        df.to_csv(self.csv_file, index=False)
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data Analytics', response.data)
    
    def test_health_check(self):
        """Test health endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_upload_no_file(self):
        """Test upload with no file"""
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 400)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


class TestDataVisualizer(unittest.TestCase):
    """Test DataVisualizer class"""
    
    def setUp(self):
        """Setup test data"""
        self.test_dir = tempfile.mkdtemp()
        self.df = pd.DataFrame({
            'X': np.random.rand(100),
            'Y': np.random.rand(100),
            'Z': np.random.choice(['A', 'B', 'C'], 100)
        })
        self.visualizer = DataVisualizer(self.df, output_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)
    
    def test_histogram_creation(self):
        """Test histogram creation"""
        result = self.visualizer.histogram('X', 'test_hist.png')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, result)))
    
    def test_scatter_creation(self):
        """Test scatter plot creation"""
        result = self.visualizer.scatter_plot('X', 'Y', 'test_scatter.png')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, result)))
    
    def test_boxplot_creation(self):
        """Test box plot creation"""
        result = self.visualizer.box_plot('X', 'test_boxplot.png')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, result)))


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🧪 Running Data Analytics Test Suite")
    print("=" * 60 + "\n")
    
    unittest.main(verbosity=2)
