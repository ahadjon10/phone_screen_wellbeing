#!/usr/bin/env python3
"""
StudentLife Data Loader
======================

Utilities for loading and preprocessing the StudentLife dataset.
"""

import os
import glob
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class StudentLifeLoader:
    """Loader for StudentLife dataset files."""
    
    def __init__(self, data_dir='../data/raw'):
        """
        Initialize the data loader.
        
        Args:
            data_dir (str): Path to the raw data directory
        """
        self.data_dir = Path(data_dir)
        self.user_ids = self._get_user_ids()
        self.sensor_types = ['gps', 'accel', 'wifi', 'bluetooth', 'conversation', 
                            'app', 'screen', 'ema', 'survey']
    
    def _get_user_ids(self):
        """Get list of user IDs from the data directory."""
        if not self.data_dir.exists():
            return []
        
        user_dirs = [d.name for d in self.data_dir.iterdir() 
                     if d.is_dir() and str(d.name).startswith('u')]
        return sorted(user_dirs)
    
    def list_files(self, user_id=None, sensor_type=None):
        """
        List files in the dataset.
        
        Args:
            user_id (str): Specific user ID to filter by
            sensor_type (str): Specific sensor type to filter by
            
        Returns:
            list: List of file paths
        """
        files = []
        
        if user_id:
            user_dir = self.data_dir / user_id
            if sensor_type:
                sensor_dir = user_dir / sensor_type
                if sensor_dir.exists():
                    files = list(sensor_dir.glob('*.csv'))
            else:
                if user_dir.exists():
                    files = list(user_dir.rglob('*.csv'))
        else:
            if sensor_type:
                sensor_dir = self.data_dir / sensor_type
                if sensor_dir.exists():
                    files = list(sensor_dir.rglob('*.csv'))
            else:
                files = list(self.data_dir.rglob('*.csv'))
        
        return files
    
    def load_gps_data(self, user_id, date=None, limit_rows=None):
        """
        Load GPS data for a specific user and date.
        
        Args:
            user_id (str): User identifier (e.g., 'u001')
            date (str): Specific date in YYYYMMDD format
            limit_rows (int): Maximum number of rows to load
            
        Returns:
            pd.DataFrame: GPS data with columns: timestamp, latitude, longitude, accuracy
        """
        gps_dir = self.data_dir / 'gps' / user_id
        
        if not gps_dir.exists():
            warnings.warn(f"GPS directory not found for user {user_id}")
            return pd.DataFrame()
        
        # Find matching files
        if date:
            files = list(gps_dir.glob(f'*{date}.csv'))
        else:
            files = list(gps_dir.glob('*.csv'))
        
        if not files:
            warnings.warn(f"No GPS files found for user {user_id}")
            return pd.DataFrame()
        
        # Load all matching files
        dfs = []
        for file_path in files:
            try:
                df = pd.read_csv(file_path)
                if limit_rows:
                    df = df.head(limit_rows)
                dfs.append(df)
            except Exception as e:
                warnings.warn(f"Error loading {file_path}: {e}")
        
        if not dfs:
            return pd.DataFrame()
        
        # Combine and process
        gps_df = pd.concat(dfs, ignore_index=True)
        
        # Standardize column names
        gps_df = self._standardize_gps_columns(gps_df)
        
        # Convert timestamp if present
        if 'timestamp' in gps_df.columns:
            gps_df['timestamp'] = pd.to_datetime(gps_df['timestamp'], unit='ms')
        
        return gps_df
    
    def _standardize_gps_columns(self, df):
        """Standardize GPS column names."""
        column_mapping = {
            'Timestamp': 'timestamp',
            'Latitude': 'latitude',
            'Longitude': 'longitude',
            'Accuracy': 'accuracy',
            'time': 'timestamp',
            'lat': 'latitude',
            'lon': 'longitude',
            'long': 'longitude',
            'acc': 'accuracy'
        }
        
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        # Ensure required columns exist
        required_cols = ['timestamp', 'latitude', 'longitude']
        for col in required_cols:
            if col not in df.columns:
                warnings.warn(f"Missing required GPS column: {col}")
        
        return df
    
    def load_accel_data(self, user_id, date=None, limit_rows=None):
        """
        Load accelerometer data for a specific user and date.
        
        Args:
            user_id (str): User identifier
            date (str): Specific date in YYYYMMDD format
            limit_rows (int): Maximum number of rows to load
            
        Returns:
            pd.DataFrame: Accelerometer data with columns: timestamp, x, y, z
        """
        accel_dir = self.data_dir / 'accel' / user_id
        
        if not accel_dir.exists():
            warnings.warn(f"Accelerometer directory not found for user {user_id}")
            return pd.DataFrame()
        
        # Find matching files
        if date:
            files = list(accel_dir.glob(f'*{date}.csv'))
        else:
            files = list(accel_dir.glob('*.csv'))
        
        if not files:
            warnings.warn(f"No accelerometer files found for user {user_id}")
            return pd.DataFrame()
        
        # Load all matching files
        dfs = []
        for file_path in files:
            try:
                df = pd.read_csv(file_path)
                if limit_rows:
                    df = df.head(limit_rows)
                dfs.append(df)
            except Exception as e:
                warnings.warn(f"Error loading {file_path}: {e}")
        
        if not dfs:
            return pd.DataFrame()
        
        # Combine and process
        accel_df = pd.concat(dfs, ignore_index=True)
        
        # Standardize column names
        accel_df = self._standardize_accel_columns(accel_df)
        
        # Convert timestamp if present
        if 'timestamp' in accel_df.columns:
            accel_df['timestamp'] = pd.to_datetime(accel_df['timestamp'], unit='ms')
        
        # Calculate magnitude
        if all(col in accel_df.columns for col in ['x', 'y', 'z']):
            accel_df['magnitude'] = np.sqrt(accel_df['x']**2 + accel_df['y']**2 + accel_df['z']**2)
        
        return accel_df
    
    def _standardize_accel_columns(self, df):
        """Standardize accelerometer column names."""
        column_mapping = {
            'Timestamp': 'timestamp',
            'X': 'x',
            'Y': 'y',
            'Z': 'z',
            'time': 'timestamp'
        }
        
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        return df
    
    def load_wifi_data(self, user_id, date=None, limit_rows=None):
        """
        Load WiFi data for a specific user and date.
        
        Args:
            user_id (str): User identifier
            date (str): Specific date in YYYYMMDD format
            limit_rows (int): Maximum number of rows to load
            
        Returns:
            pd.DataFrame: WiFi data
        """
        wifi_dir = self.data_dir / 'wifi' / user_id
        
        if not wifi_dir.exists():
            warnings.warn(f"WiFi directory not found for user {user_id}")
            return pd.DataFrame()
        
        # Find matching files
        if date:
            files = list(wifi_dir.glob(f'*{date}.csv'))
        else:
            files = list(wifi_dir.glob('*.csv'))
        
        if not files:
            warnings.warn(f"No WiFi files found for user {user_id}")
            return pd.DataFrame()
        
        # Load all matching files
        dfs = []
        for file_path in files:
            try:
                df = pd.read_csv(file_path)
                if limit_rows:
                    df = df.head(limit_rows)
                dfs.append(df)
            except Exception as e:
                warnings.warn(f"Error loading {file_path}: {e}")
        
        if not dfs:
            return pd.DataFrame()
        
        wifi_df = pd.concat(dfs, ignore_index=True)
        
        # Standardize column names
        wifi_df = self._standardize_wifi_columns(wifi_df)
        
        return wifi_df
    
    def _standardize_wifi_columns(self, df):
        """Standardize WiFi column names."""
        column_mapping = {
            'Timestamp': 'timestamp',
            'SSID': 'ssid',
            'BSSID': 'bssid',
            'RSSI': 'rssi',
            'time': 'timestamp'
        }
        
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        return df
    
    def load_conversation_data(self, user_id, date=None, limit_rows=None):
        """
        Load conversation data for a specific user and date.
        
        Args:
            user_id (str): User identifier
            date (str): Specific date in YYYYMMDD format
            limit_rows (int): Maximum number of rows to load
            
        Returns:
            pd.DataFrame: Conversation data
        """
        conv_dir = self.data_dir / 'conversation' / user_id
        
        if not conv_dir.exists():
            warnings.warn(f"Conversation directory not found for user {user_id}")
            return pd.DataFrame()
        
        # Find matching files
        if date:
            files = list(conv_dir.glob(f'*{date}.csv'))
        else:
            files = list(conv_dir.glob('*.csv'))
        
        if not files:
            warnings.warn(f"No conversation files found for user {user_id}")
            return pd.DataFrame()
        
        # Load all matching files
        dfs = []
        for file_path in files:
            try:
                df = pd.read_csv(file_path)
                if limit_rows:
                    df = df.head(limit_rows)
                dfs.append(df)
            except Exception as e:
                warnings.warn(f"Error loading {file_path}: {e}")
        
        if not dfs:
            return pd.DataFrame()
        
        conv_df = pd.concat(dfs, ignore_index=True)
        
        # Standardize column names
        conv_df = self._standardize_conversation_columns(conv_df)
        
        return conv_df
    
    def _standardize_conversation_columns(self, df):
        """Standardize conversation column names."""
        column_mapping = {
            'Timestamp': 'timestamp',
            'Start': 'start_time',
            'End': 'end_time',
            'Duration': 'duration',
            'time': 'timestamp',
            'start': 'start_time',
            'end': 'end_time',
            'duration': 'duration'
        }
        
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        return df
    
    def load_ema_data(self, user_id, date=None, limit_rows=None):
        """
        Load EMA (Ecological Momentary Assessment) data.
        
        Args:
            user_id (str): User identifier
            date (str): Specific date in YYYYMMDD format
            limit_rows (int): Maximum number of rows to load
            
        Returns:
            pd.DataFrame: EMA data with self-reported assessments
        """
        ema_dir = self.data_dir / 'ema' / user_id
        
        if not ema_dir.exists():
            warnings.warn(f"EMA directory not found for user {user_id}")
            return pd.DataFrame()
        
        # Find matching files
        if date:
            files = list(ema_dir.glob(f'*{date}.csv'))
        else:
            files = list(ema_dir.glob('*.csv'))
        
        if not files:
            warnings.warn(f"No EMA files found for user {user_id}")
            return pd.DataFrame()
        
        # Load all matching files
        dfs = []
        for file_path in files:
            try:
                df = pd.read_csv(file_path)
                if limit_rows:
                    df = df.head(limit_rows)
                dfs.append(df)
            except Exception as e:
                warnings.warn(f"Error loading {file_path}: {e}")
        
        if not dfs:
            return pd.DataFrame()
        
        ema_df = pd.concat(dfs, ignore_index=True)
        
        return ema_df
    
    def load_survey_data(self, user_id=None):
        """
        Load survey data (mental health assessments).
        
        Args:
            user_id (str): Specific user ID or None for all users
            
        Returns:
            pd.DataFrame: Survey data
        """
        survey_dir = self.data_dir / 'survey'
        
        if not survey_dir.exists():
            warnings.warn("Survey directory not found")
            return pd.DataFrame()
        
        if user_id:
            survey_file = survey_dir / f'{user_id}.csv'
            if not survey_file.exists():
                warnings.warn(f"Survey file not found for user {user_id}")
                return pd.DataFrame()
            
            try:
                df = pd.read_csv(survey_file)
                return df
            except Exception as e:
                warnings.warn(f"Error loading survey for {user_id}: {e}")
                return pd.DataFrame()
        else:
            # Load all survey files
            survey_files = list(survey_dir.glob('*.csv'))
            dfs = []
            
            for file_path in survey_files:
                try:
                    df = pd.read_csv(file_path)
                    # Add user_id column
                    df['user_id'] = file_path.stem
                    dfs.append(df)
                except Exception as e:
                    warnings.warn(f"Error loading {file_path}: {e}")
            
            if not dfs:
                return pd.DataFrame()
            
            return pd.concat(dfs, ignore_index=True)
    
    def get_dataset_stats(self):
        """
        Get statistics about the dataset.
        
        Returns:
            dict: Dataset statistics
        """
        stats = {
            'total_users': len(self.user_ids),
            'user_ids': self.user_ids,
            'sensor_types': {},
            'total_files': 0
        }
        
        for sensor_type in self.sensor_types:
            sensor_dir = self.data_dir / sensor_type
            if sensor_dir.exists():
                files = list(sensor_dir.rglob('*.csv'))
                stats['sensor_types'][sensor_type] = len(files)
                stats['total_files'] += len(files)
            else:
                stats['sensor_types'][sensor_type] = 0
        
        return stats


def main():
    """Example usage of the StudentLifeLoader."""
    loader = StudentLifeLoader()
    
    # Print dataset statistics
    stats = loader.get_dataset_stats()
    print("Dataset Statistics:")
    print(f"Total users: {stats['total_users']}")
    print(f"Total files: {stats['total_files']}")
    print("Files by sensor type:")
    for sensor_type, count in stats['sensor_types'].items():
        print(f"  {sensor_type}: {count}")
    
    # Example: Load GPS data for first user
    if stats['total_users'] > 0:
        first_user = stats['user_ids'][0]
        print(f"\nLoading GPS data for user {first_user}...")
        gps_df = loader.load_gps_data(first_user, limit_rows=10)
        if not gps_df.empty:
            print(f"GPS data shape: {gps_df.shape}")
            print(f"Columns: {list(gps_df.columns)}")
            print(gps_df.head())


if __name__ == '__main__':
    main()