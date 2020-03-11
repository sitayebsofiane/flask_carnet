# Statement for enabling the development environment
DEBUG = True
ENV = 'development'
# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the SQLite database i.e. notebook.db
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'notebook.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "lsxdr4o0_8w3xx232kfslkaz1?jf-!333l1~=jfld"

# Secret key for signing cookies
SECRET_KEY = "lsxdr4o0_8w3xx232kfslkaz1?jfse_9?xdfd"