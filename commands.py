from app import app


with app.app_context():
    @app.cli.command("initdb")
    def reset_db():
        from db import db
        db.drop_all()
        db.create_all()



    @app.cli.command("script")
    def execute_script():
        print("Executing script...")
        