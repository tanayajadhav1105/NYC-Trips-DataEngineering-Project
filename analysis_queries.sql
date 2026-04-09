--Find top 10 locations based on the number of trips
select d.pickup_location_id, 
       d.PULocationID, 
       d.borough, 
       d.zone, 
       d.service_zone 
from nyc-trips-de-project-491201.nyc_trips_DE_ds.pickup_location_dim d JOIN 
(select pickup_location_id, count(trip_id)
 from nyc-trips-de-project-491201.nyc_trips_DE_ds.fact_table 
 group by pickup_location_id 
 order by count(trip_id) 
 desc LIMIT 10) f
on d.pickup_location_id=f.pickup_location_id
order by trip_count DESC;


--Find the total number of trips by passenger count
Select d.passenger_count_id, 
       d.passenger_count, 
       count(trip_id) total_trips
FROM nyc-trips-de-project-491201.nyc_trips_DE_ds.fact_table f JOIN
nyc-trips-de-project-491201.nyc_trips_DE_ds.passenger_count_dim d
ON f.passenger_count_id = d.passenger_count_id
GROUP BY d.passenger_count_id, d.passenger_count
ORDER BY count(trip_id) DESC;


--Find the average fare amount by hour of the day
Select d.hour pickup_hour,
       AVG(fare_amount) avg_fare_amount
FROM nyc-trips-de-project-491201.nyc_trips_DE_ds.fact_table f JOIN
nyc-trips-de-project-491201.nyc_trips_DE_ds.pickup_datetime_dim d
ON f.pickup_datetime_id = d.pickup_datetime_id
GROUP BY d.hour
ORDER BY AVG(fare_amount) DESC;



---Final Select
SELECT f.trip_id,
f.VendorID,
pd.tpep_pickup_datetime,
dd.tpep_dropoff_datetime,
pc.passenger_count,
t.trip_distance,
r.rate_code_name,
pl.Borough pickup_borough,
pl.Zone pickup_zone,
pl.service_zone pickup_service_zone,
dl.Borough dropoff_borough,
dl.Zone dropoff_zone,
dl.service_zone dropoff_service_zone,
pt.payment_type_name,
f.fare_amount,
f.extra,
f.mta_tax,
f.tip_amount,
f.tolls_amount,
f.improvement_surcharge,
f.total_amount
FROM 
`nyc-trips-de-project-491201.nyc_trips_DE_ds.fact_table` f
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.pickup_datetime_dim` pd on f.pickup_datetime_id = pd.pickup_datetime_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.dropoff_datetime_dim` dd on f.dropoff_datetime_id = dd.dropoff_datetime_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.passenger_count_dim` pc on f.passenger_count_id = pc.passenger_count_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.trip_distance_dim` t on f.trip_distance_id = t.trip_distance_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.rate_code_dim` r on f.rate_code_id = r.rate_code_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.pickup_location_dim` pl on f.pickup_location_id = pl.pickup_location_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.dropoff_location_dim` dl on f.dropoff_location_id = dl.dropoff_location_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.payment_type_dim` pt on f.payment_type_id = pt.payment_type_id
JOIN `nyc-trips-de-project-491201.nyc_trips_DE_ds.store_and_fwd_dim` sf on f.store_fwd_flag_id = sf.store_fwd_flag_id
