from flask import Flask, render_template, request, redirect, url_for, jsonify
import uuid
import os

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/submit', methods=['POST'])
def submit():
    tosca_file = request.files.get('tosca_file')
    provider = request.form.get('provider')

    run_id = str(uuid.uuid4())[:8]

    os.makedirs('uploads', exist_ok=True)
    file_path = os.path.join('uploads', f'{run_id}_{tosca_file.filename}')
    tosca_file.save(file_path)

    return redirect(url_for('processing', run_id=run_id))

@app.route('/processing/<run_id>')
def processing(run_id):
    return render_template('processing.html', run_id=run_id, provider="AWS")

@app.route('/run_pipeline/<run_id>')
def run_pipeline(run_id):
   
    mock_result = {
        "success": True,
        "stages": [
            {"name": "Stage 1: TOSCA Parser", "status": "passed", "message": "Blueprint validated"},
            {"name": "Stage 2: AI Mapping", "status": "passed", "message": "Mapped to AWS services"},
            {"name": "Stage 3: IaC Generation", "status": "passed", "message": "Terraform files generated"},
            {"name": "Stage 4: Deployment", "status": "passed", "message": "Resources deployed"},
            {"name": "Stage 5: Consistency Check", "status": "passed", "message": "All resources verified"}
        ]
    }
    return jsonify(mock_result)

@app.route('/results/<run_id>')
def results(run_id):
   
    mock_data = {
        "success": True,
        "mapping_table": [
            {
                "node_id": "web_server",
                "terraform_resource": "aws_instance",
                "provider_service": "Amazon EC2",
                "reasoning": "2 CPU 4GB RAM maps to t3.small on AWS"
            }
        ],
        "stages": [
            {"name": "Stage 1: TOSCA Parser", "status": "passed", "message": "Blueprint validated"},
            {"name": "Stage 2: AI Mapping", "status": "passed", "message": "Mapped to AWS services"},
            {"name": "Stage 3: IaC Generation", "status": "passed", "message": "Terraform files generated"},
            {"name": "Stage 4: Deployment", "status": "passed", "message": "Resources deployed"},
            {"name": "Stage 5: Consistency Check", "status": "passed", "message": "All resources verified"}
        ],
        "consistency_report": {
            "drift_detected": False,
            "checks": [
                {"node_id": "web_server", "status": "passed", "message": "EC2 instance verified via CloudWatch"}
            ]
        }
    }
    return render_template('results.html', run_id=run_id, **mock_data)

if __name__ == '__main__':
    app.run(debug=True)