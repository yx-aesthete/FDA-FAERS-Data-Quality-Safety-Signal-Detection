"""
FDA FAERS Safety Signal Detection Demo

This demo showcases AI/ML-based safety signal detection techniques
for pharmacovigilance - a critical capability for patient safety monitoring.

Key Features:
- Disproportionality analysis (PRR, ROR)
- Drug-event association mining
- Serious outcome prediction
- Temporal signal detection
- ML-based signal prioritization
"""

import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


class SafetySignalDetector:
    """
    Safety Signal Detection System for FAERS data
    Implements statistical and ML-based signal detection methods
    """
    
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.demo_df = None
        self.drug_df = None
        self.reac_df = None
        self.outc_df = None
        self.signals = []
        
    def load_data(self, sample_size: int = 100000):
        """Load FAERS data files"""
        print("📥 Loading FAERS Data for Signal Detection...")
        
        # Load all necessary tables
        self.demo_df = pd.read_csv(
            self.data_path / 'ASCII/DEMO25Q3.txt',
            sep='$',
            encoding='latin1',
            nrows=sample_size,
            low_memory=False
        )
        
        self.reac_df = pd.read_csv(
            self.data_path / 'ASCII/REAC25Q3.txt',
            sep='$',
            encoding='latin1',
            low_memory=False
        )
        
        self.drug_df = pd.read_csv(
            self.data_path / 'ASCII/DRUG25Q3.txt',
            sep='$',
            encoding='latin1',
            low_memory=False
        )
        
        self.outc_df = pd.read_csv(
            self.data_path / 'ASCII/OUTC25Q3.txt',
            sep='$',
            encoding='latin1',
            low_memory=False
        )
        
        print(f"✅ Loaded data:")
        print(f"   - {len(self.demo_df):,} cases")
        print(f"   - {len(self.drug_df):,} drug records")
        print(f"   - {len(self.reac_df):,} reactions")
        print(f"   - {len(self.outc_df):,} outcomes")
        print()
        
    def calculate_prr(self, min_cases: int = 3):
        """
        Calculate Proportional Reporting Ratio (PRR)
        Standard method for signal detection in pharmacovigilance
        
        PRR = (a/b) / (c/d)
        where:
        a = reports with drug X and event Y
        b = reports with drug X and NOT event Y
        c = reports with NOT drug X and event Y
        d = reports with NOT drug X and NOT event Y
        """
        print("🔍 Calculating Proportional Reporting Ratios (PRR)...")
        
        # Merge drug and reaction data
        drug_reaction = self.drug_df.merge(
            self.reac_df,
            on=['primaryid', 'caseid'],
            how='inner'
        )
        
        # Filter for primary suspect drugs only
        drug_reaction = drug_reaction[drug_reaction['role_cod'] == 'PS']
        
        # Get top drugs and reactions for analysis
        top_drugs = drug_reaction['drugname'].value_counts().head(50).index
        top_reactions = drug_reaction['pt'].value_counts().head(100).index
        
        signals = []
        
        print(f"  Analyzing {len(top_drugs)} drugs × {len(top_reactions)} reactions...")
        
        total_cases = len(self.demo_df)
        
        for drug in top_drugs:
            for reaction in top_reactions:
                # Calculate 2x2 contingency table
                a = len(drug_reaction[
                    (drug_reaction['drugname'] == drug) & 
                    (drug_reaction['pt'] == reaction)
                ])
                
                if a < min_cases:
                    continue
                
                b = len(drug_reaction[
                    (drug_reaction['drugname'] == drug) & 
                    (drug_reaction['pt'] != reaction)
                ])
                
                c = len(drug_reaction[
                    (drug_reaction['drugname'] != drug) & 
                    (drug_reaction['pt'] == reaction)
                ])
                
                d = total_cases - a - b - c
                
                # Calculate PRR
                if b > 0 and c > 0 and d > 0:
                    prr = (a / b) / (c / d)
                    
                    # Calculate Chi-square for statistical significance
                    chi2 = total_cases * (a*d - b*c)**2 / ((a+b)*(c+d)*(a+c)*(b+d))
                    
                    # Signal criteria: PRR >= 2, chi2 >= 4, cases >= 3
                    if prr >= 2.0 and chi2 >= 4.0:
                        signals.append({
                            'drug': drug,
                            'reaction': reaction,
                            'prr': prr,
                            'chi2': chi2,
                            'cases': a,
                            'signal_strength': 'Strong' if prr >= 5 else 'Moderate'
                        })
        
        # Sort by PRR
        signals_df = pd.DataFrame(signals).sort_values('prr', ascending=False)
        
        print(f"\n  🚨 Detected {len(signals_df)} potential safety signals!")
        print(f"  📊 Signal criteria: PRR ≥ 2.0, χ² ≥ 4.0, cases ≥ {min_cases}")
        
        if len(signals_df) > 0:
            print("\n  🔝 Top 10 Strongest Signals:")
            print()
            for idx, row in signals_df.head(10).iterrows():
                print(f"    {row['signal_strength']:8s} | {row['drug'][:30]:30s} → {row['reaction'][:30]:30s}")
                print(f"              PRR: {row['prr']:6.2f} | χ²: {row['chi2']:8.2f} | Cases: {row['cases']:4.0f}")
                print()
        
        self.signals = signals_df
        return signals_df
    
    def identify_serious_outcomes(self):
        """
        Identify cases with serious outcomes
        Critical for prioritizing safety review
        """
        print("\n⚠️  Analyzing Serious Outcomes...")
        
        # Merge outcomes with demo data
        cases_with_outcomes = self.demo_df.merge(
            self.outc_df,
            on=['primaryid', 'caseid'],
            how='left'
        )
        
        # Define serious outcome codes
        serious_codes = {
            'DE': 'Death',
            'LT': 'Life-Threatening',
            'HO': 'Hospitalization',
            'DS': 'Disability',
            'CA': 'Congenital Anomaly',
            'RI': 'Required Intervention'
        }
        
        # Count serious outcomes
        serious_counts = {}
        for code, description in serious_codes.items():
            count = (cases_with_outcomes['outc_cod'] == code).sum()
            serious_counts[description] = count
        
        total_serious = cases_with_outcomes['outc_cod'].isin(serious_codes.keys()).sum()
        
        print(f"  📊 Total cases with serious outcomes: {total_serious:,}")
        print(f"  📊 Serious outcome rate: {(total_serious/len(cases_with_outcomes)*100):.2f}%")
        print("\n  Breakdown by outcome type:")
        for outcome, count in sorted(serious_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                pct = (count / len(cases_with_outcomes) * 100)
                print(f"    {outcome:25s}: {count:6,} ({pct:5.2f}%)")
        
        return cases_with_outcomes, serious_counts
    
    def temporal_signal_analysis(self):
        """
        Analyze temporal trends in adverse event reporting
        Can detect emerging safety signals
        """
        print("\n📈 Temporal Signal Analysis...")
        
        # Parse dates
        self.demo_df['fda_dt_parsed'] = pd.to_datetime(
            self.demo_df['fda_dt'],
            format='%Y%m%d',
            errors='coerce'
        )
        
        # Monthly aggregation
        monthly = self.demo_df.groupby(
            self.demo_df['fda_dt_parsed'].dt.to_period('M')
        ).size().reset_index(name='count')
        
        monthly.columns = ['month', 'count']
        monthly['month'] = monthly['month'].astype(str)
        
        # Calculate growth rates
        monthly['growth_rate'] = monthly['count'].pct_change() * 100
        
        print(f"  📅 Analysis period: {monthly['month'].min()} to {monthly['month'].max()}")
        print(f"  📊 Average monthly reports: {monthly['count'].mean():.0f}")
        
        # Identify months with unusual growth
        unusual_growth = monthly[abs(monthly['growth_rate']) > 50]
        
        if len(unusual_growth) > 0:
            print(f"\n  🚨 Months with unusual growth (>50% change):")
            for idx, row in unusual_growth.iterrows():
                direction = "📈" if row['growth_rate'] > 0 else "📉"
                print(f"    {direction} {row['month']}: {row['growth_rate']:+.1f}% ({row['count']:,} reports)")
        
        return monthly
    
    def drug_class_analysis(self):
        """
        Analyze adverse events by drug characteristics
        Useful for identifying class-wide safety issues
        """
        print("\n💊 Drug Class Analysis...")
        
        # Get most reported drugs
        top_drugs = self.drug_df[
            self.drug_df['role_cod'] == 'PS'
        ]['drugname'].value_counts().head(20)
        
        print(f"  🔝 Top 20 Most Reported Drugs:")
        print()
        for idx, (drug, count) in enumerate(top_drugs.items(), 1):
            print(f"    {idx:2d}. {drug[:50]:50s} : {count:6,} reports")
        
        # Get reactions associated with top drugs
        print(f"\n  Analyzing reaction patterns for top drugs...")
        
        drug_reactions = self.drug_df.merge(
            self.reac_df,
            on=['primaryid', 'caseid'],
            how='inner'
        )
        
        drug_reactions = drug_reactions[drug_reactions['role_cod'] == 'PS']
        
        return top_drugs, drug_reactions
    
    def predict_serious_outcome_risk(self):
        """
        ML-based prediction of serious outcome risk
        Demonstrates predictive analytics for case prioritization
        """
        print("\n🤖 ML-Based Serious Outcome Risk Prediction...")
        
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report, roc_auc_score
        
        # Merge data for feature engineering
        cases_with_outcomes = self.demo_df.merge(
            self.outc_df,
            on=['primaryid', 'caseid'],
            how='left'
        )
        
        # Define serious outcome
        serious_codes = ['DE', 'LT', 'HO', 'DS', 'CA', 'RI']
        cases_with_outcomes['serious'] = cases_with_outcomes['outc_cod'].isin(serious_codes).astype(int)
        
        # Feature engineering
        features = pd.DataFrame()
        
        # Age-based features
        features['age'] = cases_with_outcomes['age'].fillna(cases_with_outcomes['age'].median())
        features['age_unknown'] = cases_with_outcomes['age'].isna().astype(int)
        features['age_elderly'] = (features['age'] >= 65).astype(int)
        features['age_pediatric'] = (features['age'] < 18).astype(int)
        
        # Sex
        features['sex_male'] = (cases_with_outcomes['sex'] == 'M').astype(int)
        features['sex_female'] = (cases_with_outcomes['sex'] == 'F').astype(int)
        
        # Reporter type
        features['reporter_md'] = (cases_with_outcomes['occp_cod'] == 'MD').astype(int)
        features['reporter_pharm'] = (cases_with_outcomes['occp_cod'] == 'PH').astype(int)
        
        # Report source
        features['expedited'] = (cases_with_outcomes['rept_cod'] == 'EXP').astype(int)
        
        # Target
        y = cases_with_outcomes['serious']
        
        # Remove rows with missing target
        valid_mask = y.notna()
        features = features[valid_mask]
        y = y[valid_mask]
        
        if len(features) > 100 and y.sum() > 10:
            # Train/test split
            X_train, X_test, y_train, y_test = train_test_split(
                features, y, test_size=0.3, random_state=42, stratify=y
            )
            
            # Train model
            print("  🔧 Training Random Forest classifier...")
            rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            rf.fit(X_train, y_train)
            
            # Evaluate
            y_pred = rf.predict(X_test)
            y_proba = rf.predict_proba(X_test)[:, 1]
            
            auc = roc_auc_score(y_test, y_proba)
            
            print(f"\n  📊 Model Performance:")
            print(f"    - ROC-AUC Score: {auc:.3f}")
            print(f"    - Accuracy: {(y_pred == y_test).mean():.3f}")
            
            # Feature importance
            importance = pd.DataFrame({
                'feature': features.columns,
                'importance': rf.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n  🎯 Top Predictive Features:")
            for idx, row in importance.head(5).iterrows():
                print(f"    {row['feature']:20s}: {row['importance']:.3f}")
            
            print("\n  💡 Use case: Automatically flag high-risk cases for priority review")
            
            return rf, features, y
        else:
            print("  ⚠️  Insufficient data for ML model training in sample")
            return None, None, None
    
    def generate_signal_report(self):
        """Generate comprehensive safety signal report"""
        print("\n" + "="*70)
        print("🚨 FDA FAERS SAFETY SIGNAL DETECTION REPORT - Q3 2025")
        print("="*70)
        
        # Run all analyses
        signals = self.calculate_prr()
        outcomes = self.identify_serious_outcomes()
        temporal = self.temporal_signal_analysis()
        drug_analysis = self.drug_class_analysis()
        ml_model = self.predict_serious_outcome_risk()
        
        print("\n" + "="*70)
        print("✅ SIGNAL DETECTION COMPLETE")
        print("="*70)
        
        print(f"\n📊 Summary:")
        print(f"  - Safety signals detected: {len(signals) if len(signals) > 0 else 0}")
        print(f"  - Cases with serious outcomes: {outcomes[1].get('Death', 0) + outcomes[1].get('Life-Threatening', 0):,}")
        print(f"  - Deaths reported: {outcomes[1].get('Death', 0):,}")
        print(f"  - Unique drugs analyzed: {len(self.drug_df['drugname'].unique()):,}")
        print(f"  - Unique reactions: {len(self.reac_df['pt'].unique()):,}")
        
        return {
            'signals': signals,
            'outcomes': outcomes,
            'temporal': temporal,
            'drugs': drug_analysis,
            'ml': ml_model
        }


def main():
    """Main execution function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   FDA FAERS Safety Signal Detection System - PoC         ║
    ║                                                           ║
    ║   AI/ML-based pharmacovigilance signal detection         ║
    ║   for patient safety monitoring                          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize detector
    data_path = Path(__file__).parent.parent / 'data'
    detector = SafetySignalDetector(data_path)
    
    # Load data
    detector.load_data(sample_size=100000)
    
    # Generate comprehensive report
    report = detector.generate_signal_report()
    
    print("\n💡 Production Implementation:")
    print("  1. Real-time signal detection pipeline")
    print("  2. Integration with safety database")
    print("  3. Automated alert routing to safety teams")
    print("  4. Interactive signal review dashboard")
    print("  5. ML model for signal prioritization")
    print("  6. Regulatory reporting automation")
    
    print("\n🎯 Demo Complete!")


if __name__ == "__main__":
    main()
