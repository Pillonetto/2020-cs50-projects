SELECT COUNT(movies.title)
FROM movies
WHERE movies.id IN (SELECT ratings.movie_id FROM ratings WHERE ratings.rating = 10);