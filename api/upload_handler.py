"""
File upload handler for SpecSailor
Validates and parses user data files (CSV, Excel, JSON)
"""

from fastapi import UploadFile, HTTPException
import pandas as pd
import json
import io
from datetime import datetime
from typing import Dict, List
import uuid


class DataUploadHandler:
    """Handle file uploads and validation"""

    REQUIRED_COLUMNS = ['user_id', 'event_timestamp', 'event_type']
    ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.json']
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

    @staticmethod
    async def validate_and_parse(file: UploadFile) -> Dict:
        """
        Validate uploaded file and parse into DataFrame

        Returns:
            {
                'upload_id': str,
                'data': pd.DataFrame,
                'validation': {
                    'is_valid': bool,
                    'errors': List[str],
                    'warnings': List[str]
                },
                'summary': {
                    'total_events': int,
                    'unique_users': int,
                    'date_range': tuple,
                    'event_types': List[str]
                }
            }
        """

        # Check file extension
        file_ext = '.' + file.filename.split('.')[-1].lower()
        if file_ext not in DataUploadHandler.ALLOWED_EXTENSIONS:
            raise HTTPException(400, f"Unsupported file type: {file_ext}")

        # Read file content
        content = await file.read()

        # Check file size
        if len(content) > DataUploadHandler.MAX_FILE_SIZE:
            raise HTTPException(400, "File too large (max 50 MB)")

        # Parse based on file type
        try:
            if file_ext == '.csv':
                df = pd.read_csv(io.BytesIO(content))
            elif file_ext == '.xlsx':
                df = pd.read_excel(io.BytesIO(content))
            elif file_ext == '.json':
                df = pd.read_json(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(400, f"Failed to parse file: {str(e)}")

        # Validate columns
        validation_result = DataUploadHandler._validate_columns(df)

        if not validation_result['is_valid']:
            raise HTTPException(400, f"Validation failed: {validation_result['errors']}")

        # Generate upload ID
        upload_id = str(uuid.uuid4())

        # Create summary
        summary = DataUploadHandler._create_summary(df)

        return {
            'upload_id': upload_id,
            'data': df,
            'validation': validation_result,
            'summary': summary
        }

    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> Dict:
        """Validate required columns exist and are formatted correctly"""
        errors = []
        warnings = []

        # Check required columns
        missing_cols = [col for col in DataUploadHandler.REQUIRED_COLUMNS
                       if col not in df.columns]
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")

        # Check for nulls in required columns
        for col in DataUploadHandler.REQUIRED_COLUMNS:
            if col in df.columns and df[col].isnull().any():
                null_count = df[col].isnull().sum()
                errors.append(f"Column '{col}' has {null_count} null values")

        # Validate timestamp format
        if 'event_timestamp' in df.columns:
            try:
                df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
            except Exception as e:
                errors.append(f"Invalid timestamp format: {str(e)}")

        # Check minimum data requirements
        if len(df) < 100:
            errors.append(f"Insufficient data: {len(df)} events (minimum 100)")

        unique_users = df['user_id'].nunique() if 'user_id' in df.columns else 0
        if unique_users < 10:
            errors.append(f"Insufficient users: {unique_users} (minimum 10)")

        # Warnings for optional columns
        optional_cols = ['session_duration', 'donation_amount', 'content_category']
        missing_optional = [col for col in optional_cols if col not in df.columns]
        if missing_optional:
            warnings.append(f"Optional columns missing (may reduce accuracy): {missing_optional}")

        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    @staticmethod
    def _create_summary(df: pd.DataFrame) -> Dict:
        """Generate summary statistics"""
        return {
            'total_events': int(len(df)),
            'unique_users': int(df['user_id'].nunique()),
            'date_range': [
                df['event_timestamp'].min().isoformat(),
                df['event_timestamp'].max().isoformat()
            ],
            'event_types': df['event_type'].unique().tolist()
        }
