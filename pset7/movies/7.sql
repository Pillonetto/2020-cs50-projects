SELECT title, rating
FROM movies JOIN ratings
ON id = movie_id
WHERE year = 2010 AND rating BETWEEN 0 AND 10
ORDER BY rating DESC, title;