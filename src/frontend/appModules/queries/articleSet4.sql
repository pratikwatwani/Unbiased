select title, counts from wikid where 
(title like concat('%', (select actor1name 
    from eventsxgeog where actor1geo_fullname='{0}' 
    and extract(year from dateadded) = {1} order by 
    nummentions desc limit 1),'%')  
or title like 
    concat('%', (select actor2name from eventsxgeog 
    where actor2geo_fullname = '{0}'  and 
    extract(year from dateadded) = {1} order by 
    nummentions desc offset 1 limit 1),'%')
or title like 
    concat('%', (select actor1geo_fullname from eventsxgeog 
    where actiongeo_fullname = '{0}'  and 
    extract(year from dateadded) = {1} order by 
    nummentions desc offset 2 limit 1),'%')
or title like 
    concat('%', (select actor2geo_fullname from eventsxgeog 
    where actiongeo_fullname = '{0}'  and 
    extract(year from dateadded) = {1} order by 
    nummentions desc offset 3 limit 1),'%')) 
and year = {1} order by counts desc limit 5;