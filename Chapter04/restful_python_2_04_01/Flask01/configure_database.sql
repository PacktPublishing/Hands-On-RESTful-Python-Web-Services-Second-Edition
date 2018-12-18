CREATE ROLE your_user_name WITH LOGIN PASSWORD 'your_password';

GRANT ALL PRIVILEGES ON DATABASE "flask_notifications" TO your_user_name;
ALTER USER your_user_name CREATEDB;
\q
