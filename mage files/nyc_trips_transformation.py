import pandas as pd
import gc
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    gc.collect()
    # Specify your transformation logic here
    lookup_url = 'https://storage.googleapis.com/nyc-trips-de-project-bucket/taxi_zone_lookup.csv'
    lookup = pd.read_csv(lookup_url)

    df = df.drop_duplicates().reset_index(drop=True)
    df['trip_id'] = df.index + 1

    #pickup_datetime_dim
    pickup_datetime_dim = df[['tpep_pickup_datetime']].drop_duplicates().reset_index(drop=True)
    pickup_datetime_dim['hour'] = pickup_datetime_dim['tpep_pickup_datetime'].dt.hour
    pickup_datetime_dim['day'] = pickup_datetime_dim['tpep_pickup_datetime'].dt.day
    pickup_datetime_dim['month'] = pickup_datetime_dim['tpep_pickup_datetime'].dt.month
    pickup_datetime_dim['year'] = pickup_datetime_dim['tpep_pickup_datetime'].dt.year
    pickup_datetime_dim['weekday'] = pickup_datetime_dim['tpep_pickup_datetime'].dt.weekday
    pickup_datetime_dim['weekday_name'] = pickup_datetime_dim['tpep_pickup_datetime'].dt.day_name()
    pickup_datetime_dim['quarter'] = pickup_datetime_dim['tpep_pickup_datetime'].dt.quarter
    pickup_datetime_dim['pickup_datetime_id'] = pickup_datetime_dim.index + 1
    pickup_datetime_dim = pickup_datetime_dim[
        [
            'pickup_datetime_id',
            'tpep_pickup_datetime',
            'hour',
            'day',
            'month',
            'year',
            'weekday',
            'weekday_name',
            'quarter'
        ]
    ]

    #dropoff_datetime_dim
    dropoff_datetime_dim = df[['tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)
    dropoff_datetime_dim['hour'] = dropoff_datetime_dim['tpep_dropoff_datetime'].dt.hour
    dropoff_datetime_dim['day'] = dropoff_datetime_dim['tpep_dropoff_datetime'].dt.day
    dropoff_datetime_dim['month'] = dropoff_datetime_dim['tpep_dropoff_datetime'].dt.month
    dropoff_datetime_dim['year'] = dropoff_datetime_dim['tpep_dropoff_datetime'].dt.year
    dropoff_datetime_dim['weekday'] = dropoff_datetime_dim['tpep_dropoff_datetime'].dt.weekday
    dropoff_datetime_dim['weekday_name'] = dropoff_datetime_dim['tpep_dropoff_datetime'].dt.day_name()
    dropoff_datetime_dim['quarter'] = dropoff_datetime_dim['tpep_dropoff_datetime'].dt.quarter
    dropoff_datetime_dim['dropoff_datetime_id'] = dropoff_datetime_dim.index + 1
    dropoff_datetime_dim = dropoff_datetime_dim[
        [
            'dropoff_datetime_id',
            'tpep_dropoff_datetime',
            'hour',
            'day',
            'month',
            'year',
            'weekday',
            'weekday_name',
            'quarter'
        ]
    ]

    # Create passenger count dimension
    passenger_count_dim = df[['passenger_count']].copy()
    passenger_count_dim['passenger_count'] = passenger_count_dim['passenger_count'].fillna(0).astype(int)
    passenger_count_dim = passenger_count_dim[['passenger_count']].drop_duplicates().reset_index(drop=True)
    passenger_count_dim = passenger_count_dim.sort_values(by='passenger_count').reset_index(drop=True)
    passenger_count_dim['passenger_count_id'] = passenger_count_dim.index + 1
    passenger_count_dim = passenger_count_dim[
        [
            'passenger_count_id',
            'passenger_count'
        ]
    ]

    #trip_distance_dim
    trip_distance_dim = df[['trip_distance']].copy()
    trip_distance_dim['trip_distance'] = (
        trip_distance_dim['trip_distance']
        .fillna(0)
        .round(2)
    )
    trip_distance_dim = trip_distance_dim.drop_duplicates().reset_index(drop=True)
    trip_distance_dim = trip_distance_dim.sort_values(by='trip_distance').reset_index(drop=True)
    trip_distance_dim['trip_distance_id'] = trip_distance_dim.index + 1
    trip_distance_dim = trip_distance_dim[['trip_distance_id', 'trip_distance']]

    #rate_code_dim
    rate_code_mapping = {
        1: "Standard rate",
        2: "JFK",
        3: "Newark",
        4: "Nassau or Westchester",
        5: "Negotiated fare",
        6: "Group ride",
        99: "Unknown"
    }
    rate_code_dim = df[['RatecodeID']].copy()
    rate_code_dim['RatecodeID'] = df['RatecodeID'].fillna(99).astype(int)
    rate_code_dim = rate_code_dim.drop_duplicates().reset_index(drop=True)
    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_mapping)
    rate_code_dim = rate_code_dim.sort_values(by='RatecodeID').reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index + 1
    rate_code_dim = rate_code_dim[
        ['rate_code_id', 'RatecodeID', 'rate_code_name']
    ]

    #store_and_fwd_mapping
    store_and_fwd_mapping = {
        'Y': 'Stored and forwarded later',
        'N': 'Sent in real-time',
        'U': 'Unknown'
    }
    store_and_fwd_dim = df[['store_and_fwd_flag']].copy()
    store_and_fwd_dim['store_and_fwd_flag'] = store_and_fwd_dim['store_and_fwd_flag'].fillna('U')
    store_and_fwd_dim = store_and_fwd_dim.drop_duplicates().reset_index(drop=True)
    store_and_fwd_dim['description'] = store_and_fwd_dim['store_and_fwd_flag'].map(store_and_fwd_mapping)
    store_and_fwd_dim = store_and_fwd_dim.sort_values(by='store_and_fwd_flag').reset_index(drop=True)
    store_and_fwd_dim['store_fwd_flag_id'] = store_and_fwd_dim.index + 1
    store_and_fwd_dim = store_and_fwd_dim[
        ['store_fwd_flag_id', 'store_and_fwd_flag', 'description']
    ]

    # pickup_location_dim
    pickup_location_dim = df[['PULocationID']].copy()
    pickup_location_dim = pickup_location_dim.drop_duplicates().reset_index(drop=True)
    pickup_location_dim = pickup_location_dim.merge(
        lookup,
        left_on='PULocationID',
        right_on='LocationID',
        how='left'
    )
    pickup_location_dim['pickup_location_id'] = pickup_location_dim.index + 1
    pickup_location_dim = pickup_location_dim[
        [
            'pickup_location_id',
            'PULocationID',
            'Borough',
            'Zone',
            'service_zone'
        ]
    ]

    # dropoff_location_dim
    dropoff_location_dim = df[['DOLocationID']].copy()
    dropoff_location_dim = dropoff_location_dim.drop_duplicates().reset_index(drop=True)
    dropoff_location_dim = dropoff_location_dim.merge(
        lookup,
        left_on='DOLocationID',
        right_on='LocationID',
        how='left'
    )
    dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index + 1
    dropoff_location_dim = dropoff_location_dim[
        [
            'dropoff_location_id',
            'DOLocationID',
            'Borough',
            'Zone',
            'service_zone'
        ]
    ]

    #payment_type_dim
    payment_mapping = {
        0: "Flex Fare trip",
        1: "Credit card",
        2: "Cash",
        3: "No charge",
        4: "Dispute",
        5: "Unknown",
        6: "Voided trip"
    }
    payment_type_dim = df[['payment_type']].copy()
    payment_type_dim['payment_type'] = payment_type_dim['payment_type'].fillna(5).astype(int)
    payment_type_dim = payment_type_dim.drop_duplicates().reset_index(drop=True)
    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_mapping)
    payment_type_dim = payment_type_dim.sort_values(by='payment_type').reset_index(drop=True)
    payment_type_dim['payment_type_id'] = payment_type_dim.index + 1
    payment_type_dim = payment_type_dim[
        ['payment_type_id', 'payment_type', 'payment_type_name']
    ]

    #fact_table
    fact_table = df.copy()

    # Merge all dimension tables using correct keys
    fact_table = (
        fact_table
        .merge(passenger_count_dim, on='passenger_count', how='left')
        .merge(trip_distance_dim, on='trip_distance', how='left')
        .merge(rate_code_dim, on='RatecodeID', how='left')
        .merge(pickup_location_dim, on='PULocationID', how='left')
        .merge(dropoff_location_dim, on='DOLocationID', how='left')
        .merge(pickup_datetime_dim, on='tpep_pickup_datetime', how='left')
        .merge(dropoff_datetime_dim, on='tpep_dropoff_datetime', how='left')
        .merge(payment_type_dim, on='payment_type', how='left')
        .merge(store_and_fwd_dim, on='store_and_fwd_flag', how='left')
    )

    # Select columns as per ERD
    fact_table = fact_table[
        [
            'trip_id',
            'VendorID',
            'pickup_datetime_id',
            'dropoff_datetime_id',
            'passenger_count_id',
            'trip_distance_id',
            'rate_code_id',
            'store_fwd_flag_id',
            'pickup_location_id',
            'dropoff_location_id',
            'payment_type_id',
            'fare_amount',
            'extra',
            'mta_tax',
            'tip_amount',
            'tolls_amount',
            'improvement_surcharge',
            'congestion_surcharge',
            'Airport_fee',
            'cbd_congestion_fee',
            'total_amount'
        ]
    ]
    # print(fact_table)
    return {
        "fact_table": fact_table,
        "passenger_count_dim": passenger_count_dim,
        "trip_distance_dim": trip_distance_dim,
        "rate_code_dim": rate_code_dim,
        "pickup_location_dim": pickup_location_dim,
        "dropoff_location_dim": dropoff_location_dim,
        "pickup_datetime_dim": pickup_datetime_dim,
        "dropoff_datetime_dim": dropoff_datetime_dim,
        "payment_type_dim": payment_type_dim,
        "store_and_fwd_dim": store_and_fwd_dim
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
