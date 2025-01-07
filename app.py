from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# 仮のユーザーデータ（デモ用）
users = {"test_user": "password123", "sample": "0000"}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password") 
        
        if not user_id or not password:
            return render_template("login.html", error="全ての項目を入力してください。")
        
        if user_id in users and users[user_id] == password:
            return redirect(url_for("checklist"))
        elif user_id not in users:
            return render_template("login.html", error="ユーザーが存在しません。新規登録してください。")
        else:
            return render_template("login.html", error="ユーザーIDまたはパスワードが間違っています。")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user_id = request.form.get("user_id")
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if not new_user_id or not new_password or not confirm_password:
            return render_template("register.html", error="全ての項目を入力してください。")
        
        if new_user_id in users:
            return render_template("register.html", error="このユーザーIDは既に登録されています。")
        
        if new_password != confirm_password:
            return render_template("register.html", error="パスワードが一致しません。")
        
        # 新しいユーザーを登録
        users[new_user_id] = new_password
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/checklist", methods=["GET", "POST"])
def checklist():
    if request.method == "POST":
        answers = request.form
        score = sum(int(answers[key]) for key in answers)
        result = "受診することをお勧めします。"if score >= 15 else \
                 "不安であれば受診してください。" if score >= 10 else \
                 "問題ない確率が高いです。"
        return render_template("result.html", result=result, probability=score * 4)
    return render_template("checklist.html")

if __name__ == "__main__":
    app.run(debug=True)