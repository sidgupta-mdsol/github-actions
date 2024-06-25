import pdfkit
import requests
import os
import json

# Global Variables
project_name = os.environ["MEDISTRANO_PROJECT_NAME"]
stage_name = os.environ["MEDISTRANO_STAGE_NAME"]
MEDISTRANO_TOKEN = os.environ["MEDISTRANO_TOKEN"]
EKS_SWITCH = os.environ["EKS_SWITCH"]
TRIGGER_USER = os.environ["Actor"]

ICON_MDSOL = "/home/runner/work/github-actions/github-actions/icon-mdsol2.png"
ICON_SUCCESS = "/home/runner/work/github-actions/github-actions/icon-success.png"
HTML_FILE = f"{project_name}-{stage_name}-IR.html"
IR_PDF = f'{project_name}-{stage_name}-IR.pdf'

# Function to get deployment data
def get_deployment_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error making API call: {e}")
        exit()

# Function to write HTML content
def write_html_content(file_name, content):
    with open(file_name, 'w') as html_file:
        html_file.write(content)

# Function to convert HTML to PDF
def html_pdf_convertor(input_file, output_file):
    options = {
        'margin-top': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'margin-right': '10mm',
        'enable-local-file-access': None
    }
    try:
        pdfkit.from_file(input_file, output_file, options=options)
        print("\n\n")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to generate HTML report content
