from flask import Flask , jsonify, request
import dspandaswork as dpd
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome"

@app.route("/api/employees")
def employees_status():
    status =dpd.employee_status()
    return jsonify(status)

@app.route("/api/FT")
def emp_FT():
    response = dpd.fulltime()
    return jsonify(response)

@app.route("/api/status")
def emp_status():
    status = request.args.get("user_status")
    response = dpd.emp_by_status(status) #Alternate approach use if else, just to make user input simple
    return jsonify(response)

@app.route("/api/timeoff")
def emp_timeoff():
    res = dpd.timeoff()
    return jsonify(res)

app.run(debug=True)


# response.json() — converts text to dictionary
# pd.DataFrame() — converts dictionary to DataFrame
# .to_dict() — converts DataFrame to dictionary
# jsonify() — converts dictionary to JSON