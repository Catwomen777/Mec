from app import create_app
from app.models import db

from app import create_app

app = create_app("ProductionConfig")

if __name__ == "__main__":
    app.run()

