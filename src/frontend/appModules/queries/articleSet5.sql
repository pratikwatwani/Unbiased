select title, counts from wikid 
where (title like concat('%', {0}, '%')  
    or title like concat('%', {0}, '%')) 
    and year = {1} 
order by counts desc 
limit 5;
