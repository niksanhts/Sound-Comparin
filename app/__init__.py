import logging
import json
from flask import Flask

def create_app():
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    app.config.update(config)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
