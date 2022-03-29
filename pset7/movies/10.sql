SELECT name
FROM people JOIN directors
ON id = person_id
WHERE movie_id IN (SELECT ratings.movie_id FROM ratings WHERE rating >= 9.0)
ORDER BY name;