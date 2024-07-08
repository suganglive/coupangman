from app import create_app, db, make_celery

app = create_app()
celery = make_celery(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
