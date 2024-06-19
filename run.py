import sys
import os
from flask_migrate import Migrate

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import create_app, db


app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
