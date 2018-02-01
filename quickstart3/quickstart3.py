from application import create_app, db

# Create an instance of the application
app = create_app()

# Create the database and tables, if not yet exists
# NOTE: this can be done outside the application, using Flask-Migrate
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    # Start application
    app.run(debug=True)
