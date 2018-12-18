import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
# Replace your_user_name with the user name you configured for the test database
# Replace your_password with the password you specified for the test database user
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="your_user_name", DB_PASS="your_password", DB_ADDR="127.0.0.1", DB_NAME="test_flask_notifications")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# Pagination configuration
PAGINATION_PAGE_SIZE = 4
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
# Enable the TESTING flag
TESTING = True
# Disable CSRF protection in the testing configuration
WTF_CSRF_ENABLED = False
# Necessary for url_for to build the URLs
SERVER_NAME="127.0.0.1"
