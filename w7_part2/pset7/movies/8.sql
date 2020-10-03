SELECT DISTINCT(name) FROM movies JOIN stars ON movies.id = movie_id
JOIN people ON person_id = people.id WHERE title LIKE "Toy Story";
