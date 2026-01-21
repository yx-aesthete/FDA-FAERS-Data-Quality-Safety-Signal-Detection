"""
FDA FAERS Data Quality Surveillance Demo

This demo showcases AI-driven data quality monitoring techniques
relevant to the DART program's data surveillance workstream.

Key Features:
- Automated data completeness scoring
- Anomaly detection in reporting patterns
- Duplicate detection algorithms
- Missing data profiling
- Data quality dashboards
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class FAERSDataQualityMonitor:
    """
    Data Quality Monitoring System for FAERS data
    Implements the 'immune system' concept for continuous data surveillance
    """
    
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.demo_df = None
        self.drug_df = None
        self.reac_df = None
        self.quality_scores = {}
        
    def load_data(self, sample_size: int = 50000):
        """Load FAERS data files"""
        print("📥 Loading FAERS Q3 2025 Data...")
        
        # Load demographics (main table)
        self.demo_df = pd.read_csv(
            self.data_path / 'ASCII/DEMO25Q3.txt',
            sep='$',
            encoding='latin1',
            nrows=sample_size,
            low_memory=False
        )
        
        # Load reactions
        self.reac_df = pd.read_csv(
            self.data_path / 'ASCII/REAC25Q3.txt',
            sep='$',
            encoding='latin1',
            low_memory=False
        )
        
        # Load drugs
        self.drug_df = pd.read_csv(
            self.data_path / 'ASCII/DRUG25Q3.txt',
            sep='$',
            encoding='latin1',
            low_memory=False
        )
        
        print(f"✅ Loaded {len(self.demo_df):,} cases")
        print(f"   - {len(self.reac_df):,} adverse reactions")
        print(f"   - {len(self.drug_df):,} drug records")
        print()
        
    def calculate_completeness_score(self):
        """
        Calculate data completeness score for critical fields
        This is a key data quality metric for regulatory compliance
        """
        print("🔍 Calculating Data Completeness Scores...")
        
        critical_fields = {
            'Case ID': 'caseid',
            'FDA Receipt Date': 'fda_dt',
            'Event Date': 'event_dt',
            'Age': 'age',
            'Sex': 'sex',
            'Reporter Country': 'reporter_country',
            'Report Code': 'rept_cod'
        }
        
        completeness = {}
        for name, col in critical_fields.items():
            if col in self.demo_df.columns:
                non_null = self.demo_df[col].notna().sum()
                total = len(self.demo_df)
                completeness[name] = (non_null / total) * 100
        
        # Overall score
        overall_score = np.mean(list(completeness.values()))
        
        print("\n📊 Field Completeness:")
        for field, score in completeness.items():
            status = "✅" if score > 90 else "⚠️" if score > 70 else "❌"
            print(f"  {status} {field:20s}: {score:6.2f}%")
        
        print(f"\n🎯 Overall Completeness Score: {overall_score:.2f}%")
        
        self.quality_scores['completeness'] = overall_score
        return completeness
    
    def detect_duplicates(self):
        """
        Detect potential duplicate reports
        Critical for data quality as duplicates can skew safety signals
        """
        print("\n🔎 Detecting Duplicate Cases...")
        
        # Check for exact case ID duplicates
        duplicate_cases = self.demo_df[self.demo_df.duplicated(subset=['caseid'], keep=False)]
        
        # Check for potential duplicates based on multiple criteria
        potential_dupes = self.demo_df[
            self.demo_df.duplicated(
                subset=['age', 'sex', 'event_dt', 'reporter_country'],
                keep=False
            ) & 
            self.demo_df['age'].notna()
        ]
        
        print(f"  📋 Exact duplicates (case ID): {len(duplicate_cases):,} records")
        print(f"  🔍 Potential duplicates: {len(potential_dupes):,} records")
        print(f"  📊 Duplicate rate: {(len(duplicate_cases)/len(self.demo_df)*100):.2f}%")
        
        return duplicate_cases, potential_dupes
    
    def detect_anomalies_in_reporting_patterns(self):
        """
        Detect anomalies in temporal reporting patterns
        Uses statistical methods to identify unusual spikes or drops
        """
        print("\n📈 Analyzing Temporal Reporting Patterns...")
        
        # Convert FDA receipt date to datetime
        self.demo_df['fda_dt_parsed'] = pd.to_datetime(
            self.demo_df['fda_dt'],
            format='%Y%m%d',
            errors='coerce'
        )
        
        # Daily report counts
        daily_counts = self.demo_df.groupby(
            self.demo_df['fda_dt_parsed'].dt.date
        ).size().reset_index(name='count')
        
        # Calculate Z-scores for anomaly detection
        mean_count = daily_counts['count'].mean()
        std_count = daily_counts['count'].std()
        daily_counts['z_score'] = (daily_counts['count'] - mean_count) / std_count
        
        # Identify anomalies (|Z| > 3)
        anomalies = daily_counts[abs(daily_counts['z_score']) > 3]
        
        print(f"  📅 Date range: {daily_counts.iloc[0, 0]} to {daily_counts.iloc[-1, 0]}")
        print(f"  📊 Average daily reports: {mean_count:.0f} ± {std_count:.0f}")
        print(f"  🚨 Anomalous days detected: {len(anomalies)}")
        
        if len(anomalies) > 0:
            print("\n  Top 3 anomalous days:")
            for idx, row in anomalies.nlargest(3, 'count').iterrows():
                print(f"    - {row.iloc[0]}: {row['count']:,} reports (Z={row['z_score']:.2f})")
        
        return daily_counts, anomalies
    
    def profile_missing_data_patterns(self):
        """
        Analyze patterns in missing data
        Helps identify systematic data entry issues
        """
        print("\n🔍 Profiling Missing Data Patterns...")
        
        # Calculate missing percentages
        missing_stats = pd.DataFrame({
            'column': self.demo_df.columns,
            'missing_count': [self.demo_df[col].isna().sum() for col in self.demo_df.columns],
            'missing_pct': [(self.demo_df[col].isna().sum() / len(self.demo_df) * 100) 
                           for col in self.demo_df.columns]
        })
        
        missing_stats = missing_stats[missing_stats['missing_pct'] > 0].sort_values(
            'missing_pct', 
            ascending=False
        )
        
        print("\n  📊 Top 10 fields with missing data:")
        for idx, row in missing_stats.head(10).iterrows():
            print(f"    {row['column']:20s}: {row['missing_pct']:6.2f}% ({row['missing_count']:,} records)")
        
        return missing_stats
    
    def calculate_case_quality_score(self):
        """
        Calculate individual case quality scores
        This can be used for prioritization and automated review
        """
        print("\n⭐ Calculating Individual Case Quality Scores...")
        
        # Quality scoring criteria
        scores = pd.DataFrame(index=self.demo_df.index)
        
        # Completeness (40 points)
        critical_fields = ['caseid', 'fda_dt', 'age', 'sex', 'reporter_country']
        scores['completeness'] = self.demo_df[critical_fields].notna().sum(axis=1) / len(critical_fields) * 40
        
        # Age validity (20 points)
        scores['age_valid'] = 20
        scores.loc[self.demo_df['age'].isna(), 'age_valid'] = 0
        scores.loc[self.demo_df['age'] > 120, 'age_valid'] = 0
        
        # Date consistency (20 points)
        scores['date_valid'] = 20
        # Could add more sophisticated date validation here
        
        # Reporter info (20 points)
        scores['reporter_info'] = (
            self.demo_df['reporter_country'].notna().astype(int) * 10 +
            self.demo_df['occp_cod'].notna().astype(int) * 10
        )
        
        # Total score
        scores['total_score'] = scores.sum(axis=1)
        
        # Add to demo_df
        self.demo_df['quality_score'] = scores['total_score']
        
        # Summary statistics
        print(f"  📊 Mean Quality Score: {scores['total_score'].mean():.2f}/100")
        print(f"  📊 Median Quality Score: {scores['total_score'].median():.2f}/100")
        print(f"  ⚠️  Low quality cases (<50): {(scores['total_score'] < 50).sum():,} ({(scores['total_score'] < 50).sum()/len(scores)*100:.2f}%)")
        print(f"  ✅ High quality cases (>80): {(scores['total_score'] > 80).sum():,} ({(scores['total_score'] > 80).sum()/len(scores)*100:.2f}%)")
        
        return scores
    
    def identify_data_entry_issues(self):
        """
        Identify potential data entry issues using pattern analysis
        """
        print("\n🔧 Identifying Potential Data Entry Issues...")
        
        issues = []
        
        # Issue 1: Invalid age values
        invalid_ages = self.demo_df[
            (self.demo_df['age'].notna()) & 
            ((self.demo_df['age'] < 0) | (self.demo_df['age'] > 120))
        ]
        if len(invalid_ages) > 0:
            issues.append(f"Invalid ages: {len(invalid_ages)} cases")
        
        # Issue 2: Future dates
        current_date = datetime.now()
        self.demo_df['fda_dt_parsed'] = pd.to_datetime(
            self.demo_df['fda_dt'],
            format='%Y%m%d',
            errors='coerce'
        )
        future_dates = self.demo_df[
            self.demo_df['fda_dt_parsed'] > current_date
        ]
        if len(future_dates) > 0:
            issues.append(f"Future FDA receipt dates: {len(future_dates)} cases")
        
        # Issue 3: Missing critical identifiers
        missing_ids = self.demo_df[self.demo_df['caseid'].isna()]
        if len(missing_ids) > 0:
            issues.append(f"Missing case IDs: {len(missing_ids)} cases")
        
        print(f"  🚨 Total issues identified: {len(issues)}")
        for issue in issues:
            print(f"    - {issue}")
        
        return issues
    
    def generate_quality_report(self):
        """Generate comprehensive data quality report"""
        print("\n" + "="*60)
        print("📋 FDA FAERS DATA QUALITY REPORT - Q3 2025")
        print("="*60)
        
        # Run all checks
        completeness = self.calculate_completeness_score()
        duplicates = self.detect_duplicates()
        temporal_analysis = self.detect_anomalies_in_reporting_patterns()
        missing_profile = self.profile_missing_data_patterns()
        quality_scores = self.calculate_case_quality_score()
        issues = self.identify_data_entry_issues()
        
        print("\n" + "="*60)
        print("✅ QUALITY REPORT COMPLETE")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  - Overall Completeness: {self.quality_scores.get('completeness', 0):.2f}%")
        print(f"  - Duplicate Rate: {(len(duplicates[0])/len(self.demo_df)*100):.2f}%")
        print(f"  - Data Entry Issues: {len(issues)}")
        print(f"  - Average Case Quality: {self.demo_df['quality_score'].mean():.2f}/100")
        
        return {
            'completeness': completeness,
            'duplicates': duplicates,
            'temporal': temporal_analysis,
            'missing': missing_profile,
            'scores': quality_scores,
            'issues': issues
        }


def main():
    """Main execution function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   FDA FAERS Data Quality Surveillance System - PoC       ║
    ║                                                           ║
    ║   Demonstration of AI-driven data quality monitoring     ║
    ║   for Pharmacovigilance data (DART Program)              ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize monitor
    data_path = Path(__file__).parent.parent / 'data'
    monitor = FAERSDataQualityMonitor(data_path)
    
    # Load data
    monitor.load_data(sample_size=50000)  # Use 50k records for demo
    
    # Generate comprehensive report
    report = monitor.generate_quality_report()
    
    print("\n💡 Next Steps for Production:")
    print("  1. Deploy as real-time monitoring service")
    print("  2. Integrate with alerting system (CloudWatch/PagerDuty)")
    print("  3. Add ML-based anomaly detection models")
    print("  4. Implement automated data remediation workflows")
    print("  5. Create interactive dashboard (Streamlit/Dash)")
    
    print("\n🎯 Demo Complete!")


if __name__ == "__main__":
    main()
