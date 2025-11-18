# backend/utils/rules_engine.py
def run_rules(age_months, symptoms: dict, vitals: dict):
    """
    Simple rule-based triage hint:
    - urgent: danger signs (difficulty breathing, unconscious, severe dehydration, temp > 39.5 for infants, etc)
    - non-urgent: common cough/cold without danger signs
    """
    # Danger signs
    if symptoms.get('difficulty_breathing') or symptoms.get('convulsions') or symptoms.get('unable_to_drink'):
        return 'urgent'
    temp = vitals.get('temp_c', 0) or 0
    if age_months and age_months < 2 and temp > 38.0:
        return 'urgent'
    if temp and temp >= 40:
        return 'urgent'
    # default fallback
    if symptoms.get('fever') or symptoms.get('cough'):
        return 'non-urgent'
    return 'non-urgent'
