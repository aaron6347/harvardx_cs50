SELECT SUM(rating)/COUNT(movie_id) AS average FROM ratings WHERE movie_id IN
(SELECT id FROM movies WHERE year = 2012)