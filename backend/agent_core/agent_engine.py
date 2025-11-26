import pandas as pd
import numpy as np
import json
import os
from django.conf import settings
from .models import CleaningJob, AnalysisReport
import re

class SemanticAnalyzer:
    """
    Simulates LLM-based semantic analysis using regex and heuristics.
    In a real-world scenario, this would call an LLM API (OpenAI/Gemini).
    """
    def __init__(self):
        self.pii_patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}',
            'ssn': r'\d{3}-\d{2}-\d{4}',
            'credit_card': r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}'
        }

    def analyze_column(self, series):
        """Infer column type and check for PII."""
        sample = series.dropna().astype(str).head(100)
        if sample.empty:
            return "empty", False

        # Check for PII
        for pii_type, pattern in self.pii_patterns.items():
            matches = sample.str.match(pattern).sum()
            if matches > 0.5 * len(sample): # If > 50% match pattern
                return pii_type, True
        
        return "text", False

    def detect_issues(self, df):
        issues = {}
        pii_columns = []
        
        for col in df.columns:
            col_type, is_pii = self.analyze_column(df[col])
            if is_pii:
                pii_columns.append(f"{col} ({col_type})")
        
        if pii_columns:
            issues['pii_detected'] = pii_columns
            
        return issues

class UDAQAgent:
    def __init__(self, job_id):
        self.job_id = job_id
        
    def run(self):
        try:
            job = CleaningJob.objects.get(id=self.job_id)
            job.status = 'RUNNING'
            job.save()
            job.add_log("Agent started. Loading dataset...")
            
            file_path = job.dataset.file.path
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file format")
            except Exception as e:
                job.status = 'FAILED'
                job.add_log(f"Error loading file: {str(e)}")
                job.save()
                return

            job.add_log(f"Dataset loaded. Shape: {df.shape}")
            
            # 1. Initial Evaluation
            initial_score, initial_issues = self.evaluate_quality(df)
            job.add_log(f"Initial Quality Score: {initial_score}/100")
            job.add_log(f"Issues detected: {list(initial_issues.keys())}")
            
            # 2. Fix Issues (Reasoning Loop Simulation)
            actions_taken = []
            df_clean = df.copy()
            
            # Priority 1: Structure & Types
            if 'inconsistent_types' in initial_issues:
                job.add_log("Plan: Fix inconsistent types (converting to numeric where applicable).")
                df_clean = self.fix_inconsistent_types(df_clean)
                actions_taken.append("Fixed inconsistent types")

            # Priority 2: Data Cleaning
            if 'missing_values' in initial_issues:
                job.add_log("Plan: Fix missing values using mean/mode imputation.")
                df_clean = self.fix_missing_values(df_clean)
                actions_taken.append("Imputed missing values")
                
            if 'duplicates' in initial_issues:
                job.add_log("Plan: Remove duplicate rows.")
                df_clean = self.fix_duplicates(df_clean)
                actions_taken.append("Removed duplicates")

            if 'rare_categories' in initial_issues:
                job.add_log("Plan: Group rare categories into 'Other'.")
                df_clean = self.fix_rare_categories(df_clean)
                actions_taken.append("Grouped rare categories")

            # Priority 3: Advanced Analysis
            if 'data_leakage' in initial_issues:
                job.add_log("Plan: Remove highly correlated features (potential leakage).")
                df_clean = self.fix_leakage(df_clean)
                actions_taken.append("Removed correlated features")

            if 'pii_detected' in initial_issues:
                job.add_log(f"Plan: Flagged PII columns: {initial_issues['pii_detected']}. (Action: Anonymizing/Hashing in future updates)")
                # For now, we just log it, but we could drop or hash them.
                actions_taken.append("Detected PII (Flagged)")
                
            # 3. Final Evaluation
            final_score, final_issues = self.evaluate_quality(df_clean)
            job.add_log(f"Final Quality Score: {final_score}/100")
            
            # 4. Save Cleaned File
            cleaned_filename = f"cleaned_{os.path.basename(file_path)}"
            cleaned_path = os.path.join(settings.MEDIA_ROOT, 'cleaned', cleaned_filename)
            os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
            
            if file_path.endswith('.csv'):
                df_clean.to_csv(cleaned_path, index=False)
            else:
                df_clean.to_excel(cleaned_path, index=False)
                
            # 5. Create Report
            AnalysisReport.objects.create(
                job=job,
                initial_quality_score=initial_score,
                final_quality_score=final_score,
                issues_found=initial_issues,
                actions_taken=actions_taken,
                cleaned_file_path=cleaned_path
            )
            
            job.status = 'COMPLETED'
            job.add_log("Job completed successfully.")
            job.save()
            
        except Exception as e:
            print(f"Agent Error: {e}")
            # Re-fetch job to ensure we have latest state
            job = CleaningJob.objects.get(id=self.job_id)
            job.status = 'FAILED'
            job.add_log(f"Critical Error: {str(e)}")
            job.save()

    def evaluate_quality(self, df):
        issues = {}
        score = 100
        
        # 1. Missing Values
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            issues['missing_values'] = int(missing_count)
            score -= 15
            
        # 2. Duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            issues['duplicates'] = int(dup_count)
            score -= 15
            
        # 3. Inconsistent Types (Heuristic: Object columns that look numeric)
        inconsistent_cols = 0
        for col in df.select_dtypes(include=['object']):
            # Try converting to numeric, if > 80% success, it's likely inconsistent
            numeric_conversion = pd.to_numeric(df[col], errors='coerce')
            success_rate = numeric_conversion.notnull().mean()
            if 0.5 < success_rate < 1.0: # If mixed (some numbers, some strings)
                inconsistent_cols += 1
        
        if inconsistent_cols > 0:
            issues['inconsistent_types'] = int(inconsistent_cols)
            score -= 10

        # 4. Rare Categories (Typos)
        rare_cats = 0
        for col in df.select_dtypes(include=['object']):
            counts = df[col].value_counts(normalize=True)
            # If categories exist with < 1% frequency and there are many categories
            if (counts < 0.01).any() and len(counts) > 5:
                rare_cats += 1
        
        if rare_cats > 0:
            issues['rare_categories'] = int(rare_cats)
            score -= 10

        # 5. Data Leakage (High Correlation)
        # Only check numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] > 1:
            corr_matrix = numeric_df.corr().abs()
            # Select upper triangle of correlation matrix
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            # Find index of feature columns with correlation greater than 0.98
            to_drop = [column for column in upper.columns if any(upper[column] > 0.98)]
            if len(to_drop) > 0:
                issues['data_leakage'] = len(to_drop)
                score -= 10

        # 6. Outliers
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outliers = 0
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outlier_mask = (df[col] < (q1 - 1.5 * iqr)) | (df[col] > (q3 + 1.5 * iqr))
            outliers += outlier_mask.sum()
            
        if outliers > 0:
            issues['outliers'] = int(outliers)
            score -= 10

        # 7. Semantic Analysis (LLM Simulation)
        analyzer = SemanticAnalyzer()
        semantic_issues = analyzer.detect_issues(df)
        if 'pii_detected' in semantic_issues:
            issues['pii_detected'] = len(semantic_issues['pii_detected'])
            score -= 10 # Penalty for exposing PII
            
        return max(0, score), issues

    def fix_missing_values(self, df):
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col].fillna(df[col].mean(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown", inplace=True)
        return df

    def fix_duplicates(self, df):
        return df.drop_duplicates()

    def fix_inconsistent_types(self, df):
        for col in df.select_dtypes(include=['object']):
            numeric_conversion = pd.to_numeric(df[col], errors='coerce')
            success_rate = numeric_conversion.notnull().mean()
            if 0.5 < success_rate < 1.0:
                # Convert to numeric, invalid values become NaN (which will be fixed by fix_missing_values)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def fix_rare_categories(self, df):
        for col in df.select_dtypes(include=['object']):
            counts = df[col].value_counts(normalize=True)
            rare_labels = counts[counts < 0.01].index
            if len(rare_labels) > 0:
                df[col] = df[col].replace(rare_labels, 'Other')
        return df

    def fix_leakage(self, df):
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] > 1:
            corr_matrix = numeric_df.corr().abs()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            to_drop = [column for column in upper.columns if any(upper[column] > 0.98)]
            df.drop(columns=to_drop, inplace=True)
        return df
