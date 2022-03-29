SELECT name FROM
people JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE stars.movie_id IN (SELECT movie_id FROM stars WHERE person_id = (SELECT people.id FROM people WHERE people.name = 'Kevin Bacon' AND people.birth = 1958))
AND people.name != "Kevin Bacon";