select title, w.counts from wikidata w
where title like concat('%', (select actor1name from (select 
actor1name, nummentions from eventsxgeog where 
actor1geo_fullname='{0}'   and 
extract(year from dateadded) = {1} 
union all
select 
actor1name, nummentions from eventsxgeog where 
actor2geo_fullname = '{0}'  and 
extract(year from dateadded) = {1} 
order by nummentions desc limit 1)as stats),'%') 
and year = {1} order by w.counts desc limit 5;