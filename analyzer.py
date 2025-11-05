# analyzer.py - Data Analysis Module

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAnalyzer:
    """Main class for data analysis operations"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load CSV file with error handling"""
        try:
            self.df = pd.read_csv(self.filepath)
            logger.info(f"✓ Data loaded successfully: {self.filepath}")
            logger.info(f"  Shape: {self.df.shape}")
            return True
        except FileNotFoundError:
            logger.error(f"✗ File not found: {self.filepath}")
            return False
        except pd.errors.EmptyDataError:
            logger.error("✗ File is empty")
            return False
        except Exception as e:
            logger.error(f"✗ Error loading file: {str(e)}")
            return False
    
    def get_overview(self):
        """Get comprehensive data overview"""
        if self.df is None:
            return None
        
        try:
            overview = {
                'rows': int(self.df.shape[0]),
                'columns': int(self.df.shape[1]),
                'column_names': list(self.df.columns),
                'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()},
                'missing_values': {col: int(count) for col, count in self.df.isnull().sum().items()},
                'duplicate_rows': int(self.df.duplicated().sum()),
                'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB"
            }
            logger.info("✓ Overview generated")
            return overview
        except Exception as e:
            logger.error(f"✗ Error generating overview: {str(e)}")
            return None
    
    def get_statistics(self):
        """Get descriptive statistics for numeric columns"""
        try:
            stats = self.df.describe().to_dict()
            logger.info("✓ Statistics calculated")
            return stats
        except Exception as e:
            logger.error(f"✗ Error calculating statistics: {str(e)}")
            return None
    
    def get_correlation(self):
        """Get correlation matrix for numeric columns"""
        try:
            numeric_df = self.df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                logger.warning("⚠ No numeric columns found")
                return None
            
            corr = numeric_df.corr().to_dict()
            logger.info("✓ Correlation matrix calculated")
            return corr
        except Exception as e:
            logger.error(f"✗ Error calculating correlation: {str(e)}")
            return None
    
    def get_head(self, n=5):
        """Get first n rows"""
        try:
            head = self.df.head(n).to_dict(orient='records')
            logger.info(f"✓ First {n} rows retrieved")
            return head
        except Exception as e:
            logger.error(f"✗ Error getting head: {str(e)}")
            return None
    
    def get_tail(self, n=5):
        """Get last n rows"""
        try:
            tail = self.df.tail(n).to_dict(orient='records')
            logger.info(f"✓ Last {n} rows retrieved")
            return tail
        except Exception as e:
            logger.error(f"✗ Error getting tail: {str(e)}")
            return None
    
    def get_column_stats(self, column):
        """Get detailed stats for specific column"""
        try:
            if column not in self.df.columns:
                logger.warning(f"⚠ Column not found: {column}")
                return None
            
            col_data = self.df[column]
            stats = {
                'unique': int(col_data.nunique()),
                'null_count': int(col_data.isnull().sum()),
                'null_percentage': float(col_data.isnull().sum() / len(col_data) * 100),
                'dtype': str(col_data.dtype),
                'value_counts': col_data.value_counts().head(10).to_dict()
            }
            logger.info(f"✓ Stats for column '{column}' retrieved")
            return stats
        except Exception as e:
            logger.error(f"✗ Error getting column stats: {str(e)}")
            return None
    
    def get_numeric_columns(self):
        """Get list of numeric columns"""
        try:
            cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            logger.info(f"✓ Found {len(cols)} numeric columns")
            return cols
        except Exception as e:
            logger.error(f"✗ Error getting numeric columns: {str(e)}")
            return []
    
    def get_categorical_columns(self):
        """Get list of categorical columns"""
        try:
            cols = self.df.select_dtypes(include=['object']).columns.tolist()
            logger.info(f"✓ Found {len(cols)} categorical columns")
            return cols
        except Exception as e:
            logger.error(f"✗ Error getting categorical columns: {str(e)}")
            return []
    
    def drop_missing(self):
        """Remove rows with missing values"""
        try:
            before = len(self.df)
            self.df = self.df.dropna()
            after = len(self.df)
            logger.info(f"✓ Dropped {before - after} rows with missing values")
            return before - after
        except Exception as e:
            logger.error(f"✗ Error dropping missing values: {str(e)}")
            return 0
    
    def drop_duplicates(self):
        """Remove duplicate rows"""
        try:
            before = len(self.df)
            self.df = self.df.drop_duplicates()
            after = len(self.df)
            logger.info(f"✓ Dropped {before - after} duplicate rows")
            return before - after
        except Exception as e:
            logger.error(f"✗ Error dropping duplicates: {str(e)}")
            return 0