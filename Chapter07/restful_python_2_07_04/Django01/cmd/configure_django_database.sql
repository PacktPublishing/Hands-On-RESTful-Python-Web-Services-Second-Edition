CREATE ROLE your_games_user_name WITH LOGIN PASSWORD 'your_games_password';

GRANT ALL PRIVILEGES ON DATABASE "django_games" TO your_user_name;
ALTER USER your_games_user_name CREATEDB;
\q
