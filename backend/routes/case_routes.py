# backend/routes/case_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import PatientCase, User
from utils.ml_model import predict_risk
from utils.rules_engine import run_rules

case_bp = Blueprint('cases', __name__)

@case_bp.route('/', methods=['POST'])
@jwt_required()
def create_case():
    payload = request.get_json() or {}
    identity = get_jwt_identity()
    chw_id = identity.get('id')
    # expected payload: sex, age_months, symptoms (dict), vitals (dict), facility_id (optional)
    sex = payload.get('sex')
    age_months = payload.get('age_months')
    symptoms = payload.get('symptoms', {})
    vitals = payload.get('vitals', {})
    facility_id = payload.get('facility_id')

    # run rules engine (fast, local logic)
    triage_hint = run_rules(age_months=age_months, symptoms=symptoms, vitals=vitals)

    # prepare features for ML (example mapping)
    features = {
        "age_months": age_months or 0,
        "fever": int(bool(symptoms.get('fever'))),
        "cough": int(bool(symptoms.get('cough'))),
        "difficulty_breathing": int(bool(symptoms.get('difficulty_breathing'))),
        "temp_c": float(vitals.get('temp_c') or 0.0)
    }

    risk_score = predict_risk(features)

    # compose referral note
    referral_note = {
        "triage_hint": triage_hint,
        "recommended_action": "refer" if risk_score > 0.5 or triage_hint == 'urgent' else "manage locally",
        "notes": "Auto-generated; confirm clinically"
    }

    case = PatientCase(
        chw_id=chw_id,
        facility_id=facility_id,
        sex=sex,
        age_months=age_months,
        symptoms=symptoms,
        vitals=vitals,
        triage_result=referral_note['recommended_action'],
        risk_score=risk_score,
        referral_note=referral_note,
        synced=True
    )
    db.session.add(case)
    db.session.commit()

    return jsonify({
        "case_id": case.id,
        "triage_result": referral_note['recommended_action'],
        "risk_score": risk_score,
        "referral_note": referral_note
    }), 201

@case_bp.route('/<int:case_id>', methods=['GET'])
@jwt_required()
def get_case(case_id):
    case = PatientCase.query.get_or_404(case_id)
    return jsonify({
        "id": case.id,
        "chw_id": case.chw_id,
        "sex": case.sex,
        "age_months": case.age_months,
        "symptoms": case.symptoms,
        "vitals": case.vitals,
        "triage_result": case.triage_result,
        "risk_score": case.risk_score,
        "referral_note": case.referral_note,
        "created_at": case.created_at.isoformat()
    })

@case_bp.route('/sync', methods=['POST'])
@jwt_required()
def bulk_sync():
    payload = request.get_json() or {}
    cases = payload.get('cases', [])
    saved = []
    for c in cases:
        case = PatientCase(
            chw_id=c.get('chw_id'),
            facility_id=c.get('facility_id'),
            sex=c.get('sex'),
            age_months=c.get('age_months'),
            symptoms=c.get('symptoms'),
            vitals=c.get('vitals'),
            triage_result=c.get('triage_result'),
            risk_score=c.get('risk_score'),
            referral_note=c.get('referral_note'),
            synced=True
        )
        db.session.add(case)
        saved.append(case)
    db.session.commit()
    return jsonify({"msg": f"{len(saved)} cases synced", "synced_count": len(saved)}), 201
