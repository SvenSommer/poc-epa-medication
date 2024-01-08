#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from flask import Flask, render_template, request, jsonify
from fhirapi import fhir_api
from controller.database import Database
from models.bundles import SearchSetBundleModel

logging.basicConfig(level=logging.INFO)
APPNAME = """
     ______  ___   ___  ___         _ _           _   _             
     | ___ \/ _ \  |  \/  |        | (_)         | | (_)            
  ___| |_/ / /_\ \ | .  . | ___  __| |_  ___ __ _| |_ _  ___  _ __  
 / _ \  __/|  _  | | |\/| |/ _ \/ _` | |/ __/ _` | __| |/ _ \| '_ \ 
|  __/ |   | | | | | |  | |  __/ (_| | | (_| (_| | |_| | (_) | | | |
 \___\_|   \_| |_/ \_|  |_/\___|\__,_|_|\___\__,_|\__|_|\___/|_| |_|
                                                                    
                                                                   
"""
                                                       
app = Flask(__name__)
app.register_blueprint(fhir_api)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/ressources", methods=["GET"])
def resources():
    return render_template("resources.html")

@app.route("/get-fhir-data", methods=["GET"])
def get_fhir_data():
    return jsonify(SearchSetBundleModel.manager.get_all())


def start_app():
    logging.info(APPNAME) 
    Database.Instance().start()
    logging.info("Database connected")
    app.run(debug=True)


if __name__ == "__main__":
    start_app()
