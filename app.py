from flask import Flask, render_template, request

app = Flask(__name__)

# ฟังก์ชันคำนวณคะแนนความเสี่ยง
def calculate_risk_score(age, gender, smoking, hypertension, waist_circumference, weight, height, exercise, family_history, blood_sugar, cholesterol, diet):
    score = 0

    # คำนวณคะแนนตามข้อมูลที่ส่งมา
    if int(age) > 50: score += 5
    if gender == "ชาย": score += 3
    if smoking == "True": score += 2
    if hypertension == "True": score += 3
    if int(waist_circumference) > 90: score += 4
    if int(blood_sugar) > 126: score += 4
    if int(cholesterol) > 240: score += 4
    if exercise == "True": score += 3
    if family_history == "True": score += 5
    if diet == "ไขมันสูง": score += 3

    return score

# ตีความคะแนน
def interpret_risk(score):
    if score < 5:
        return "<1%", "คุณมีความเสี่ยงต่ำมาก ควรรักษาสุขภาพต่อไป"
    elif score < 10:
        return "2%", "คุณมีความเสี่ยงปานกลาง ควรปรึกษาแพทย์"
    else:
        return "5%", "คุณมีความเสี่ยงสูงมาก ควรพบแพทย์ทันที"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # รับข้อมูลจากฟอร์ม
    data = request.form
    score = calculate_risk_score(
        age=data['age'],
        gender=data['gender'],
        smoking=data['smoking'],
        hypertension=data['hypertension'],
        waist_circumference=data['waist_circumference'],
        weight=data['weight'],
        height=data['height'],
        exercise=data['exercise'],
        family_history=data['family_history'],
        blood_sugar=data['blood_sugar'],
        cholesterol=data['cholesterol'],
        diet=data['diet']
    )
    risk, advice = interpret_risk(score)
    return render_template('index.html', risk=risk, advice=advice)

if __name__ == '__main__':
    app.run(debug=True)
