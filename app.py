from flask import Flask, render_template_string, request
from cards_database import CREDIT_CARDS
from templates import HOME_TEMPLATE, RESULTS_TEMPLATE
import json

app = Flask(__name__)

# Map income dropdown values to numeric
INCOME_MAP = {
    'under_30k': 20000,
    '30k_50k': 40000,
    '50k_75k': 62500,
    '75k_100k': 87500,
    '100k_plus': 150000,
}

# Map credit score dropdown values to numeric
CREDIT_SCORE_MAP = {
    'none': 0,
    'poor': 450,
    'fair': 620,
    'good': 700,
    'very_good': 770,
    'excellent': 825,
}

CREDIT_SCORE_LABELS = {
    'none': 'No Credit History',
    'poor': 'Poor (300\u2013579)',
    'fair': 'Fair (580\u2013669)',
    'good': 'Good (670\u2013739)',
    'very_good': 'Very Good (740\u2013799)',
    'excellent': 'Excellent (800\u2013850)',
}


@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)


@app.route('/recommend', methods=['POST'])
def recommend():
    # Parse inputs
    age = int(request.form.get('age', 18))
    income_key = request.form.get('income', 'under_30k')
    credit_key = request.form.get('credit_score', 'none')
    income = INCOME_MAP.get(income_key, 20000)
    credit_score = CREDIT_SCORE_MAP.get(credit_key, 0)
    credit_label = CREDIT_SCORE_LABELS.get(credit_key, 'Unknown')

    # Spending (monthly amounts)
    spending = {
        'dining': float(request.form.get('dining', 0) or 0),
        'grocery': float(request.form.get('grocery', 0) or 0),
        'gas': float(request.form.get('gas', 0) or 0),
        'travel': float(request.form.get('travel', 0) or 0),
        'streaming': float(request.form.get('streaming', 0) or 0),
        'shopping': float(request.form.get('shopping', 0) or 0),
        'other': float(request.form.get('other', 0) or 0),
    }
    total_monthly = sum(spending.values())

    warning = None
    if credit_score == 0:
        warning = "No credit history detected \u2014 we're showing cards that help build credit. Responsible card use will improve your score over time."
    elif credit_score < 580:
        warning = "With a poor credit score, your options are limited. Focus on secured cards or student cards to build your credit history."

    recommendations = []
    total_qualifying = 0

    for card in CREDIT_CARDS:
        # Eligibility checks
        if age < card['min_age']:
            continue
        if income < card['min_income']:
            continue
        if credit_score > 0 and credit_score < card['min_credit_score']:
            continue
        if credit_score == 0 and card['min_credit_score'] > 580:
            continue

        total_qualifying += 1

        # Calculate annual rewards
        annual_rewards = 0
        for category, monthly_amount in spending.items():
            if 'all' in card['rewards']:
                rate = card['rewards']['all']
            else:
                rate = card['rewards'].get(category, card['rewards'].get('other', 1))
            annual_rewards += monthly_amount * 12 * (rate / 100)

        # Calculate values
        first_year_value = annual_rewards + card['signup_bonus'] - card['annual_fee']
        ongoing_value = annual_rewards - card['annual_fee']

        # Calculate match score (how well this card fits the user's spending)
        match_score = _calculate_match_score(card, spending)

        # Build flat reward rates for template/comparison
        def get_rate(cat, c=card):
            if 'all' in c['rewards']:
                return c['rewards']['all']
            return c['rewards'].get(cat, c['rewards'].get('other', 1))

        rec = dict(card)
        rec['annual_rewards'] = round(annual_rewards, 2)
        rec['first_year_value'] = round(first_year_value, 2)
        rec['ongoing_value'] = round(ongoing_value, 2)
        rec['match_score'] = match_score
        rec['dining_rate'] = get_rate('dining')
        rec['grocery_rate'] = get_rate('grocery')
        rec['gas_rate'] = get_rate('gas')
        rec['travel_rate'] = get_rate('travel')
        rec['streaming_rate'] = get_rate('streaming')
        rec['shopping_rate'] = get_rate('shopping')
        rec['other_rate'] = get_rate('other')
        recommendations.append(rec)

    # Sort by first year value
    recommendations.sort(key=lambda x: x['first_year_value'], reverse=True)
    top5 = recommendations[:5]

    # Build comparison data for JavaScript
    comparison_data = []
    for i, rec in enumerate(top5):
        comparison_data.append({
            'index': i,
            'name': rec['name'],
            'issuer': rec['issuer'],
            'annual_fee': rec['annual_fee'],
            'signup_bonus': rec['signup_bonus'],
            'dining_rate': rec['dining_rate'],
            'grocery_rate': rec['grocery_rate'],
            'gas_rate': rec['gas_rate'],
            'travel_rate': rec['travel_rate'],
            'streaming_rate': rec['streaming_rate'],
            'shopping_rate': rec['shopping_rate'],
            'other_rate': rec['other_rate'],
            'first_year_value': rec['first_year_value'],
            'ongoing_value': rec['ongoing_value'],
            'no_foreign_fee': rec['no_foreign_fee'],
            'card_gradient': rec['card_gradient'],
            'card_text_color': rec['card_text_color'],
            'network': rec['network'],
        })

    max_annual = max((r['annual_rewards'] for r in top5), default=0)

    return render_template_string(
        RESULTS_TEMPLATE,
        recommendations=top5,
        all_recommendations=recommendations,
        total_monthly=total_monthly,
        max_annual=max_annual,
        warning=warning,
        credit_label=credit_label,
        total_qualifying=total_qualifying,
        spending=spending,
        comparison_json=json.dumps(comparison_data),
    )


def _calculate_match_score(card, spending):
    total = sum(spending.values())
    if total == 0:
        return 75
    # Perfect card rates for normalization
    perfect = {'dining': 4, 'grocery': 6, 'gas': 3, 'travel': 5, 'streaming': 6, 'shopping': 5, 'other': 2}
    card_rewards = 0
    perfect_rewards = 0
    for cat, amt in spending.items():
        if 'all' in card['rewards']:
            rate = card['rewards']['all']
        else:
            rate = card['rewards'].get(cat, card['rewards'].get('other', 1))
        card_rewards += amt * rate
        perfect_rewards += amt * perfect.get(cat, 2)
    if perfect_rewards == 0:
        return 75
    score = int((card_rewards / perfect_rewards) * 100)
    return max(40, min(99, score))


if __name__ == '__main__':
    app.run(debug=True)