def generate_html_report(doc_json, trigger_user):
    summary = doc_json["summary"]
    tasks = doc_json.get('tasks', [])

    # Determine if the product version needs to be replaced by git_ref
    product_version = summary["product_version"]
    if product_version in [None, "None"]:
        product_version = summary["git_ref"]

    # Prepare the deployed by field
    deployed_by = summary['deployed_by']
    if "machine-user" in deployed_by:
        deployed_by = f"{trigger_user} (deployed as {deployed_by})"

    # Generate HTML content
    html_content = f"""
    <html>
    <head><title>{summary['project']} Installation Report</title></head>
    <body style='font-family:sans-serif;'>
    <img width=240 height=36 align='right' src='{ICON_MDSOL}'><br><br>
    <p style='text-align:center'><font size='5'><b>Installation Report</b></font></p>
    <p style='text-align:center'><font size='4'><b>Summary</b></font></p>
    <table border=1 style='font-size:13px;word-wrap:break-word;width:100%;table-layout:fixed;' bordercolor='#6a737c' cellspacing=0 cellpadding=5>
    <col width='20%'><col width='80%'>
    <tr bgcolor='#E5E7E9'><td><b>Name</b></td><td><b>Value</b></td></tr>
    <tr><td>Status</td><td>{summary['status']} <img width=36 height=36 align='middle' src='{ICON_SUCCESS}'></td></tr>
    <tr><td>Project</td><td>{summary['project']}</td></tr>
    <tr><td>Stage</td><td>{summary['stage']}</td></tr>
    <tr><td>Environment</td><td>{summary['environment']}</td></tr>
    <tr><td>Region</td><td>{summary['region']}</td></tr>
    <tr><td>Deployment Release</td><td>{summary['deployment_release']}</td></tr>
    <tr><td>Git Ref</td><td>{summary['git_ref']}</td></tr>
    <tr><td>Git SHA</td><td>{summary['git_sha']}</td></tr>
    <tr><td>Message</td><td>{summary['message']}</td></tr>
    <tr><td>Created</td><td>{summary['created_at']}</td></tr>
    <tr><td>Updated At</td><td>{summary['updated_at']}</td></tr>
    <tr><td>Cluster Name</td><td>{summary['cluster_name']}</td></tr>
    <tr><td>Deployed By</td><td>{deployed_by}</td></tr>
    <tr><td>Product Name</td><td>{summary['product_name']}</td></tr>
    <tr><td>Product Version</td><td>{product_version}</td></tr>
    </table>&nbsp;
    <p style='text-align:center'><font size='4'><b>Tasks</b></font></p>
    """

    # Process each task
    for task in tasks:
        task_name = task['display_action']
        task_status = task['status']
        html_content += f"""
        <table border=1 style='font-size:13px;word-wrap:break-word;width:100%;table-layout:fixed;' bordercolor='#6a737c' cellspacing=0 cellpadding=5>
        <col width='100%'><tr><td>
        <p><font size='3'><b>{task_name}</b></font></p>
        <p><font size='2'><b>Status: {task_status}</b></font></p>
        """

        if "skipped by user" in task_status.lower():
            html_content += "</td></tr></table>&nbsp;<p />\n"
            continue

        html_content += """
        <table border=1 style='font-size:13px;word-wrap:break-word;width:100%;table-layout:fixed;' bordercolor='#6a737c' cellspacing=0 cellpadding=5>
        <col width='20%'><col width='8%'><col width='72%'>
        <tr bgcolor='#E5E7E9'><td><b>Operation Name</b></td><td><b>Status</b></td><td><b>Message</b></td></tr>
        """

        # Process each AWS operation
        for ops_task in task.get('aws_operations', []):
            ops_name = ops_task['operation_name']
            ops_status = ops_task['status']
            ops_message = ops_task['message']
            html_content += f"<tr style='vertical-align:top'><td>{ops_name}</td><td>{ops_status}</td><td>{ops_message}<br>\n"

            for data_type in ['request_data', 'response_data']:
                data_content = ops_task.get(data_type, "")

                if isinstance(data_content, dict):
                    data_content = json.dumps(data_content, indent=2)

                data_content = data_content.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                html_content += f"<br><b>{data_type.replace('_', ' ').title()}</b><br>\n"

                if data_content.strip() == "{}":
                    html_content += "{<br>}<br>\n"
                else:
                    for line in data_content.splitlines():
                        html_content += f"{line}<br>\n"

            html_content += "</td></tr>\n"

        html_content += "</table>&nbsp;\n"

        # Process logs
        logs = task.get('logs', [])
        if logs:
            html_content += "<p><font size='3'><b>Log</b></font></p>\n"
            MAX_MSG_NR = 500
            msg_count = 0

            for log in logs:
                log_stream = log.get('log_stream')
                if log_stream:
                    html_content += f"<p><font size='3'><b>{log_stream}</b></font></p>\n"

                for event in log.get('events', []):
                    timestamp = event['timestamp'].replace('T', ' ').replace('Z', ' UTC')
                    message = event['message']
                    html_content += f"{timestamp} - {message}<br><br>\n"
                    msg_count += 1

                    if msg_count >= MAX_MSG_NR:
                        html_content += f"<br>Large logs were truncated - showing the last {MAX_MSG_NR} lines of output<br><br>\n"
                        break

                if msg_count >= MAX_MSG_NR:
                    break

        html_content += "</td></tr></table>&nbsp;<p />\n"

    html_content += "</body></html>\n"
    return html_content


## Main script execution ##
engine = "k8s" if EKS_SWITCH == "ON" else "ecs"
url = f"https://medistrano.imedidata.net/api/v0/projects/{project_name}/stages/{stage_name}/{engine}/deployments/"
headers = {'Authorization': f'Bearer {MEDISTRANO_TOKEN}'}

deployment_data = get_deployment_data(url, headers)
deployment = deployment_data['deployments'][0]
deploy_id = deployment['id']
deployment_status = deployment['status']

if deployment_status == "success":
    IR_URL = f"https://medistrano.imedidata.net/api/v0/projects/{project_name}/stages/{stage_name}/{engine}/deployments/{deploy_id}/installation_report"
    doc_json = get_deployment_data(IR_URL, headers)
    html_content = generate_html_report(doc_json, TRIGGER_USER)
    write_html_content(HTML_FILE, html_content)
    print(f"Generating installation report {IR_PDF}...")
    html_pdf_convertor(HTML_FILE, IR_PDF)
    print(f"Installation report {IR_PDF} generated successfully")
else:
    print(f"Deployment status is '{deployment_status}', no installation report generated.")
