HOME_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CardMatch &mdash; Find Your Perfect Credit Card</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --navy: #1a1f36;
    --blue: #3d4eac;
    --green: #00c853;
    --gray-50: #f8f9fa;
    --gray-100: #f0f2f5;
    --gray-400: #9ca3af;
    --gray-600: #6b7280;
    --gray-900: #111827;
  }
  body { font-family: 'Inter', sans-serif; background: var(--gray-50); color: var(--gray-900); min-height: 100vh; }

  /* HEADER */
  .header {
    position: sticky; top: 0; z-index: 100;
    background: #fff; border-bottom: 1px solid #e5e7eb;
    padding: 0 24px; height: 64px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  .logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
  .logo-icon {
    width: 36px; height: 36px; background: var(--navy); border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
  }
  .logo-text { font-size: 20px; font-weight: 700; color: var(--navy); }
  .header-tagline { font-size: 13px; color: var(--gray-600); font-weight: 500; }

  /* HERO */
  .hero {
    background: linear-gradient(135deg, var(--navy) 0%, #2d3561 100%);
    padding: 72px 24px 80px;
    text-align: center;
    color: #fff;
  }
  .hero h1 {
    font-size: clamp(28px, 5vw, 48px);
    font-weight: 700; line-height: 1.2;
    max-width: 720px; margin: 0 auto 16px;
    letter-spacing: -0.5px;
  }
  .hero p {
    font-size: 17px; color: rgba(255,255,255,0.82);
    max-width: 560px; margin: 0 auto 32px;
    line-height: 1.6;
  }
  .trust-badges {
    display: flex; justify-content: center; gap: 32px; flex-wrap: wrap;
    margin-top: 8px;
  }
  .badge {
    display: flex; align-items: center; gap: 8px;
    font-size: 14px; color: rgba(255,255,255,0.9); font-weight: 500;
  }

  /* FORM CARD */
  .form-wrap { max-width: 600px; margin: -40px auto 60px; padding: 0 16px; }
  .form-card {
    background: #fff; border-radius: 16px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.12);
    overflow: hidden;
  }

  /* STEP INDICATOR */
  .step-header { padding: 24px 32px 0; }
  .step-label {
    font-size: 13px; font-weight: 600; color: var(--blue);
    text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;
  }
  .progress-track {
    height: 4px; background: var(--gray-100); border-radius: 2px; overflow: hidden;
  }
  .progress-bar {
    height: 100%; background: var(--blue); border-radius: 2px;
    transition: width 0.4s ease; width: 50%;
  }

  /* STEP BODY */
  .step-body { padding: 28px 32px 32px; }
  .field-group { margin-bottom: 20px; }
  .field-label {
    display: block; font-size: 14px; font-weight: 600;
    color: var(--navy); margin-bottom: 6px;
  }
  .field-input {
    width: 100%; padding: 12px 14px; font-size: 15px; font-family: 'Inter', sans-serif;
    border: 2px solid #e5e7eb; border-radius: 8px; outline: none;
    transition: border-color 0.2s;
    color: var(--gray-900); background: #fff;
    -webkit-appearance: none; -moz-appearance: textfield; appearance: none;
  }
  input[type=number].field-input::-webkit-inner-spin-button,
  input[type=number].field-input::-webkit-outer-spin-button { -webkit-appearance: none; }
  .field-input:focus { border-color: var(--blue); }
  .field-input.input-error { border-color: #ef4444; }
  .field-error { font-size: 12px; color: #ef4444; margin-top: 4px; min-height: 16px; }

  /* SPENDING GRID */
  .spending-hint { font-size: 13px; color: var(--gray-600); margin-bottom: 20px; line-height: 1.5; }
  .spending-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  @media (max-width: 480px) { .spending-grid { grid-template-columns: 1fr; } }

  .input-group {
    display: flex; align-items: center;
    border: 2px solid #e5e7eb; border-radius: 8px; overflow: hidden;
    transition: border-color 0.2s;
  }
  .input-group:focus-within { border-color: var(--blue); }
  .input-prefix {
    padding: 12px 10px 12px 14px; font-size: 15px; font-weight: 600;
    color: var(--gray-600); background: var(--gray-50);
    border-right: 2px solid #e5e7eb; white-space: nowrap;
    user-select: none;
  }
  .input-group .field-input {
    border: none; border-radius: 0; flex: 1; margin: 0;
    padding: 12px 14px;
  }
  .input-group .field-input:focus { border: none; outline: none; }
  .field-icon { font-size: 15px; margin-right: 2px; }

  /* SPENDING TOTAL */
  .spending-total {
    margin-top: 20px; padding: 14px 16px;
    background: var(--gray-50); border-radius: 8px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .spending-total-label { font-size: 14px; color: var(--gray-600); font-weight: 500; }
  .spending-total-value { font-size: 18px; font-weight: 700; color: var(--navy); }

  /* BUTTONS */
  .btn-row { display: flex; justify-content: flex-end; gap: 12px; margin-top: 28px; align-items: center; }
  .btn-back {
    background: none; border: none; font-size: 14px; font-weight: 600;
    color: var(--gray-600); cursor: pointer; padding: 10px 0;
    display: flex; align-items: center; gap: 6px;
    font-family: 'Inter', sans-serif;
  }
  .btn-back:hover { color: var(--navy); }
  .btn-primary {
    background: var(--navy); color: #fff; border: none;
    padding: 14px 28px; border-radius: 8px; font-size: 15px; font-weight: 600;
    cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif;
    display: flex; align-items: center; gap: 8px;
  }
  .btn-primary:hover { background: #252d4a; transform: translateY(-1px); box-shadow: 0 4px 16px rgba(26,31,54,0.25); }
  .btn-primary:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }

  /* SPINNER */
  .spinner {
    width: 16px; height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    display: inline-block;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* FOOTER */
  .footer { text-align: center; padding: 32px 24px; color: var(--gray-400); font-size: 13px; }
</style>
</head>
<body>

<header class="header">
  <a class="logo" href="/">
    <div class="logo-icon">&#x1F4B3;</div>
    <span class="logo-text">CardMatch</span>
  </a>
  <span class="header-tagline">Free &bull; No Credit Check</span>
</header>

<section class="hero">
  <h1>Find Your Perfect Credit Card in 60 Seconds</h1>
  <p>Answer a few questions about your spending and we&rsquo;ll match you with the cards that maximize your rewards.</p>
  <div class="trust-badges">
    <span class="badge">&#x1F512; No credit check required</span>
    <span class="badge">&#x26A1; Takes 60 seconds</span>
    <span class="badge">&#x2713; 100% free</span>
  </div>
</section>

<div class="form-wrap">
  <div class="form-card">
    <form id="mainForm" action="/recommend" method="POST">

      <!-- STEP 1 -->
      <div id="step1">
        <div class="step-header">
          <div class="step-label" id="stepLabel">Step 1 of 2 &mdash; Personal Info</div>
          <div class="progress-track">
            <div class="progress-bar" id="progressBar" style="width:50%"></div>
          </div>
        </div>
        <div class="step-body">

          <div class="field-group">
            <label class="field-label" for="age">Your Age</label>
            <input class="field-input" type="number" id="age" name="age"
              min="18" max="100" placeholder="e.g. 25" required>
            <div class="field-error" id="age_error"></div>
          </div>

          <div class="field-group">
            <label class="field-label" for="income">Annual Income</label>
            <select class="field-input" id="income" name="income">
              <option value="" disabled selected>Select your income range</option>
              <option value="under_30k">Under $30,000</option>
              <option value="30k_50k">$30,000 &ndash; $50,000</option>
              <option value="50k_75k">$50,000 &ndash; $75,000</option>
              <option value="75k_100k">$75,000 &ndash; $100,000</option>
              <option value="100k_plus">$100,000+</option>
            </select>
            <div class="field-error" id="income_error"></div>
          </div>

          <div class="field-group">
            <label class="field-label" for="credit_score">Credit Score</label>
            <select class="field-input" id="credit_score" name="credit_score">
              <option value="" disabled selected>Select your credit score</option>
              <option value="none">No Credit History</option>
              <option value="poor">Poor (300&ndash;579)</option>
              <option value="fair">Fair (580&ndash;669)</option>
              <option value="good">Good (670&ndash;739)</option>
              <option value="very_good">Very Good (740&ndash;799)</option>
              <option value="excellent">Excellent (800&ndash;850)</option>
            </select>
            <div class="field-error" id="credit_error"></div>
          </div>

          <div class="btn-row">
            <button type="button" class="btn-primary" onclick="nextStep()">
              Continue to Spending &rarr;
            </button>
          </div>

        </div>
      </div>

      <!-- STEP 2 -->
      <div id="step2" style="display:none">
        <div class="step-header">
          <div class="step-label">Step 2 of 2 &mdash; Monthly Spending</div>
          <div class="progress-track">
            <div class="progress-bar" style="width:100%"></div>
          </div>
        </div>
        <div class="step-body">
          <p class="spending-hint">Enter your average monthly spending in each category. Leave blank or enter 0 if you don&rsquo;t spend in that category.</p>

          <div class="spending-grid">

            <div class="field-group">
              <label class="field-label"><span class="field-icon">&#x1F37D;&#xFE0F;</span> Dining &amp; Restaurants</label>
              <div class="input-group">
                <div class="input-prefix">$</div>
                <input class="field-input" type="number" id="dining" name="dining"
                  min="0" step="1" placeholder="200" oninput="updateTotal()">
              </div>
            </div>

            <div class="field-group">
              <label class="field-label"><span class="field-icon">&#x1F6D2;</span> Groceries</label>
              <div class="input-group">
                <div class="input-prefix">$</div>
                <input class="field-input" type="number" id="grocery" name="grocery"
                  min="0" step="1" placeholder="400" oninput="updateTotal()">
              </div>
            </div>

            <div class="field-group">
              <label class="field-label"><span class="field-icon">&#x26FD;</span> Gas &amp; Transportation</label>
              <div class="input-group">
                <div class="input-prefix">$</div>
                <input class="field-input" type="number" id="gas" name="gas"
                  min="0" step="1" placeholder="150" oninput="updateTotal()">
              </div>
            </div>

            <div class="field-group">
              <label class="field-label"><span class="field-icon">&#x2708;&#xFE0F;</span> Travel &amp; Hotels</label>
              <div class="input-group">
                <div class="input-prefix">$</div>
                <input class="field-input" type="number" id="travel" name="travel"
                  min="0" step="1" placeholder="100" oninput="updateTotal()">
              </div>
            </div>

            <div class="field-group">
              <label class="field-label"><span class="field-icon">&#x1F4FA;</span> Streaming &amp; Subscriptions</label>
              <div class="input-group">
                <div class="input-prefix">$</div>
                <input class="field-input" type="number" id="streaming" name="streaming"
                  min="0" step="1" placeholder="50" oninput="updateTotal()">
              </div>
            </div>

            <div class="field-group">
              <label class="field-label"><span class="field-icon">&#x1F6CD;&#xFE0F;</span> Online Shopping</label>
              <div class="input-group">
                <div class="input-prefix">$</div>
                <input class="field-input" type="number" id="shopping" name="shopping"
                  min="0" step="1" placeholder="200" oninput="updateTotal()">
              </div>
            </div>

            <div class="field-group">
              <label class="field-label"><span class="field-icon">&#x1F4B3;</span> Other Expenses</label>
              <div class="input-group">
                <div class="input-prefix">$</div>
                <input class="field-input" type="number" id="other" name="other"
                  min="0" step="1" placeholder="300" oninput="updateTotal()">
              </div>
            </div>

          </div>

          <div class="spending-total">
            <span class="spending-total-label">Estimated monthly spending</span>
            <span class="spending-total-value" id="spendingTotal">$0</span>
          </div>

          <div class="btn-row">
            <button type="button" class="btn-back" onclick="prevStep()">
              &larr; Back
            </button>
            <button type="submit" class="btn-primary" id="submitBtn">
              Find My Cards &rarr;
            </button>
          </div>

        </div>
      </div>

    </form>
  </div>
</div>

<footer class="footer">
  <p>&copy; 2025 CardMatch. For educational purposes only.</p>
</footer>

<script>
function nextStep() {
  var age = document.getElementById('age').value;
  var income = document.getElementById('income').value;
  var credit = document.getElementById('credit_score').value;
  var valid = true;

  if (!age || parseInt(age) < 18 || parseInt(age) > 100) {
    document.getElementById('age_error').textContent = 'Please enter a valid age (18\u2013100)';
    document.getElementById('age').classList.add('input-error');
    valid = false;
  } else {
    document.getElementById('age_error').textContent = '';
    document.getElementById('age').classList.remove('input-error');
  }

  if (!income) {
    document.getElementById('income_error').textContent = 'Please select your income range';
    document.getElementById('income').classList.add('input-error');
    valid = false;
  } else {
    document.getElementById('income_error').textContent = '';
    document.getElementById('income').classList.remove('input-error');
  }

  if (!credit) {
    document.getElementById('credit_error').textContent = 'Please select your credit score range';
    document.getElementById('credit_score').classList.add('input-error');
    valid = false;
  } else {
    document.getElementById('credit_error').textContent = '';
    document.getElementById('credit_score').classList.remove('input-error');
  }

  if (valid) {
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'block';
    document.getElementById('progressBar').style.width = '100%';
    document.getElementById('stepLabel').textContent = 'Step 2 of 2 \u2014 Monthly Spending';
    window.scrollTo(0, 0);
  }
}

function prevStep() {
  document.getElementById('step2').style.display = 'none';
  document.getElementById('step1').style.display = 'block';
  document.getElementById('progressBar').style.width = '50%';
  document.getElementById('stepLabel').textContent = 'Step 1 of 2 \u2014 Personal Info';
  window.scrollTo(0, 0);
}

function updateTotal() {
  var fields = ['dining','grocery','gas','travel','streaming','shopping','other'];
  var total = 0;
  fields.forEach(function(f) {
    total += parseFloat(document.getElementById(f).value || 0);
  });
  document.getElementById('spendingTotal').textContent = '$' + total.toLocaleString('en-US', {minimumFractionDigits:0, maximumFractionDigits:0});
}

document.getElementById('mainForm').addEventListener('submit', function() {
  var btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Analyzing your profile...';
});
</script>

</body>
</html>
'''


RESULTS_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Your Card Matches &mdash; CardMatch</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --navy: #1a1f36;
    --blue: #3d4eac;
    --green: #00c853;
    --gray-50: #f8f9fa;
    --gray-100: #f0f2f5;
    --gray-400: #9ca3af;
    --gray-600: #6b7280;
    --gray-900: #111827;
  }
  body { font-family: 'Inter', sans-serif; background: var(--gray-50); color: var(--gray-900); }

  /* HEADER */
  .header {
    position: sticky; top: 0; z-index: 200;
    background: #fff; border-bottom: 1px solid #e5e7eb;
    padding: 0 24px; height: 64px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  .logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
  .logo-icon {
    width: 36px; height: 36px; background: var(--navy); border-radius: 8px;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
  }
  .logo-text { font-size: 20px; font-weight: 700; color: var(--navy); }
  .start-over {
    font-size: 14px; font-weight: 600; color: var(--blue);
    text-decoration: none; display: flex; align-items: center; gap: 6px;
  }
  .start-over:hover { text-decoration: underline; }

  /* WARNING */
  .warning-banner {
    background: #fffbeb; border: 1px solid #f59e0b; border-radius: 8px;
    padding: 14px 20px; margin: 20px auto; max-width: 900px;
    display: flex; align-items: flex-start; gap: 12px; font-size: 14px; color: #92400e;
  }
  .warning-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }

  /* STATS BAR */
  .stats-bar {
    background: var(--navy); color: #fff; padding: 28px 24px;
  }
  .stats-inner { max-width: 900px; margin: 0 auto; }
  .stats-title { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
  .stats-sub { font-size: 14px; color: rgba(255,255,255,0.7); margin-bottom: 20px; }
  .stats-boxes { display: flex; gap: 16px; flex-wrap: wrap; }
  .stat-box {
    background: rgba(255,255,255,0.1); border-radius: 10px;
    padding: 14px 20px; min-width: 160px;
  }
  .stat-box-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: rgba(255,255,255,0.6); margin-bottom: 4px; }
  .stat-box-value { font-size: 20px; font-weight: 700; color: #fff; }

  /* TOOLBAR */
  .toolbar {
    background: #fff; border-bottom: 1px solid #e5e7eb;
    padding: 14px 24px;
    display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
  }
  .toolbar-inner { max-width: 900px; margin: 0 auto; width: 100%; display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }
  .sort-select {
    padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px;
    font-size: 13px; font-family: 'Inter', sans-serif; color: var(--navy);
    background: #fff; cursor: pointer; font-weight: 500;
  }
  .filter-toggle { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; font-weight: 500; color: var(--gray-600); }
  .filter-toggle input { width: 16px; height: 16px; cursor: pointer; accent-color: var(--blue); }
  .card-count { margin-left: auto; font-size: 13px; color: var(--gray-400); }

  /* MAIN LAYOUT */
  .main { max-width: 900px; margin: 0 auto; padding: 24px 16px 80px; }

  /* CARD ITEM */
  .card-item {
    background: #fff; border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 20px; overflow: hidden;
    opacity: 0; transform: translateY(20px);
    animation: fadeSlide 0.4s ease forwards;
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .card-item:hover { box-shadow: 0 8px 32px rgba(0,0,0,0.12); transform: translateY(-2px); }
  @keyframes fadeSlide {
    to { opacity: 1; transform: translateY(0); }
  }
  .card-item:nth-child(1) { animation-delay: 0s; }
  .card-item:nth-child(2) { animation-delay: 0.08s; }
  .card-item:nth-child(3) { animation-delay: 0.16s; }
  .card-item:nth-child(4) { animation-delay: 0.24s; }
  .card-item:nth-child(5) { animation-delay: 0.32s; }

  .card-body {
    display: flex; gap: 24px; padding: 24px;
    align-items: flex-start;
  }
  @media (max-width: 640px) {
    .card-body { flex-direction: column; }
    .card-visual-wrap { width: 100% !important; }
    .card-visual { width: 100% !important; max-width: 280px; margin: 0 auto; }
  }

  /* MINI CREDIT CARD VISUAL */
  .card-visual-wrap { width: 180px; flex-shrink: 0; }
  .card-visual {
    width: 100%; aspect-ratio: 1.586;
    border-radius: 12px; padding: 16px;
    display: flex; flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    position: relative; overflow: hidden;
  }
  .card-chip {
    width: 28px; height: 20px; background: #d4a017;
    border-radius: 4px;
  }
  .card-dots {
    display: flex; gap: 5px; align-items: center;
  }
  .card-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: rgba(255,255,255,0.7);
  }
  .card-dot-group { display: flex; gap: 3px; }
  .card-bottom {
    display: flex; justify-content: space-between; align-items: flex-end;
  }
  .card-name-visual {
    font-size: 8px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.3px;
    max-width: 100px; line-height: 1.3;
  }
  .card-network {
    font-size: 9px; font-weight: 700; opacity: 0.9;
  }

  /* CARD DETAILS */
  .card-details { flex: 1; min-width: 0; }
  .card-top-row {
    display: flex; align-items: flex-start; justify-content: space-between;
    gap: 12px; margin-bottom: 10px; flex-wrap: wrap;
  }
  .card-name-text { font-size: 19px; font-weight: 700; color: var(--navy); line-height: 1.2; }
  .match-badge {
    background: #e8f5e9; color: #1b5e20; font-size: 12px; font-weight: 700;
    padding: 4px 10px; border-radius: 20px; white-space: nowrap; flex-shrink: 0;
  }
  .best-for-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--gray-100); color: var(--gray-600);
    font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 6px;
    margin-bottom: 10px;
  }
  .meta-row {
    display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 12px; align-items: center;
  }
  .fee-badge {
    font-size: 14px; font-weight: 700;
  }
  .fee-free { color: var(--green); }
  .fee-paid { color: var(--gray-900); }
  .bonus-text { font-size: 13px; color: var(--gray-600); }
  .bonus-text strong { color: var(--navy); }

  /* REWARDS GRID */
  .rewards-grid {
    display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px;
  }
  .reward-pill {
    display: flex; align-items: center; gap: 4px;
    padding: 4px 10px; border-radius: 6px;
    font-size: 12px; font-weight: 600;
    background: var(--gray-100); color: var(--gray-900);
  }
  .reward-pill.highlight {
    background: #e3f2fd; color: #0d47a1;
  }
  .reward-pill.top-rate {
    background: #e8f5e9; color: #1b5e20;
  }

  /* VALUE BOXES */
  .value-row {
    display: flex; gap: 12px; margin-bottom: 14px; flex-wrap: wrap;
  }
  .value-box {
    padding: 12px 16px; border-radius: 8px; flex: 1; min-width: 140px;
  }
  .value-box-primary {
    background: #e8f5e9;
  }
  .value-box-secondary { background: var(--gray-100); }
  .value-box-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.4px; color: var(--gray-600); margin-bottom: 4px; font-weight: 600; }
  .value-box-amount {
    font-size: 20px; font-weight: 700;
  }
  .value-box-primary .value-box-amount { color: #1b5e20; }
  .value-box-secondary .value-box-amount { color: var(--navy); }

  /* PERKS */
  .perks-list { list-style: none; margin-bottom: 16px; }
  .perks-list li {
    display: flex; align-items: flex-start; gap: 8px;
    font-size: 13px; color: var(--gray-600); padding: 3px 0; line-height: 1.4;
  }
  .perk-check { color: var(--green); font-weight: 700; flex-shrink: 0; }

  /* ACTION ROW */
  .action-row {
    display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
  }
  .btn-apply {
    background: var(--navy); color: #fff; border: none;
    padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600;
    cursor: pointer; text-decoration: none; display: inline-block;
    transition: background 0.2s, transform 0.15s;
    font-family: 'Inter', sans-serif;
  }
  .btn-apply:hover { background: #252d4a; transform: translateY(-1px); }
  .btn-why {
    background: none; border: 1px solid #d1d5db;
    padding: 10px 16px; border-radius: 8px; font-size: 13px; font-weight: 600;
    color: var(--gray-600); cursor: pointer; transition: all 0.15s;
    font-family: 'Inter', sans-serif;
  }
  .btn-why:hover { border-color: var(--blue); color: var(--blue); }
  .compare-check {
    margin-left: auto; display: flex; align-items: center; gap: 6px;
    font-size: 13px; color: var(--gray-600); cursor: pointer; white-space: nowrap;
  }
  .compare-check input { width: 15px; height: 15px; cursor: pointer; accent-color: var(--blue); }

  /* WHY SECTION */
  .why-section {
    display: none; border-top: 1px solid #e5e7eb;
    padding: 20px 24px; background: var(--gray-50);
  }
  .why-section.open { display: block; }
  .why-title { font-size: 14px; font-weight: 700; color: var(--navy); margin-bottom: 8px; }
  .why-text { font-size: 14px; color: var(--gray-600); line-height: 1.6; }

  /* FLOATING COMPARE BTN */
  .float-compare {
    position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%);
    background: var(--blue); color: #fff;
    padding: 14px 28px; border-radius: 32px; font-size: 15px; font-weight: 700;
    box-shadow: 0 4px 24px rgba(61,78,172,0.45); cursor: pointer; border: none;
    transition: all 0.2s; display: none; z-index: 150;
    font-family: 'Inter', sans-serif;
  }
  .float-compare:hover { background: #2d3a8c; transform: translateX(-50%) translateY(-2px); }
  .float-compare.visible { display: block; }

  /* MODAL */
  .modal-overlay {
    display: none; position: fixed; inset: 0; z-index: 300;
    background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
    overflow-y: auto;
  }
  .modal-overlay.open { display: flex; align-items: flex-start; justify-content: center; padding: 40px 16px; }
  .modal {
    background: #fff; border-radius: 16px; width: 100%; max-width: 860px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2); overflow: hidden;
  }
  .modal-header {
    padding: 20px 24px; background: var(--navy); color: #fff;
    display: flex; align-items: center; justify-content: space-between;
  }
  .modal-title { font-size: 18px; font-weight: 700; }
  .modal-close {
    background: rgba(255,255,255,0.15); border: none; color: #fff;
    width: 32px; height: 32px; border-radius: 6px; cursor: pointer;
    font-size: 18px; display: flex; align-items: center; justify-content: center;
    font-family: 'Inter', sans-serif;
  }
  .modal-close:hover { background: rgba(255,255,255,0.25); }
  .modal-body { padding: 24px; overflow-x: auto; }
  .compare-table {
    width: 100%; border-collapse: collapse; font-size: 13px;
    min-width: 500px;
  }
  .compare-table th {
    padding: 10px 14px; text-align: left; background: var(--gray-50);
    border-bottom: 2px solid #e5e7eb; font-weight: 700; font-size: 12px;
    color: var(--navy); white-space: nowrap;
  }
  .compare-table td {
    padding: 10px 14px; border-bottom: 1px solid #f0f2f5; color: var(--gray-900); vertical-align: middle;
  }
  .compare-table tr:last-child td { border-bottom: none; }
  .compare-table .row-label {
    font-weight: 600; color: var(--gray-600); font-size: 12px;
    text-transform: uppercase; letter-spacing: 0.3px; white-space: nowrap;
    background: var(--gray-50);
  }
  .cell-winner { background: #e8f5e9; font-weight: 700; color: #1b5e20; border-radius: 4px; }
  .modal-footer { padding: 16px 24px; border-top: 1px solid #e5e7eb; display: flex; justify-content: flex-end; }
  .btn-close-modal {
    background: var(--gray-100); border: none; padding: 10px 20px;
    border-radius: 8px; font-size: 14px; font-weight: 600;
    color: var(--gray-900); cursor: pointer; font-family: 'Inter', sans-serif;
  }
  .btn-close-modal:hover { background: #e5e7eb; }

  /* FOOTER */
  .page-footer {
    max-width: 900px; margin: 0 auto; padding: 0 16px 40px;
  }
  .disclaimer {
    background: #fff; border-radius: 10px; padding: 16px 20px;
    font-size: 12px; color: var(--gray-400); line-height: 1.6;
    border: 1px solid #e5e7eb;
  }
  .footer-links {
    text-align: center; margin-top: 16px; font-size: 12px; color: var(--gray-400);
  }
  .footer-links a { color: var(--gray-400); text-decoration: none; margin: 0 8px; }
  .footer-links a:hover { color: var(--gray-600); }
</style>
</head>
<body>

<header class="header">
  <a class="logo" href="/">
    <div class="logo-icon">&#x1F4B3;</div>
    <span class="logo-text">CardMatch</span>
  </a>
  <a class="start-over" href="/">&larr; Start Over</a>
</header>

{% if warning %}
<div style="padding: 0 16px; max-width: 900px; margin: 0 auto;">
  <div class="warning-banner">
    <span class="warning-icon">&#x26A0;&#xFE0F;</span>
    <span>{{ warning }}</span>
  </div>
</div>
{% endif %}

<div class="stats-bar">
  <div class="stats-inner">
    <div class="stats-title">Your Top Card Matches</div>
    <div class="stats-sub">Based on ${{ "{:,.0f}".format(total_monthly) }}/month in spending across {{ spending.values() | select("greaterthan", 0) | list | length }} categories</div>
    <div class="stats-boxes">
      <div class="stat-box">
        <div class="stat-box-label">Qualifying Cards</div>
        <div class="stat-box-value">{{ total_qualifying }}</div>
      </div>
      {% if recommendations %}
      <div class="stat-box">
        <div class="stat-box-label">Max First-Year Value</div>
        <div class="stat-box-value">${{ "{:,.0f}".format(recommendations[0].first_year_value) }}</div>
      </div>
      {% endif %}
      <div class="stat-box">
        <div class="stat-box-label">Credit Profile</div>
        <div class="stat-box-value" style="font-size:15px;">{{ credit_label }}</div>
      </div>
    </div>
  </div>
</div>

<div class="toolbar">
  <div class="toolbar-inner">
    <select class="sort-select" id="sortSelect" onchange="applyFilters()">
      <option value="first_year">Sort by: Best Match (First-Year Value)</option>
      <option value="ongoing">Ongoing Value</option>
      <option value="fee">Lowest Fee</option>
      <option value="bonus">Highest Bonus</option>
    </select>
    <label class="filter-toggle">
      <input type="checkbox" id="noFeeFilter" onchange="applyFilters()">
      No Annual Fee Only
    </label>
    <span class="card-count" id="cardCount">Showing {{ recommendations|length }} of {{ total_qualifying }} qualifying cards</span>
  </div>
</div>

<div class="main">
  <div id="cardsGrid">
    {% for card in recommendations %}
    <div class="card-item"
      data-index="{{ loop.index0 }}"
      data-annual-fee="{{ card.annual_fee }}"
      data-first-year="{{ card.first_year_value }}"
      data-ongoing="{{ card.ongoing_value }}"
      data-bonus="{{ card.signup_bonus }}"
      data-match="{{ card.match_score }}"
      data-no-fee="{{ 'true' if card.annual_fee == 0 else 'false' }}"
    >
      <div class="card-body">
        <!-- MINI CARD VISUAL -->
        <div class="card-visual-wrap">
          <div class="card-visual" style="background: {{ card.card_gradient }}; color: {{ card.card_text_color }};">
            <div class="card-chip"></div>
            <div class="card-dots">
              <div class="card-dot-group">
                <div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div>
              </div>
              <div class="card-dot-group">
                <div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div>
              </div>
              <div class="card-dot-group">
                <div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div>
              </div>
              <div class="card-dot-group">
                <div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div><div class="card-dot"></div>
              </div>
            </div>
            <div class="card-bottom">
              <div class="card-name-visual">{{ card.name }}</div>
              <div class="card-network">{{ card.network }}</div>
            </div>
          </div>
        </div>

        <!-- CARD DETAILS -->
        <div class="card-details">
          <div class="card-top-row">
            <div class="card-name-text">{{ card.name }}</div>
            <span class="match-badge">{{ card.match_score }}% match</span>
          </div>

          <div class="best-for-badge">{{ card.best_for_icon }} {{ card.best_for }}</div>

          <div class="meta-row">
            {% if card.annual_fee == 0 %}
            <span class="fee-badge fee-free">$0/yr &mdash; No Annual Fee</span>
            {% else %}
            <span class="fee-badge fee-paid">${{ card.annual_fee }}/yr</span>
            {% endif %}

            {% if card.id == 'discover-it-cash-back' %}
            <span class="bonus-text">&#x2728; <strong>Cashback Match&trade;</strong> &mdash; doubles all first-year rewards</span>
            {% elif card.id == 'apple-card' %}
            <span class="bonus-text">No traditional signup bonus</span>
            {% elif card.bonus_spend == 0 and card.signup_bonus > 0 %}
            <span class="bonus-text"><strong>${{ card.signup_bonus }}</strong> bonus upon approval</span>
            {% elif card.signup_bonus > 0 %}
            <span class="bonus-text">Earn <strong>${{ card.signup_bonus }}</strong> after ${{ "{:,}".format(card.bonus_spend) }} in {{ card.bonus_timeframe }}</span>
            {% endif %}
          </div>

          <!-- REWARDS PILLS -->
          <div class="rewards-grid">
            {% set rates = [
              ('dining', card.dining_rate, '🍽️'),
              ('grocery', card.grocery_rate, '🛒'),
              ('gas', card.gas_rate, '⛽'),
              ('travel', card.travel_rate, '✈️'),
              ('streaming', card.streaming_rate, '📺'),
              ('shopping', card.shopping_rate, '🛍️'),
              ('other', card.other_rate, '💳'),
            ] %}
            {% set max_rate = [card.dining_rate, card.grocery_rate, card.gas_rate, card.travel_rate, card.streaming_rate, card.shopping_rate, card.other_rate] | max %}
            {% for cat, rate, icon in rates %}
            {% if spending[cat] > 0 %}
            <span class="reward-pill {% if rate == max_rate and rate >= 3 %}top-rate{% elif rate >= 2 %}highlight{% endif %}">
              {{ icon }} {{ rate }}% {{ cat }}
            </span>
            {% endif %}
            {% endfor %}
            {% set cats_with_spending = namespace(count=0) %}
            {% for cat, rate, icon in rates %}{% if spending[cat] > 0 %}{% set cats_with_spending.count = cats_with_spending.count + 1 %}{% endif %}{% endfor %}
            {% if cats_with_spending.count == 0 %}
            <span class="reward-pill highlight">{{ max_rate }}% base rate</span>
            {% endif %}
          </div>

          <!-- VALUE BOXES -->
          <div class="value-row">
            <div class="value-box value-box-primary">
              <div class="value-box-label">First-Year Value</div>
              <div class="value-box-amount">${{ "{:,.0f}".format(card.first_year_value) }}</div>
            </div>
            <div class="value-box value-box-secondary">
              <div class="value-box-label">Ongoing Value</div>
              <div class="value-box-amount">${{ "{:,.0f}".format(card.ongoing_value) }}/yr</div>
            </div>
          </div>

          <!-- TOP PERKS -->
          <ul class="perks-list">
            {% for perk in card.perks[:3] %}
            <li><span class="perk-check">&#x2713;</span> {{ perk }}</li>
            {% endfor %}
          </ul>

          <!-- ACTIONS -->
          <div class="action-row">
            <a class="btn-apply" href="{{ card.apply_link }}" target="_blank" rel="noopener noreferrer">Apply Now &rarr;</a>
            <button class="btn-why" onclick="toggleWhy(this)">&#x25BC; Why This Card?</button>
            <label class="compare-check">
              <input type="checkbox" class="compare-cb" data-idx="{{ loop.index0 }}" onchange="handleCompare(this)">
              Add to Compare
            </label>
          </div>
        </div>
      </div>

      <!-- WHY SECTION -->
      <div class="why-section" id="why-{{ loop.index0 }}">
        <div class="why-title">Why we recommend the {{ card.name }}</div>
        <div class="why-text" id="why-text-{{ loop.index0 }}"></div>
      </div>
    </div>
    {% endfor %}
  </div>

  {% if not recommendations %}
  <div style="text-align:center; padding: 60px 24px; color: var(--gray-600);">
    <div style="font-size: 48px; margin-bottom: 16px;">&#x1F615;</div>
    <div style="font-size: 20px; font-weight: 700; color: var(--navy); margin-bottom: 8px;">No matching cards found</div>
    <div style="margin-bottom: 24px;">Try adjusting your credit score or income to see more options.</div>
    <a href="/" style="color: var(--blue); font-weight: 600; text-decoration: none;">&larr; Start over</a>
  </div>
  {% endif %}
</div>

<div class="page-footer">
  <div class="disclaimer">
    <strong>Disclaimer:</strong> CardMatch is for educational purposes only. We are not financial advisors. All card information is subject to change &mdash; please verify current terms on the issuer&rsquo;s official website before applying. Credit card approval is not guaranteed.
  </div>
  <div class="footer-links">
    <a href="#">About</a> &bull;
    <a href="#">How It Works</a> &bull;
    <a href="#">Privacy Policy</a>
  </div>
</div>

<!-- FLOATING COMPARE BUTTON -->
<button class="float-compare" id="floatCompareBtn" onclick="openModal()">
  Compare <span id="compareCount">0</span> Cards &rarr;
</button>

<!-- COMPARISON MODAL -->
<div class="modal-overlay" id="compModal">
  <div class="modal">
    <div class="modal-header">
      <span class="modal-title">Card Comparison</span>
      <button class="modal-close" onclick="closeModal()">&#x2715;</button>
    </div>
    <div class="modal-body">
      <div id="modalTableWrap"></div>
    </div>
    <div class="modal-footer">
      <button class="btn-close-modal" onclick="clearAndClose()">Clear &amp; Close</button>
    </div>
  </div>
</div>

<script>
var comparisonData = {{ comparison_json | safe }};
var selectedCards = [];
var spendingData = {
  dining: {{ spending.dining }},
  grocery: {{ spending.grocery }},
  gas: {{ spending.gas }},
  travel: {{ spending.travel }},
  streaming: {{ spending.streaming }},
  shopping: {{ spending.shopping }},
  other: {{ spending.other }}
};

// ---- SORT & FILTER ----
function applyFilters() {
  var sortKey = document.getElementById('sortSelect').value;
  var noFeeOnly = document.getElementById('noFeeFilter').checked;
  var grid = document.getElementById('cardsGrid');
  var cards = Array.from(grid.querySelectorAll('.card-item'));

  var visible = cards.filter(function(c) {
    if (noFeeOnly && c.dataset.noFee !== 'true') { c.style.display = 'none'; return false; }
    c.style.display = '';
    return true;
  });

  visible.sort(function(a, b) {
    if (sortKey === 'first_year') return parseFloat(b.dataset.firstYear) - parseFloat(a.dataset.firstYear);
    if (sortKey === 'ongoing')    return parseFloat(b.dataset.ongoing) - parseFloat(a.dataset.ongoing);
    if (sortKey === 'fee')        return parseFloat(a.dataset.annualFee) - parseFloat(b.dataset.annualFee);
    if (sortKey === 'bonus')      return parseFloat(b.dataset.bonus) - parseFloat(a.dataset.bonus);
    return 0;
  });

  visible.forEach(function(c) { grid.appendChild(c); });

  document.getElementById('cardCount').textContent =
    'Showing ' + visible.length + ' of {{ total_qualifying }} qualifying cards';
}

// ---- WHY THIS CARD ----
function toggleWhy(btn) {
  var cardItem = btn.closest('.card-item');
  var idx = cardItem.dataset.index;
  var sec = document.getElementById('why-' + idx);
  var isOpen = sec.classList.contains('open');

  if (!isOpen) {
    generateWhyText(idx);
    sec.classList.add('open');
    btn.textContent = '\u25B2 Hide Explanation';
  } else {
    sec.classList.remove('open');
    btn.textContent = '\u25BC Why This Card?';
  }
}

function generateWhyText(idx) {
  var card = comparisonData[parseInt(idx)];
  if (!card) return;
  var el = document.getElementById('why-text-' + idx);
  if (!el) return;

  var parts = [];
  var totalSpend = 0;
  var cats = ['dining','grocery','gas','travel','streaming','shopping','other'];
  cats.forEach(function(c) { totalSpend += (spendingData[c] || 0); });

  if (totalSpend > 0) {
    var rewardBreakdown = [];
    cats.forEach(function(c) {
      var amt = spendingData[c] || 0;
      if (amt > 0) {
        var rate = card[c + '_rate'] || 1;
        var earned = amt * 12 * (rate / 100);
        if (earned > 0) rewardBreakdown.push({ cat: c, earned: earned, rate: rate });
      }
    });
    rewardBreakdown.sort(function(a,b) { return b.earned - a.earned; });

    if (rewardBreakdown.length > 0) {
      var topCats = rewardBreakdown.slice(0, 3);
      var earnedStr = topCats.map(function(r) {
        return '$' + Math.round(r.earned).toLocaleString() + ' in ' + r.cat + ' rewards (' + r.rate + '%)';
      }).join(', ');
      parts.push('Based on your spending, you\u2019d earn approximately ' + earnedStr + ' annually.');
    }
  }

  var totalRewards = parseFloat(card.first_year_value) - parseFloat(card.signup_bonus) + parseFloat(card.annual_fee);
  if (card.signup_bonus > 0) {
    parts.push('Combined with the $' + card.signup_bonus.toLocaleString() + ' welcome bonus, this card delivers $' + Math.round(card.first_year_value).toLocaleString() + ' in first-year value.');
  } else if (card.signup_bonus === 0 && card.annual_fee === 0) {
    parts.push('With no annual fee and no signup bonus, the ongoing rewards of $' + Math.round(totalRewards).toLocaleString() + '/year speak for themselves.');
  }

  if (card.annual_fee === 0) {
    parts.push('There\u2019s no annual fee, so every dollar of rewards goes straight to you.');
  } else {
    parts.push('The $' + card.annual_fee + ' annual fee is offset by strong rewards and valuable perks.');
  }

  if (card.no_foreign_fee) {
    parts.push('No foreign transaction fees make this card ideal for international travel.');
  }

  el.textContent = parts.join(' ');
}

// ---- COMPARISON ----
function handleCompare(cb) {
  var idx = parseInt(cb.dataset.idx);
  if (cb.checked) {
    if (selectedCards.length >= 3) { cb.checked = false; alert('You can compare up to 3 cards at a time.'); return; }
    if (selectedCards.indexOf(idx) === -1) selectedCards.push(idx);
  } else {
    selectedCards = selectedCards.filter(function(i) { return i !== idx; });
  }
  updateFloatBtn();
}

function updateFloatBtn() {
  var btn = document.getElementById('floatCompareBtn');
  document.getElementById('compareCount').textContent = selectedCards.length;
  if (selectedCards.length >= 2) {
    btn.classList.add('visible');
  } else {
    btn.classList.remove('visible');
  }
}

function openModal() {
  if (selectedCards.length < 2) return;
  buildTable();
  document.getElementById('compModal').classList.add('open');
}

function closeModal() {
  document.getElementById('compModal').classList.remove('open');
}

function clearAndClose() {
  selectedCards = [];
  document.querySelectorAll('.compare-cb').forEach(function(cb) { cb.checked = false; });
  updateFloatBtn();
  closeModal();
}

function buildTable() {
  var cards = selectedCards.map(function(i) { return comparisonData[i]; }).filter(Boolean);
  if (cards.length === 0) return;

  var rows = [
    { label: 'Annual Fee', key: 'annual_fee', fmt: function(v) { return v === 0 ? '$0 (Free)' : '$' + v; }, lower: true },
    { label: 'Signup Bonus', key: 'signup_bonus', fmt: function(v) { return v > 0 ? '$' + v.toLocaleString() : '\u2014'; }, lower: false },
    { label: 'Dining Rate', key: 'dining_rate', fmt: function(v) { return v + '%'; }, lower: false },
    { label: 'Grocery Rate', key: 'grocery_rate', fmt: function(v) { return v + '%'; }, lower: false },
    { label: 'Gas Rate', key: 'gas_rate', fmt: function(v) { return v + '%'; }, lower: false },
    { label: 'Travel Rate', key: 'travel_rate', fmt: function(v) { return v + '%'; }, lower: false },
    { label: 'Streaming Rate', key: 'streaming_rate', fmt: function(v) { return v + '%'; }, lower: false },
    { label: 'Shopping Rate', key: 'shopping_rate', fmt: function(v) { return v + '%'; }, lower: false },
    { label: 'Base/Other Rate', key: 'other_rate', fmt: function(v) { return v + '%'; }, lower: false },
    { label: 'No Foreign Fee', key: 'no_foreign_fee', fmt: function(v) { return v ? '\u2713 Yes' : '\u2715 No'; }, lower: false },
    { label: 'First-Year Value', key: 'first_year_value', fmt: function(v) { return '$' + Math.round(v).toLocaleString(); }, lower: false },
    { label: 'Ongoing Value', key: 'ongoing_value', fmt: function(v) { return '$' + Math.round(v).toLocaleString() + '/yr'; }, lower: false },
  ];

  var html = '<table class="compare-table"><thead><tr><th style="width:140px">Feature</th>';
  cards.forEach(function(c) {
    html += '<th>' + c.name + '<br><span style="font-weight:400;color:var(--gray-600)">' + c.issuer + '</span></th>';
  });
  html += '</tr></thead><tbody>';

  rows.forEach(function(row) {
    html += '<tr><td class="row-label">' + row.label + '</td>';
    var values = cards.map(function(c) { return c[row.key]; });
    var best = row.lower
      ? Math.min.apply(null, values.map(function(v) { return typeof v === 'boolean' ? (v ? 0 : 1) : v; }))
      : Math.max.apply(null, values.map(function(v) { return typeof v === 'boolean' ? (v ? 1 : 0) : v; }));

    cards.forEach(function(c) {
      var val = c[row.key];
      var numVal = typeof val === 'boolean' ? (val ? (row.lower ? 0 : 1) : (row.lower ? 1 : 0)) : val;
      var isWinner = numVal === best;
      var cellClass = isWinner ? 'cell-winner' : '';
      html += '<td class="' + cellClass + '">' + row.fmt(val) + '</td>';
    });
    html += '</tr>';
  });

  html += '</tbody></table>';
  document.getElementById('modalTableWrap').innerHTML = html;
}

// Close modal on overlay click
document.getElementById('compModal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});
</script>

</body>
</html>
'''
