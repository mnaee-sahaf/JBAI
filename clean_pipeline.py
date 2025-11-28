import pandas as pd
import json
from datetime import datetime

# Fixed exchange rates to USD
EXCHANGE_RATES = {
    'USD': 1.0,
    'MYR': 0.22,
    'PHP': 0.018,
    'PKR': 0.0036
}

def normalize_device(device):
    """Normalize device values to standard format"""
    device_upper = str(device).upper()
    if device_upper in ['WEB', 'DESKTOP']:
        return 'WEB'
    elif device_upper == 'MOBILE':
        return 'MOBILE'
    elif device_upper == 'IOS':
        return 'IOS'
    elif device_upper == 'ANDROID':
        return 'ANDROID'
    else:
        return 'MOBILE'  # default fallback

def convert_to_usd(amount, currency):
    """Convert amount to USD using exchange rates"""
    rate = EXCHANGE_RATES.get(currency, 1.0)
    return round(amount * rate, 2)

def calculate_duration(time_in, time_out):
    """Calculate duration in minutes between time_in and time_out"""
    time_in_dt = pd.to_datetime(time_in)
    time_out_dt = pd.to_datetime(time_out)
    duration = (time_out_dt - time_in_dt).total_seconds() / 60
    return round(duration, 2)

def main():
    # Read the CSV file
    print("Reading input file...")
    df = pd.read_csv('entries.csv')
    
    total_entries = len(df)
    print(f"Total entries loaded: {total_entries}")
    
    # Data cleaning: Remove rows where time_in or time_out is missing
    print("Cleaning data...")
    df_clean = df.dropna(subset=['time_in', 'time_out'])
    
    # Normalize device values
    df_clean['device'] = df_clean['device'].apply(normalize_device)
    
    # Calculate duration in minutes
    df_clean['duration_minutes'] = df_clean.apply(
        lambda row: calculate_duration(row['time_in'], row['time_out']), 
        axis=1
    )
    
    # Convert amount to USD
    df_clean['amount_usd'] = df_clean.apply(
        lambda row: convert_to_usd(row['amount'], row['currency']), 
        axis=1
    )
    
    # Extract date from time_in
    df_clean['date'] = pd.to_datetime(df_clean['time_in']).dt.date
    
    # Select and reorder columns for output
    output_df = df_clean[['user_id', 'organization_id', 'date', 'duration_minutes', 'device', 'amount_usd']]
    
    # Save clean entries to CSV
    print("Saving clean_entries.csv...")
    output_df.to_csv('clean_entries.csv', index=False)
    
    # Generate report
    clean_entries = len(output_df)
    avg_duration = round(output_df['duration_minutes'].mean(), 2)
    total_amount_usd = round(output_df['amount_usd'].sum(), 2)
    
    report = {
        "total_entries": total_entries,
        "clean_entries": clean_entries,
        "avg_duration": avg_duration,
        "total_amount_usd": total_amount_usd
    }
    
    # Save report to JSON
    print("Saving report.json...")
    with open('report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\nPipeline completed successfully!")
    print(f"Clean entries: {clean_entries}")
    print(f"Average duration: {avg_duration} minutes")
    print(f"Total amount (USD): ${total_amount_usd}")

if __name__ == "__main__":
    main()