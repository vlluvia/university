
# q1_sample
```sql
SELECT DISTINCT(language) FROM akas ORDER BY language LIMIT 10;
```

# q2_sci_fi
```sql
select primary_title,premiered,runtime_minutes||'(mins)' from titles where genres like '%Sci-Fi%' order by runtime_minutes desc limit 10;
```
# q3_oldest_people
```sql
select name,died-born as age from people where born>=1900 order by age desc, name ASC limit 20;
```

# q4_crew_appears_most
```sql
select p.name,count(*) as NUM_APPEARANCES from people p, crew c where p.person_id = c.person_id group by p.person_id order by NUM_APPEARANCES desc limit 20;
```

# q5_decade_ratings
```sql 
select CAST(premiered/10*10 AS TEXT) || 's' decade,round(avg(rating),2) avgs, max(rating), min(rating), count(*) as NUM_RELEASES from titles t, ratings r where t.title_id=r.title_id and premiered is not NULL group by decade order by avgs desc, decade asc limit 10;
```

# q6_cruiseing_altitude
```sql
select t.primary_title,r.votes from crew c, people p, titles t, ratings r where c.title_id=t.title_id and c.person_id=p.person_id and t.title_id=r.title_id and p.name like '%Cruise%' and p.born = 1962 order by r.votes  desc limit 10;
```


