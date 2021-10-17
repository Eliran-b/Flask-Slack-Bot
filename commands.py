from app import app


with app.app_context():
    @app.cli.command("script")
    def execute_script():
        print("Executing script...")
        