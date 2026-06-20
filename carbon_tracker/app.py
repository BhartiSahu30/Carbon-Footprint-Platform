import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model for EcoTrack User Metrics
class CarbonLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(10), nullable=False) # Format: YYYY-MM-DD
    transport_emissions = db.Column(db.Float, nullable=False)
    energy_emissions = db.Column(db.Float, nullable=False)
    diet_emissions = db.Column(db.Float, nullable=False)
    waste_emissions = db.Column(db.Float, nullable=False)
    total_daily = db.Column(db.Float, nullable=False)

# Advanced Carbon Intensity Coefficients (kg CO2e per unit)
EMISSION_FACTORS = {
    "transport": {"petrol_car": 0.170, "diesel_car": 0.171, "ev": 0.047, "transit": 0.035, "zero": 0.0},
    "energy": {"electricity": 0.475, "gas": 0.181},
    "diet": {"heavy_meat": 3.3, "average": 2.5, "vegetarian": 1.4, "vegan": 0.9},
    "waste": {"standard": 0.52, "recycle_pro": 0.15} # Per kg of household waste
}

# Ensure database tables exist cleanly on startup
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/log', methods=['POST'])
def log_emissions():
    data = request.get_json()
    
    # Calculate operational metrics
    t_emissions = float(data.get('distance', 0)) * EMISSION_FACTORS['transport'].get(data.get('transport_type'), 0)
    e_emissions = float(data.get('electricity', 0)) * EMISSION_FACTORS['energy']['electricity'] + float(data.get('gas', 0)) * EMISSION_FACTORS['energy']['gas']
    d_emissions = EMISSION_FACTORS['diet'].get(data.get('diet_type'), 2.5)
    w_emissions = float(data.get('waste_weight', 0)) * EMISSION_FACTORS['waste'].get(data.get('waste_type'), 0.52)
    
    total = t_emissions + e_emissions + d_emissions + w_emissions
    date_str = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    
    # Persistent State Handling: Check if entry exists for selected date
    existing_record = CarbonLog.query.filter_by(timestamp=date_str).first()
    if existing_record:
        existing_record.transport_emissions = t_emissions
        existing_record.energy_emissions = e_emissions
        existing_record.diet_emissions = d_emissions
        existing_record.waste_emissions = w_emissions
        existing_record.total_daily = total
    else:
        new_log = CarbonLog(
            timestamp=date_str,
            transport_emissions=t_emissions,
            energy_emissions=e_emissions,
            diet_emissions=d_emissions,
            waste_emissions=w_emissions,
            total_daily=total
        )
        db.session.add(new_log)
        
    db.session.commit()
    return jsonify({"status": "success", "message": "Metrics processed successfully"})

@app.route('/api/history', methods=['GET'])
def get_history():
    logs = CarbonLog.query.order_by(CarbonLog.timestamp.desc()).limit(7).all()
    history_list = []
    for log in logs:
        history_list.append({
            "date": log.timestamp,
            "breakdown": {
                "Transport": round(log.transport_emissions, 2),
                "Energy": round(log.energy_emissions, 2),
                "Diet": round(log.diet_emissions, 2),
                "Waste": round(log.waste_emissions, 2)
            },
            "total": round(log.total_daily, 2)
        })
    return jsonify(history_list)

if __name__ == '__main__':
    # Binds to 0.0.0.0 and reads port from cloud environment variable, defaults to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    app.run(debug=True)