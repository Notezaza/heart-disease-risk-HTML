from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# ฟังก์ชันคำนวณคะแนนความเสี่ยง
def calculate_risk_score(age, gender, smoking, hypertension, waist_circumference, weight, height, exercise, family_history, blood_sugar, cholesterol, diet):
    score = 0

    # อายุ
    if age < 35:
        score += -3
    elif 35 <= age <= 39:
        score += -2
    elif 40 <= age <= 44:
        score += 0
    elif 45 <= age <= 49:
        score += 2
    elif 50 <= age <= 54:
        score += 4
    elif 55 <= age <= 59:
        score += 6
    elif 60 <= age <= 64:
        score += 8
    elif 65 <= age <= 69:
        score += 10
    elif age >= 70:
        score += 12

    # เพศ
    if gender == "ชาย":
        score += 3

    # การสูบบุหรี่
    if smoking:
        score += 2

    # ความดันเลือดสูง
    if hypertension:
        score += 3

    # คอเลสเตอรอล
    if cholesterol > 240:
        score += 4
    elif cholesterol > 200:
        score += 2

    # น้ำตาลในเลือด
    if blood_sugar > 126:
        score += 4

    # รอบเอว
    if (gender == "ชาย" and waist_circumference >= 90) or (gender == "หญิง" and waist_circumference >= 80):
        score += 4

    # น้ำหนักและดัชนีมวลกาย (BMI)
    bmi = weight / (height / 100) ** 2
    if bmi < 18.5:
        score += 3
    elif bmi > 30:
        score += 4

    # กิจกรรมทางกาย
    if exercise == "ไม่ออกกำลังกาย":
        score += 3

    # ประวัติครอบครัว
    if family_history:
        score += 5

    # การบริโภคอาหาร
    if diet == "ทานอาหารที่มีไขมันสูง":
        score += 3
    elif diet == "ทานผักและผลไม้ไม่เพียงพอ":
        score += 2

    return score

# ฟังก์ชันตีความคะแนนความเสี่ยง
def interpret_risk(score):
    if score < 0:
        risk_percentage = "<1%"
        advice = "คุณมีความเสี่ยงต่ำมาก ควรรักษาพฤติกรรมสุขภาพที่ดีต่อไป"
    elif 1 <= score <= 5:
        risk_percentage = "1%"
        advice = "ความเสี่ยงอยู่ในระดับต่ำ ควรดูแลสุขภาพต่อไป"
    elif 6 <= score <= 8:
        risk_percentage = "2%"
        advice = "คุณมีความเสี่ยงปานกลาง ควรปรึกษาแพทย์เกี่ยวกับสุขภาพ"
    elif 9 <= score <= 11:
        risk_percentage = "4%"
        advice = "ความเสี่ยงค่อนข้างสูง ควรปรึกษาแพทย์และปรับพฤติกรรมสุขภาพ"
    elif 12 <= score <= 15:
        risk_percentage = "5-10%"
        advice = "ความเสี่ยงสูง ควรพบแพทย์เพื่อการวินิจฉัยและการรักษา"
    else:
        risk_percentage = ">12%"
        advice = "คุณมีความเสี่ยงสูงมาก ควรปรึกษาแพทย์ทันที"

    return risk_percentage, advice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate-risk', methods=['POST'])
def calculate_risk():
    try:
        data = request.json

        # ตรวจสอบว่าข้อมูลครบถ้วน
        required_fields = ['age', 'gender', 'smoking', 'hypertension', 'waist_circumference',
                           'weight', 'height', 'exercise', 'family_history', 'blood_sugar', 'cholesterol', 'diet']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # คำนวณคะแนนความเสี่ยง
        score = calculate_risk_score(
            data['age'], data['gender'], data['smoking'], data['hypertension'],
            data['waist_circumference'], data['weight'], data['height'],
            data['exercise'], data['family_history'], data['blood_sugar'], data['cholesterol'], data['diet']
        )
        risk_percentage, advice = interpret_risk(score)

        return jsonify({'risk_percentage': risk_percentage, 'advice': advice, 'score': score})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
