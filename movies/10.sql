SELECT name FROM ratings
JOIN movies ON movies.id = ratings.movie_id
JOIN directors ON movies.id = directors.movie_id
JOIN people ON people.id = directors.person_id
WHERE rating >= 9;

