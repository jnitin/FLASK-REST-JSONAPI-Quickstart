from application import app, db
from application.endpoints import create_api_endpoints


# Create the database and tables, if not yet exists
# NOTE: this can be done outside the application, using Flask-Migrate
db.create_all()


if __name__ == '__main__':
    # Start application
    app.run(debug=True)
