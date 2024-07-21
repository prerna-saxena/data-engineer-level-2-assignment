import pandas as pd

def clean_and_transform_data(file_path):
    df = pd.read_csv(file_path)

    # Remove trips with missing or corrupt data
    df.dropna(inplace=True)
    df = df[df['trip_distance'] > 0]
    df = df[df['fare_amount'] > 0]

    # Derive new columns
    df['trip_duration'] = pd.to_datetime(df['tpep_dropoff_datetime']) - pd.to_datetime(df['tpep_pickup_datetime'])
    df['trip_duration'] = df['trip_duration'].dt.total_seconds() / 60  # convert to minutes
    df['average_speed'] = df['trip_distance'] / (df['trip_duration'] / 60)  # convert to hours

    # Aggregate data
    df['pickup_date'] = pd.to_datetime(df['tpep_pickup_datetime']).dt.date
    daily_data = df.groupby('pickup_date').agg(total_trips=('trip_distance', 'size'),
                                               avg_fare=('fare_amount', 'mean')).reset_index()

    return df, daily_data

# Example file path
file_path = './data/2019/2019.csv'
cleaned_data, daily_aggregates = clean_and_transform_data(file_path)
