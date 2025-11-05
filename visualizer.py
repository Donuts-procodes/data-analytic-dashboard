# visualizer.py - Data Visualization Module

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataVisualizer:
    """Class for creating data visualizations"""
    
    def __init__(self, df, output_dir='static/images/'):
        self.df = df
        self.output_dir = output_dir
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"✓ Visualizer initialized. Output: {output_dir}")
    
    def histogram(self, column, filename='histogram.png'):
        """Create histogram"""
        try:
            plt.figure(figsize=(10, 6))
            self.df[column].hist(bins=30, edgecolor='black', color='skyblue')
            plt.title(f'Histogram of {column}', fontsize=14, fontweight='bold')
            plt.xlabel(column)
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Histogram saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Error creating histogram: {str(e)}")
            return None
    
    def scatter_plot(self, x_col, y_col, filename='scatter.png'):
        """Create scatter plot"""
        try:
            plt.figure(figsize=(10, 6))
            plt.scatter(self.df[x_col], self.df[y_col], alpha=0.6, color='coral')
            plt.xlabel(x_col, fontsize=12)
            plt.ylabel(y_col, fontsize=12)
            plt.title(f'{x_col} vs {y_col}', fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Scatter plot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Error creating scatter plot: {str(e)}")
            return None
    
    def correlation_heatmap(self, filename='heatmap.png'):
        """Create correlation heatmap"""
        try:
            numeric_df = self.df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                logger.warning("⚠ No numeric columns for heatmap")
                return None
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', 
                       center=0, square=True, linewidths=1)
            plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
            
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Heatmap saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Error creating heatmap: {str(e)}")
            return None
    
    def box_plot(self, column, filename='boxplot.png'):
        """Create box plot"""
        try:
            plt.figure(figsize=(10, 6))
            self.df[column].plot(kind='box', figsize=(10, 6))
            plt.title(f'Box Plot of {column}', fontsize=14, fontweight='bold')
            plt.ylabel(column)
            plt.grid(True, alpha=0.3)
            
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Box plot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Error creating box plot: {str(e)}")
            return None
    
    def line_chart(self, column, filename='line_chart.png'):
        """Create line chart"""
        try:
            plt.figure(figsize=(12, 6))
            self.df[column].plot(figsize=(12, 6), color='green', linewidth=2)
            plt.title(f'Line Chart of {column}', fontsize=14, fontweight='bold')
            plt.ylabel(column)
            plt.xlabel('Index')
            plt.grid(True, alpha=0.3)
            
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Line chart saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Error creating line chart: {str(e)}")
            return None
    
    def bar_chart(self, column, filename='bar_chart.png'):
        """Create bar chart for categorical data"""
        try:
            plt.figure(figsize=(12, 6))
            value_counts = self.df[column].value_counts().head(10)
            value_counts.plot(kind='bar', color='purple', alpha=0.7)
            plt.title(f'Bar Chart of {column}', fontsize=14, fontweight='bold')
            plt.ylabel('Count')
            plt.xlabel(column)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3, axis='y')
            
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Bar chart saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Error creating bar chart: {str(e)}")
            return None
    
    def distribution_plot(self, column, filename='distribution.png'):
        """Create distribution plot"""
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(self.df[column], kde=True, color='blue', alpha=0.6)
            plt.title(f'Distribution of {column}', fontsize=14, fontweight='bold')
            plt.xlabel(column)
            plt.grid(True, alpha=0.3)
            
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Distribution plot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"✗ Error creating distribution plot: {str(e)}")
            return None