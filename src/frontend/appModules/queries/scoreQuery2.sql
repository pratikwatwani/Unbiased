select avg(avgtone) from eventsXgeog 
where actor1geo_fullname = '{0}' 
or actor2geo_fullname= '{0}' and 
extract(year from dateadded)={1};