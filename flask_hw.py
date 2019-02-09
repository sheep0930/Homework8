import numpy as np
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread':False})
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()
    all_precipitations = list(np.ravel(results))

    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    all_station = list(np.ravel(results))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    date_end = session.query(func.max(Measurement.date)).all()[0][0]
    date_stt = dt.datetime.strptime(date_end, '%Y-%m-%d').date() - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= date_stt).order_by(Measurement.date).all()
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>/<end>")
def tmp_stt_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    stat_tobs = list(np.ravel(results))

    return jsonify(stat_tobs)

@app.route("/api/v1.0/<start>")
def tmp_stt(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    stat_tobs = list(np.ravel(results))

    return jsonify(stat_tobs)

if __name__ == "__main__":
    app.run(debug=True)