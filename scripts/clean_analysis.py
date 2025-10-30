"""
Clean Analysis for Nigerian MCH Research Limitations Scoping Review
Complete analysis script with all findings.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Load and clean the dataset"""
    df = pd.read_csv('data/raw/Extracted_data_v1.csv')
    
    # Basic cleaning
    df['Year'] = df['Year of publication']
    
    # Clean topic area
    df['Primary_topic'] = df['Topic area'].str.split(';').str[0].str.strip()
    
    # Clean funding
    df['Funding_clean'] = df['Funding sources'].fillna('Not reported')
    
    # Clean region
    def clean_region(region):
        if pd.isna(region): return 'Not specified'
        region_str = str(region).lower()
        if 'north' in region_str: return 'North'
        elif 'south' in region_str: return 'South'
        elif 'national' in region_str: return 'National'
        else: return 'Not specified'
    
    df['Region_clean'] = df['Region'].apply(clean_region)

        # Clean urban-rural data
    def clean_urban_rural(value):
        if pd.isna(value):
            return 'Not specified'
        value_str = str(value).lower()
        if 'urban' in value_str:
            return 'Urban'
        elif 'rural' in value_str:
            return 'Rural'
        elif 'both' in value_str:
            return 'Both'
        else:
            return 'Not specified'

    df['Urban_Rural_clean'] = df['Urban–Rural'].apply(clean_urban_rural)
    
        # Clean multi-site data
    def clean_multi_site(value):
        if pd.isna(value):
            return 'Not reported'
        value_str = str(value).strip().lower()
        if value_str == 'yes':
            return 'Yes'
        elif value_str == 'no':
            return 'No'
        else:
            return 'Not reported'
    
    df['Multi_site_clean'] = df['Multi-site study '].apply(clean_multi_site)

    # Define limitation columns
    limitation_columns = [
        '-- SAMPLING & DESIGN --',
        '-- MEASUREMENT & DATA --', 
        '-- CONTEXT & LOGISTICS --',
        '-- ANALYSIS & GENERALIZABILITY --',
        '-- RESEARCH CAPACITY --'
    ]
    
    return df, limitation_columns

def analyze_limitation_categories(df, limitation_columns):
    """Analyze broad limitation categories"""
    print("=== 1. BROAD LIMITATION CATEGORIES ===")
    
    limitation_summary = {}
    for col in limitation_columns:
        count = df[col].notna().sum()
        percentage = (count / len(df)) * 100
        limitation_summary[col] = {'count': count, 'percentage': percentage}
    
    summary_df = pd.DataFrame(limitation_summary).T
    summary_df = summary_df.sort_values('percentage', ascending=False)
    
    print("Most common limitation categories:")
    print(summary_df)
    
    # Visualization
    plt.figure(figsize=(10, 6))
    clean_names = {
        '-- SAMPLING & DESIGN --': 'Sampling & Design',
        '-- MEASUREMENT & DATA --': 'Measurement & Data', 
        '-- ANALYSIS & GENERALIZABILITY --': 'Analysis & Generalizability',
        '-- CONTEXT & LOGISTICS --': 'Context & Logistics',
        '-- RESEARCH CAPACITY --': 'Research Capacity'
    }
    
    plot_data = summary_df.copy()
    plot_data.index = plot_data.index.map(clean_names)
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    bars = plt.barh(plot_data.index, plot_data['percentage'], color=colors)
    
    plt.xlabel('Percentage of Studies Reporting (%)')
    plt.title('Most Common Limitation Categories in Nigerian MCH Research\n(2014-2024, n=228 studies)')
    plt.xlim(0, 100)
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                 ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/01_limitation_categories.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return summary_df

def analyze_specific_limitations(df, limitation_columns):
    """Analyze specific limitation codes"""
    print("\n=== 2. SPECIFIC LIMITATION CODES ===")
    
    limitation_counts = {}
    
    for col in limitation_columns:
        non_null_data = df[col].dropna()
        for value in non_null_data:
            codes = [code.strip() for code in str(value).split(';')]
            for code in codes:
                code_key = code.split(':')[0].strip() if ':' in code else code.strip()
                if code_key in limitation_counts:
                    limitation_counts[code_key] += 1
                else:
                    limitation_counts[code_key] = 1
    
    limitations_df = pd.DataFrame.from_dict(limitation_counts, orient='index', columns=['Count'])
    limitations_df['Percentage'] = (limitations_df['Count'] / len(df)) * 100
    limitations_df = limitations_df.sort_values('Count', ascending=False)
    
    print("Top 10 specific limitations:")
    print(limitations_df.head(10))
    
    return limitations_df

