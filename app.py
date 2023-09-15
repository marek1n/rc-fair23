from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS

from pathlib import Path
import src.functions as fn
import threading


app = Flask(__name__)
CORS(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    global SUBJECT_ID
    SUBJECT_ID = fn.increment_subject_id()

    return render_template('index.html')


@app.route('/rc', methods=['GET', 'POST'])
def experiment_start():
   return render_template('experiment.html')


@app.route('/results', methods=['POST'])
def submit_results():
    data = request.get_json()
    condition = int(data['final']) # coerces 0 or 1
    # save data
    fn.save_results(data, condition, subject_id=SUBJECT_ID)
    # run rcicr in separate thread
    t = threading.Thread(target=fn.run_rcicr, args=(condition, SUBJECT_ID), daemon=True)
    t.start()

    return jsonify(success=True)


@app.route('/results', methods=['GET'])
def display_results():
    ci_paths = [f"cis/ci_sub-{SUBJECT_ID}_{i}.png" for i in range(2)]
    return render_template('results_page.html', 
                           subjectCI_0=ci_paths[0],
                           subjectCI_1=ci_paths[1]
                           )

@app.route('/explainer', methods=['GET'])
def explainer():
    return render_template('explainer.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)