def analyze_facility_vs_community(df, limitation_columns):
    """Compare methodological vs contextual limitations between facility and community studies"""
    print("\n=== 3. FACILITY vs COMMUNITY-BASED STUDIES ===")
    
    # Clean study setting data
    setting_counts = df['Study setting'].value_counts()
    print("Study setting distribution:")
    print(setting_counts)
    
    facility_studies = df[df['Study setting'] == 'Facility-based']
    community_studies = df[df['Study setting'] == 'Community-based']
    
    print(f"\nFacility-based studies: {len(facility_studies)}")
    print(f"Community-based studies: {len(community_studies)}")
    
    # Define methodological vs contextual categories
    methodological_columns = [
        '-- SAMPLING & DESIGN --',
        '-- MEASUREMENT & DATA --', 
        '-- ANALYSIS & GENERALIZABILITY --'
    ]
    
    contextual_columns = [
        '-- CONTEXT & LOGISTICS --',
        '-- RESEARCH CAPACITY --'
    ]
    
    # Calculate percentages for each category
    comparison_data = []
    
    for setting_name, setting_studies in [('Facility', facility_studies), ('Community', community_studies)]:
        # Methodological limitations
        methodological_count = setting_studies[methodological_columns].notna().any(axis=1).sum()
        methodological_pct = (methodological_count / len(setting_studies)) * 100
        
        # Contextual limitations  
        contextual_count = setting_studies[contextual_columns].notna().any(axis=1).sum()
        contextual_pct = (contextual_count / len(setting_studies)) * 100
        
        # Total limitations reported
        total_limitations = setting_studies[limitation_columns].notna().any(axis=1).sum()
        total_pct = (total_limitations / len(setting_studies)) * 100
        
        comparison_data.append({
            'Setting': setting_name,
            'Methodological_Percentage': methodological_pct,
            'Contextual_Percentage': contextual_pct,
            'Total_Percentage': total_pct,
            'Methodological_Count': methodological_count,
            'Contextual_Count': contextual_count,
            'Total_Count': total_limitations
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nMethodological vs Contextual Limitations by Setting:")
    print(comparison_df[['Setting', 'Methodological_Percentage', 'Contextual_Percentage', 'Total_Percentage']])
    
    # Visualization - Methodological vs Contextual comparison
    plt.figure(figsize=(10, 6))
    
    settings = comparison_df['Setting']
    methodological_pct = comparison_df['Methodological_Percentage']
    contextual_pct = comparison_df['Contextual_Percentage']
    
    x = np.arange(len(settings))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, methodological_pct, width, label='Methodological Limitations', color='#1f77b4', alpha=0.8)
    bars2 = plt.bar(x + width/2, contextual_pct, width, label='Contextual Limitations', color='#ff7f0e', alpha=0.8)
    
    plt.xlabel('Study Setting')
    plt.ylabel('Percentage of Studies Reporting (%)')
    plt.title('Methodological vs Contextual Limitations:\nFacility vs Community-Based Studies')
    plt.xticks(x, settings)
    plt.legend()
    plt.ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/03_facility_vs_community.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return comparison_df

def analyze_regional_comparison(df, limitation_columns):
    """Compare methodological vs contextual limitations between Northern and Southern Nigeria"""
    print("\n=== 4. REGIONAL ANALYSIS: NORTH vs SOUTH NIGERIA ===")
    
    # Use cleaned region data
    north_studies = df[df['Region_clean'] == 'North']
    south_studies = df[df['Region_clean'] == 'South']
    
    print(f"Northern studies: {len(north_studies)}")
    print(f"Southern studies: {len(south_studies)}")
    
    # Define methodological vs contextual categories
    methodological_columns = [
        '-- SAMPLING & DESIGN --',
        '-- MEASUREMENT & DATA --', 
        '-- ANALYSIS & GENERALIZABILITY --'
    ]
    
    contextual_columns = [
        '-- CONTEXT & LOGISTICS --',
        '-- RESEARCH CAPACITY --'
    ]
    
    # Calculate percentages for each category by region
    comparison_data = []
    
    for region_name, region_studies in [('North', north_studies), ('South', south_studies)]:
        # Methodological limitations
        methodological_count = region_studies[methodological_columns].notna().any(axis=1).sum()
        methodological_pct = (methodological_count / len(region_studies)) * 100
        
        # Contextual limitations  
        contextual_count = region_studies[contextual_columns].notna().any(axis=1).sum()
        contextual_pct = (contextual_count / len(region_studies)) * 100
        
        # Total limitations reported
        total_limitations = region_studies[limitation_columns].notna().any(axis=1).sum()
        total_pct = (total_limitations / len(region_studies)) * 100
        
        comparison_data.append({
            'Region': region_name,
            'Methodological_Percentage': methodological_pct,
            'Contextual_Percentage': contextual_pct,
            'Total_Percentage': total_pct,
            'Methodological_Count': methodological_count,
            'Contextual_Count': contextual_count,
            'Total_Count': total_limitations
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nMethodological vs Contextual Limitations by Region:")
    print(comparison_df[['Region', 'Methodological_Percentage', 'Contextual_Percentage', 'Total_Percentage']])
    
    # Visualization - Methodological vs Contextual comparison by region
    plt.figure(figsize=(10, 6))
    
    regions = comparison_df['Region']
    methodological_pct = comparison_df['Methodological_Percentage']
    contextual_pct = comparison_df['Contextual_Percentage']
    
    x = np.arange(len(regions))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, methodological_pct, width, label='Methodological Limitations', color='#8B4513', alpha=0.8)
    bars2 = plt.bar(x + width/2, contextual_pct, width, label='Contextual Limitations', color='#228B22', alpha=0.8)
    
    plt.xlabel('Region')
    plt.ylabel('Percentage of Studies Reporting (%)')
    plt.title('Methodological vs Contextual Limitations:\nNorthern vs Southern Nigeria')
    plt.xticks(x, regions)
    plt.legend()
    plt.ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/04_regional_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return comparison_df

def analyze_trends_over_time(df, limitation_columns):
    print("\n=== 5. TRENDS OVER TIME (2014-2024) ===")
    
    df['Year'] = pd.to_numeric(df['Year of publication'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    
    trends_data = []
    years = sorted(df['Year'].unique())
    
    for year in years:
        year_studies = df[df['Year'] == year]
        if len(year_studies) == 0:
            continue
            
        analysis_gen_count = year_studies['-- ANALYSIS & GENERALIZABILITY --'].notna().sum()
        analysis_gen_pct = (analysis_gen_count / len(year_studies)) * 100
        
        contextual_count = year_studies['-- CONTEXT & LOGISTICS --'].notna().sum()
        contextual_pct = (contextual_count / len(year_studies)) * 100
        
        trends_data.append({
            'Year': year,
            'Analysis_Generalizability_Percentage': analysis_gen_pct,
            'Contextual_Percentage': contextual_pct,
            'Total_Studies': len(year_studies)
        })
    
    trends_df = pd.DataFrame(trends_data)
    
    print("Trends in analysis/generalizability and contextual limitations:")
    print(trends_df[['Year', 'Analysis_Generalizability_Percentage', 'Contextual_Percentage', 'Total_Studies']])
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(trends_df['Year'], trends_df['Analysis_Generalizability_Percentage'], 
             marker='o', linewidth=3, label='Analysis & Generalizability', color='#2ca02c')
    plt.plot(trends_df['Year'], trends_df['Contextual_Percentage'], 
             marker='s', linewidth=3, label='Contextual Limitations', color='#d62728')
    
    plt.xlabel('Publication Year', fontsize=12)
    plt.ylabel('Percentage of Studies Reporting (%)', fontsize=12)
    plt.title('Temporal Trends in Limitation Reporting\nNigerian MCH Research (2014-2024)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(years, rotation=45)
    plt.ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('outputs/figures/05_trends_over_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return trends_df

def analyze_contextual_limitations_trends(df, limitation_columns):
    print("Analyzing trends in contextual limitations over time...")
    """Analyze trends in contextual limitations (the under-reported ones)"""
    print("\n=== 6. CONTEXTUAL LIMITATIONS TRENDS ===")
    
    # Focus on contextual limitations
    contextual_limitations = ['FUNDING_CONSTRAINTS', 'TIME_CONSTRAINTS', 'LOGISTICAL_ISSUES', 'ETHICAL_CONSTRAINTS']
    clean_labels = {
        'FUNDING_CONSTRAINTS': 'Funding Constraints',
        'TIME_CONSTRAINTS': 'Time Constraints', 
        'LOGISTICAL_ISSUES': 'Logistical Issues',
        'ETHICAL_CONSTRAINTS': 'Ethical Constraints'
    }
    
    trend_data = []
    for limitation in contextual_limitations:
        for year in sorted(df['Year of publication'].dropna().unique()):
            year_data = df[df['Year of publication'] == year]
            total_studies = len(year_data)
            
            # Count studies reporting this contextual limitation
            count = 0
            for col in limitation_columns:
                count += year_data[col].str.contains(limitation, na=False).sum()
            
            percentage = (count / total_studies * 100) if total_studies > 0 else 0
            trend_data.append({
                'Year': year, 
                'Limitation': limitation, 
                'Percentage': percentage, 
                'Count': count, 
                'Total': total_studies
            })
    
    trend_df = pd.DataFrame(trend_data)
    
    print("Contextual limitations over time:")
    
    # Create trend visualization
    plt.figure(figsize=(12, 6))
    for limitation in contextual_limitations:
        data = trend_df[trend_df['Limitation'] == limitation]
        if len(data) > 0:  # Only plot if we have data
            plt.plot(data['Year'], data['Percentage'], marker='o', linewidth=2.5, markersize=8, 
                     label=clean_labels.get(limitation, limitation))
    
    plt.xlabel('Year')
    plt.ylabel('Percentage of Studies Reporting (%)')
    plt.title('Trends in Contextual Limitations in Nigerian MCH Research\n(Under-Reported Operational Challenges)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(sorted(df['Year of publication'].dropna().unique()))
    plt.ylim(0, 25)  # Set y-axis limit since percentages are low
    plt.tight_layout()
    plt.savefig('outputs/figures/06_contextual_limitations_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary
    print("\nContextual Limitations Summary (2014-2024):")
    for limitation in contextual_limitations:
        total_count = trend_df[trend_df['Limitation'] == limitation]['Count'].sum()
        overall_pct = (total_count / len(df)) * 100
        print(f"  {clean_labels[limitation]}: {total_count} studies ({overall_pct:.1f}%)")
    
    return trend_df

def analyze_topic_areas(df, limitation_columns):
    """Analyze distinctive limitation patterns by MCH topic area"""
    print("\n=== 7. TOPIC-SPECIFIC LIMITATION PATTERNS ===")
    
    # Get top topic areas
    topic_counts = df['Topic area'].value_counts()
    top_topics = topic_counts.head(5).index
    
    # Analyze distinctive limitations for each topic
    topic_analysis = []
    
    for topic in top_topics:
        topic_studies = df[df['Topic area'] == topic]
        other_studies = df[df['Topic area'] != topic]
        
        topic_limits = {'Topic': topic, 'N': len(topic_studies)}
        
        # Find limitations that are distinctive to this topic
        for col in limitation_columns:
            topic_pct = (topic_studies[col].notna().sum() / len(topic_studies)) * 100
            other_pct = (other_studies[col].notna().sum() / len(other_studies)) * 100
            
            # Calculate distinctiveness (how much more common in this topic)
            distinctiveness = topic_pct - other_pct
            topic_limits[col] = distinctiveness
        
        topic_analysis.append(topic_limits)
    
    topic_df = pd.DataFrame(topic_analysis)
    
    # Clean topic names
    topic_clean_names = {
        'Maternal outcomes ': 'Maternal Outcomes',
        'Other': 'Other Topics', 
        'Child health outcomes ': 'Child Health Outcomes',
        'Neonatal outcomes ': 'Neonatal Outcomes', 
        'Immunization ': 'Immunization'
    }
    topic_df['Clean_Topic'] = topic_df['Topic'].map(topic_clean_names)
    
    print("Distinctive Limitations by Topic Area:")
    print("(Positive values = more common in this topic, Negative = less common)")
    
    # Show most distinctive limitation for each topic
    for _, row in topic_df.iterrows():
        distinctive_limits = []
        for col in limitation_columns:
            if row[col] > 5:  # More than 5% higher than other topics
                distinctive_limits.append(f"{col}: +{row[col]:.1f}%")
            elif row[col] < -5:  # More than 5% lower than other topics
                distinctive_limits.append(f"{col}: {row[col]:.1f}%")
        
        print(f"\n{row['Clean_Topic']} (N={row['N']}):")
        if distinctive_limits:
            for limit in distinctive_limits[:3]:  # Top 3 distinctive
                print(f"  • {limit}")
        else:
            print("  No strongly distinctive limitations")
    
        # Visualization - Distinctive limitations by topic
    plt.figure(figsize=(12, 8))
    
    # Prepare data for heatmap-style visualization
    viz_data = []
    for _, row in topic_df.iterrows():
        for col in limitation_columns:
            if abs(row[col]) > 5:  # Only show distinctive differences
                viz_data.append({
                    'Topic': row['Clean_Topic'],
                    'Limitation': col.replace('-- ', '').replace(' --', ''),
                    'Distinctiveness': row[col],
                    'Size': abs(row[col])
                })
    
    if viz_data:  # Only create visualization if we have distinctive data
        viz_df = pd.DataFrame(viz_data)
        
        # Create bubble chart
        topics = viz_df['Topic'].unique()
        limitations = viz_df['Limitation'].unique()
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        for i, topic in enumerate(topics):
            for j, limitation in enumerate(limitations):
                data_point = viz_df[(viz_df['Topic'] == topic) & (viz_df['Limitation'] == limitation)]
                if not data_point.empty:
                    distinctiveness = data_point['Distinctiveness'].iloc[0]
                    size = data_point['Size'].iloc[0] * 10  # Scale for visibility
                    color = 'green' if distinctiveness > 0 else 'red'
                    
                    ax.scatter(j, i, s=size, c=color, alpha=0.6, edgecolors='black', linewidth=0.5)
                    ax.text(j, i, f'{distinctiveness:+.1f}%', ha='center', va='center', 
                           fontsize=9, fontweight='bold')
        
        ax.set_xticks(range(len(limitations)))
        ax.set_xticklabels(limitations, rotation=45, ha='right')
        ax.set_yticks(range(len(topics)))
        ax.set_yticklabels(topics)
        ax.set_xlabel('Limitation Category')
        ax.set_ylabel('Topic Area')
        ax.set_title('Distinctive Limitation Patterns by MCH Topic Area\n(Green = More Common, Red = Less Common)')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/figures/07_topic_areas.png', dpi=300, bbox_inches='tight')
        plt.show()
    else:
        print("\nNo strongly distinctive patterns found for visualization")
    return topic_df

def analyze_funding_impact(df, limitation_columns):
    """Compare limitation reporting between internationally funded studies and studies with no funding disclosure"""
    print("\n=== 8. FUNDING TRANSPARENCY AND LIMITATION REPORTING ===")
    
    print("Funding source distribution:")
    funding_counts = df['Funding sources'].value_counts()
    print(funding_counts)
    
    # Focus on meaningful comparison: International vs Not reported (adequate sample sizes)
    international_studies = df[df['Funding sources'].str.strip() == 'International']
    not_reported_studies = df[df['Funding sources'].str.strip() == 'Not reported']
    
    print(f"\nComparison groups:")
    print(f"International funded: {len(international_studies)} studies")
    print(f"No funding disclosure: {len(not_reported_studies)} studies")
    
    # Define methodological vs contextual categories
    methodological_columns = [
        '-- SAMPLING & DESIGN --',
        '-- MEASUREMENT & DATA --', 
        '-- ANALYSIS & GENERALIZABILITY --'
    ]
    
    contextual_columns = [
        '-- CONTEXT & LOGISTICS --',
        '-- RESEARCH CAPACITY --'
    ]
    
    # Calculate percentages for each group
    comparison_data = []
    
    for group_name, group_studies in [('International', international_studies), ('Not Reported', not_reported_studies)]:
        # Methodological limitations
        methodological_count = group_studies[methodological_columns].notna().any(axis=1).sum()
        methodological_pct = (methodological_count / len(group_studies)) * 100
        
        # Contextual limitations  
        contextual_count = group_studies[contextual_columns].notna().any(axis=1).sum()
        contextual_pct = (contextual_count / len(group_studies)) * 100
        
        # Any limitations reported
        any_limitations = group_studies[limitation_columns].notna().any(axis=1).sum()
        any_limitations_pct = (any_limitations / len(group_studies)) * 100
        
        comparison_data.append({
            'Funding_Group': group_name,
            'Methodological_Percentage': methodological_pct,
            'Contextual_Percentage': contextual_pct,
            'Any_Limitations_Percentage': any_limitations_pct,
            'N': len(group_studies)
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nLimitation Reporting by Funding Disclosure:")
    print(comparison_df[['Funding_Group', 'N', 'Methodological_Percentage', 'Contextual_Percentage', 'Any_Limitations_Percentage']])
    
    # Visualization - Methodological vs Contextual comparison
    plt.figure(figsize=(10, 6))
    
    groups = comparison_df['Funding_Group']
    methodological_pct = comparison_df['Methodological_Percentage']
    contextual_pct = comparison_df['Contextual_Percentage']
    
    x = np.arange(len(groups))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, methodological_pct, width, label='Methodological Limitations', color='#1f77b4', alpha=0.8)
    bars2 = plt.bar(x + width/2, contextual_pct, width, label='Contextual Limitations', color='#ff7f0e', alpha=0.8)
    
    plt.xlabel('Funding Disclosure')
    plt.ylabel('Percentage of Studies Reporting (%)')
    plt.title('Limitation Reporting: International Funding vs No Disclosure\nNigerian MCH Research (2014-2024)')
    plt.xticks(x, groups)
    plt.legend()
    plt.ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/08_funding_impact.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return comparison_df

def analyze_urban_rural(df, limitation_columns):
    """Compare limitation patterns across urban, rural, and mixed geographic settings"""
    print("\n=== 9. GEOGRAPHIC SETTING AND LIMITATION PATTERNS ===")
    
    print("Urban-Rural distribution:")
    urban_rural_counts = df['Urban_Rural_clean'].value_counts()
    print(urban_rural_counts)
    
    # Focus on meaningful comparison: Urban vs Rural vs Both (exclude "Not specified")
    urban_studies = df[df['Urban–Rural'].str.strip() == 'Urban']
    rural_studies = df[df['Urban–Rural'].str.strip() == 'Rural']
    both_studies = df[df['Urban–Rural'].str.strip() == 'Both']
    
    print(f"\nComparison groups:")
    print(f"Urban settings: {len(urban_studies)} studies")
    print(f"Rural settings: {len(rural_studies)} studies")
    print(f"Mixed settings: {len(both_studies)} studies")
    
    # Define methodological vs contextual categories
    methodological_columns = [
        '-- SAMPLING & DESIGN --',
        '-- MEASUREMENT & DATA --', 
        '-- ANALYSIS & GENERALIZABILITY --'
    ]
    
    contextual_columns = [
        '-- CONTEXT & LOGISTICS --',
        '-- RESEARCH CAPACITY --'
    ]
    
    # Calculate percentages for each geographic setting
    comparison_data = []
    
    for setting_name, setting_studies in [('Urban', urban_studies), ('Rural', rural_studies), ('Mixed (Both)', both_studies)]:
        if len(setting_studies) > 0:
            # Methodological limitations
            methodological_count = setting_studies[methodological_columns].notna().any(axis=1).sum()
            methodological_pct = (methodological_count / len(setting_studies)) * 100
            
            # Contextual limitations  
            contextual_count = setting_studies[contextual_columns].notna().any(axis=1).sum()
            contextual_pct = (contextual_count / len(setting_studies)) * 100
            
            # Specific contextual challenges that might vary by setting
            logistics_count = setting_studies['-- CONTEXT & LOGISTICS --'].notna().sum()
            logistics_pct = (logistics_count / len(setting_studies)) * 100
            
            comparison_data.append({
                'Setting': setting_name,
                'Methodological_Percentage': methodological_pct,
                'Contextual_Percentage': contextual_pct,
                'Logistics_Percentage': logistics_pct,
                'N': len(setting_studies)
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nLimitation Patterns by Geographic Setting:")
    print(comparison_df[['Setting', 'N', 'Methodological_Percentage', 'Contextual_Percentage', 'Logistics_Percentage']])
    
    # Visualization - Methodological vs Contextual comparison by setting
    plt.figure(figsize=(12, 6))
    
    settings = comparison_df['Setting']
    methodological_pct = comparison_df['Methodological_Percentage']
    contextual_pct = comparison_df['Contextual_Percentage']
    
    x = np.arange(len(settings))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, methodological_pct, width, label='Methodological Limitations', color='#1f77b4', alpha=0.8)
    bars2 = plt.bar(x + width/2, contextual_pct, width, label='Contextual Limitations', color='#ff7f0e', alpha=0.8)
    
    plt.xlabel('Geographic Setting')
    plt.ylabel('Percentage of Studies Reporting (%)')
    plt.title('Limitation Patterns by Geographic Setting\nNigerian MCH Research (2014-2024)')
    plt.xticks(x, settings)
    plt.legend()
    plt.ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/09_urban_rural.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return comparison_df

def analyze_multi_site_studies(df, limitation_columns):
    """Compare limitation patterns between multi-site and single-site study designs"""
    print("\n=== 10. STUDY DESIGN COMPLEXITY: MULTI-SITE vs SINGLE-SITE ===")
    
    print("Multi-site study distribution:")
    multi_site_counts = df['Multi-site study '].value_counts()
    print(multi_site_counts)
    
    # Focus on meaningful comparison: Multi-site vs Single-site
    multi_site_studies = df[df['Multi-site study '].str.strip() == 'Yes']
    single_site_studies = df[df['Multi-site study '].str.strip() == 'No']
    
    print(f"\nComparison groups:")
    print(f"Multi-site studies: {len(multi_site_studies)} studies")
    print(f"Single-site studies: {len(single_site_studies)} studies")
    
    # Define methodological vs contextual categories
    methodological_columns = [
        '-- SAMPLING & DESIGN --',
        '-- MEASUREMENT & DATA --', 
        '-- ANALYSIS & GENERALIZABILITY --'
    ]
    
    contextual_columns = [
        '-- CONTEXT & LOGISTICS --',
        '-- RESEARCH CAPACITY --'
    ]
    
    # Calculate percentages for each study design
    comparison_data = []
    
    for design_name, design_studies in [('Multi-site', multi_site_studies), ('Single-site', single_site_studies)]:
        # Methodological limitations
        methodological_count = design_studies[methodological_columns].notna().any(axis=1).sum()
        methodological_pct = (methodological_count / len(design_studies)) * 100
        
        # Contextual limitations  
        contextual_count = design_studies[contextual_columns].notna().any(axis=1).sum()
        contextual_pct = (contextual_count / len(design_studies)) * 100
        
        # Specific limitations that might differ by design
        generalizability_count = design_studies['-- ANALYSIS & GENERALIZABILITY --'].notna().sum()
        generalizability_pct = (generalizability_count / len(design_studies)) * 100
        
        logistics_count = design_studies['-- CONTEXT & LOGISTICS --'].notna().sum()
        logistics_pct = (logistics_count / len(design_studies)) * 100
        
        comparison_data.append({
            'Study_Design': design_name,
            'Methodological_Percentage': methodological_pct,
            'Contextual_Percentage': contextual_pct,
            'Generalizability_Percentage': generalizability_pct,
            'Logistics_Percentage': logistics_pct,
            'N': len(design_studies)
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nLimitation Patterns by Study Design:")
    print(comparison_df[['Study_Design', 'N', 'Methodological_Percentage', 'Contextual_Percentage', 'Generalizability_Percentage', 'Logistics_Percentage']])
    
    # Visualization - Methodological vs Contextual comparison by design
    plt.figure(figsize=(10, 6))
    
    designs = comparison_df['Study_Design']
    methodological_pct = comparison_df['Methodological_Percentage']
    contextual_pct = comparison_df['Contextual_Percentage']
    
    x = np.arange(len(designs))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, methodological_pct, width, label='Methodological Limitations', color='#1f77b4', alpha=0.8)
    bars2 = plt.bar(x + width/2, contextual_pct, width, label='Contextual Limitations', color='#ff7f0e', alpha=0.8)
    
    plt.xlabel('Study Design')
    plt.ylabel('Percentage of Studies Reporting (%)')
    plt.title('Limitation Patterns by Study Design Complexity\nNigerian MCH Research (2014-2024)')
    plt.xticks(x, designs)
    plt.legend()
    plt.ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/10_multi_site.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return comparison_df

def analyze_journal_types(df, limitation_columns):
    """Compare limitation reporting patterns between international and local journals"""
    print("\n=== 11. PUBLICATION VENUE: INTERNATIONAL vs LOCAL JOURNALS ===")
    
    print("Journal type distribution:")
    journal_counts = df['Journal type '].value_counts()
    print(journal_counts)
    
    # Focus on meaningful comparison: International vs Local journals
    international_studies = df[df['Journal type '].str.strip() == 'International']
    local_studies = df[df['Journal type '].str.strip() == 'Local']
    
    print(f"\nComparison groups:")
    print(f"International journals: {len(international_studies)} studies")
    print(f"Local journals: {len(local_studies)} studies")
    
    # Define methodological vs contextual categories
    methodological_columns = [
        '-- SAMPLING & DESIGN --',
        '-- MEASUREMENT & DATA --', 
        '-- ANALYSIS & GENERALIZABILITY --'
    ]
    
    contextual_columns = [
        '-- CONTEXT & LOGISTICS --',
        '-- RESEARCH CAPACITY --'
    ]
    
    # Calculate percentages for each journal type
    comparison_data = []
    
    for journal_type, journal_studies in [('International', international_studies), ('Local', local_studies)]:
        # Methodological limitations
        methodological_count = journal_studies[methodological_columns].notna().any(axis=1).sum()
        methodological_pct = (methodological_count / len(journal_studies)) * 100
        
        # Contextual limitations  
        contextual_count = journal_studies[contextual_columns].notna().any(axis=1).sum()
        contextual_pct = (contextual_count / len(journal_studies)) * 100
        
        # Specific limitations that might differ by journal type
        generalizability_count = journal_studies['-- ANALYSIS & GENERALIZABILITY --'].notna().sum()
        generalizability_pct = (generalizability_count / len(journal_studies)) * 100
        
        logistics_count = journal_studies['-- CONTEXT & LOGISTICS --'].notna().sum()
        logistics_pct = (logistics_count / len(journal_studies)) * 100
        
        # Overall limitation reporting
        any_limitations = journal_studies[limitation_columns].notna().any(axis=1).sum()
        any_limitations_pct = (any_limitations / len(journal_studies)) * 100
        
        comparison_data.append({
            'Journal_Type': journal_type,
            'Methodological_Percentage': methodological_pct,
            'Contextual_Percentage': contextual_pct,
            'Generalizability_Percentage': generalizability_pct,
            'Logistics_Percentage': logistics_pct,
            'Any_Limitations_Percentage': any_limitations_pct,
            'N': len(journal_studies)
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nLimitation Reporting by Journal Type:")
    print(comparison_df[['Journal_Type', 'N', 'Methodological_Percentage', 'Contextual_Percentage', 'Generalizability_Percentage', 'Any_Limitations_Percentage']])
    
    # Visualization - Methodological vs Contextual comparison by journal type
    plt.figure(figsize=(10, 6))
    
    journal_types = comparison_df['Journal_Type']
    methodological_pct = comparison_df['Methodological_Percentage']
    contextual_pct = comparison_df['Contextual_Percentage']
    
    x = np.arange(len(journal_types))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, methodological_pct, width, label='Methodological Limitations', color='#1f77b4', alpha=0.8)
    bars2 = plt.bar(x + width/2, contextual_pct, width, label='Contextual Limitations', color='#ff7f0e', alpha=0.8)
    
    plt.xlabel('Journal Type')
    plt.ylabel('Percentage of Studies Reporting (%)')
    plt.title('Limitation Reporting Patterns by Publication Venue\nNigerian MCH Research (2014-2024)')
    plt.xticks(x, journal_types)
    plt.legend()
    plt.ylim(0, 100)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/11_journal_types.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return comparison_df

def analyze_study_characteristics(df):
    """
    Analyze basic study characteristics for the scoping review
    """
    print("\n=== STUDY CHARACTERISTICS ===")
    
    # Study selection summary
    print("STUDY SELECTION:")
    print("• 2388 references imported for screening")
    print("• 2054 studies screened against title/abstract")
    print("• 539 reports assessed for eligibility") 
    print("• 228 studies included in final analysis")
    
    # Study designs
    print("\nSTUDY DESIGNS:")
    design_counts = df['Study design'].value_counts()
    for design, count in design_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {design}: {count} ({percentage:.1f}%)")
    
    # Geographic distribution
    print("\nGEOGRAPHIC DISTRIBUTION:")
    region_counts = df['Region_clean'].value_counts()
    for region, count in region_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {region}: {count} ({percentage:.1f}%)")
    
    # Publication years
    print("\nPUBLICATION YEARS (2014-2024):")
    year_counts = df['Year of publication'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f"  {year}: {count} studies")
    
    return design_counts

def analyze_top5_limitations_trends(df, limitation_columns):
    print("\n=== TOP 5 LIMITATIONS TEMPORAL TRENDS (2014-2024) ===")
    
    limitation_counts = {}
    
    for col in limitation_columns:
        non_null_data = df[col].dropna()
        for value in non_null_data:
            codes = [code.strip() for code in str(value).split(';')]
            for code in codes:
                code_key = code.split(':')[0].strip() if ':' in code else code.strip()
                if code_key in limitation_counts:
                    limitation_counts[code_key] += 1
                else:
                    limitation_counts[code_key] = 1
    
    top_limitations_df = pd.DataFrame.from_dict(limitation_counts, orient='index', columns=['Count'])
    top_limitations_df['Percentage'] = (top_limitations_df['Count'] / len(df)) * 100
    top_limitations_df = top_limitations_df.sort_values('Count', ascending=False)
    
    top_5_limitations = top_limitations_df.head(5).index.tolist()
    print(f"Top 5 Limitations to track: {top_5_limitations}")
    
    df['Year'] = pd.to_numeric(df['Year of publication'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    
    trends_data = []
    years = sorted(df['Year'].unique())
    
    for year in years:
        year_studies = df[df['Year'] == year]
        if len(year_studies) == 0:
            continue
            
        year_data = {'Year': year, 'Total_Studies': len(year_studies)}
        
        for limitation in top_5_limitations:
            count = 0
            for col in limitation_columns:
                for idx, value in year_studies[col].items():
                    if pd.notna(value):
                        codes = [code.strip() for code in str(value).split(';')]
                        clean_codes = [code.split(':')[0].strip() if ':' in code else code.strip() for code in codes]
                        if limitation in clean_codes:
                            count += 1
                            break
            
            percentage = (count / len(year_studies)) * 100 if len(year_studies) > 0 else 0
            year_data[limitation] = percentage
        
        trends_data.append(year_data)
    
    trends_df = pd.DataFrame(trends_data)
    
    plt.figure(figsize=(12, 8))
    
    for limitation in top_5_limitations:
        if limitation in trends_df.columns:
            plt.plot(trends_df['Year'], trends_df[limitation], marker='o', linewidth=2.5, label=limitation)
    
    plt.title('Trends in Top 5 Reported Limitations (2014-2024)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Publication Year', fontsize=12)
    plt.ylabel('Percentage of Studies Reporting Limitation (%)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    
    os.makedirs('outputs/figures', exist_ok=True)
    plt.savefig('outputs/figures/12_top5_limitations_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nTop 5 Limitations Temporal Trends analysis completed!")
    print(f"Figure saved as: outputs/figures/12_top5_limitations_trends.png")
    
    return trends_df

def analyze_limitation_cooccurrence(df, limitation_columns):
    print("\n=== LIMITATION CO-OCCURRENCE ANALYSIS ===")
    
    limitation_counts = {}
    
    for col in limitation_columns:
        non_null_data = df[col].dropna()
        for value in non_null_data:
            codes = [code.strip() for code in str(value).split(';')]
            for code in codes:
                code_key = code.split(':')[0].strip() if ':' in code else code.strip()
                if code_key in limitation_counts:
                    limitation_counts[code_key] += 1
                else:
                    limitation_counts[code_key] = 1
    
    top_limitations_df = pd.DataFrame.from_dict(limitation_counts, orient='index', columns=['Count'])
    top_limitations_df = top_limitations_df.sort_values('Count', ascending=False)
    top_10_limitations = top_limitations_df.head(10).index.tolist()
    
    print(f"Top 10 limitations for co-occurrence analysis: {top_10_limitations}")
    
    cooccurrence_matrix = pd.DataFrame(0, index=top_10_limitations, columns=top_10_limitations)
    
    for col in limitation_columns:
        for idx, value in df[col].items():
            if pd.notna(value):
                codes = [code.strip() for code in str(value).split(';')]
                clean_codes = [code.split(':')[0].strip() if ':' in code else code.strip() for code in codes]
                present_limitations = [lim for lim in top_10_limitations if lim in clean_codes]
                
                for i, lim1 in enumerate(present_limitations):
                    for lim2 in present_limitations[i+1:]:
                        cooccurrence_matrix.loc[lim1, lim2] += 1
                        cooccurrence_matrix.loc[lim2, lim1] += 1
    
    plt.figure(figsize=(12, 10))
    
    total_studies = len(df)
    cooccurrence_pct = (cooccurrence_matrix / total_studies) * 100
    
    mask = np.triu(np.ones_like(cooccurrence_pct, dtype=bool))
    sns.heatmap(cooccurrence_pct, mask=mask, annot=True, fmt='.1f', cmap='YlOrRd',
                square=True, cbar_kws={'label': 'Co-occurrence Percentage (%)'})
    
    plt.title('Co-occurrence of Top 10 Limitations\n(Percentage of Studies Reporting Both)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    os.makedirs('outputs/figures', exist_ok=True)
    plt.savefig('outputs/figures/13_limitation_cooccurrence.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nLimitation Co-occurrence analysis completed!")
    print(f"Figure saved as: outputs/figures/13_limitation_cooccurrence.png")
    
    cooccurrence_pairs = []
    for i, lim1 in enumerate(top_10_limitations):
        for lim2 in top_10_limitations[i+1:]:
            if cooccurrence_pct.loc[lim1, lim2] > 0:
                cooccurrence_pairs.append((lim1, lim2, cooccurrence_pct.loc[lim1, lim2]))
    
    cooccurrence_pairs.sort(key=lambda x: x[2], reverse=True)
    
    print("\nTop Co-occurring Limitation Pairs:")
    for i, (lim1, lim2, pct) in enumerate(cooccurrence_pairs[:10], 1):
        print(f"{i}. {lim1} + {lim2}: {pct:.1f}% of studies")
    
    return cooccurrence_pct

def main():
    print("=== NIGERIAN MCH RESEARCH LIMITATIONS ANALYSIS ===\n")
    
    # Load data
    df, limitation_columns = load_data()
    print(f"Dataset: {len(df)} studies from 2014 to 2024")
    
    study_chars = analyze_study_characteristics(df)
    
    # Create outputs directory
    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('outputs/tables', exist_ok=True)
    
    # Run all 11 analyses
    results = {}
    
    print("\n" + "="*60)
    print("ANALYSIS 1: BROAD LIMITATION CATEGORIES")
    print("="*60)
    results['limitation_categories'] = analyze_limitation_categories(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 2: SPECIFIC LIMITATION CODES")
    print("="*60)
    results['specific_limitations'] = analyze_specific_limitations(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 3: FACILITY vs COMMUNITY STUDIES")
    print("="*60)
    results['facility_community'] = analyze_facility_vs_community(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 4: REGIONAL COMPARISON")
    print("="*60)
    results['regional'] = analyze_regional_comparison(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 5: TRENDS OVER TIME")
    print("="*60)
    results['trends'] = analyze_trends_over_time(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 6: CONTEXTUAL LIMITATIONS TRENDS")
    print("="*60)
    results['contextual_trends'] = analyze_contextual_limitations_trends(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 7: TOPIC AREAS")
    print("="*60)
    results['topic_areas'] = analyze_topic_areas(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 8: FUNDING IMPACT")
    print("="*60)
    results['funding'] = analyze_funding_impact(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 9: URBAN-RURAL SETTINGS")
    print("="*60)
    results['urban_rural'] = analyze_urban_rural(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 10: MULTI-SITE vs SINGLE-SITE")
    print("="*60)
    results['multi_site'] = analyze_multi_site_studies(df, limitation_columns)
    
    print("\n" + "="*60)
    print("ANALYSIS 11: JOURNAL TYPES")
    print("="*60)
    results['journal_types'] = analyze_journal_types(df, limitation_columns)

    print("\n" + "="*60)
    print("ANALYSIS 12: TOP 5 LIMITATIONS TEMPORAL TRENDS")
    print("="*60)
    results['top5_trends'] = analyze_top5_limitations_trends(df, limitation_columns)

    print("\n" + "="*60)
    print("ANALYSIS 13: LIMITATION CO-OCCURRENCE")
    print("="*60)
    results['cooccurrence'] = analyze_limitation_cooccurrence(df, limitation_columns)
    
    print("\n=== ANALYSIS COMPLETE ===")
    print("All 11 analyses completed and outputs saved to outputs/ folder")
    
    return results

# Execute the main analysis function
if __name__ == "__main__":
    results = main()
