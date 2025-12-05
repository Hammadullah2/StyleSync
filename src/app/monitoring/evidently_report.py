from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from evidently.pipeline.column_mapping import ColumnMapping
import pandas as pd
import os

import http.server
import socketserver
import webbrowser

PORT = 7000
os.makedirs("reports", exist_ok=True)
report_path = "reports/evidently_report.html"


def serve(port: int = 7000):
    print(f"Starting Evidently server on http://127.0.0.1:{port} ...")

    os.makedirs("reports", exist_ok=True)

    # Minimal dummy dataset
    data = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5],
            "feature2": [5, 4, 3, 2, 1],
            "target": [0, 1, 0, 1, 0],
            "prediction": [0, 1, 0, 0, 1],
        }
    )

    column_mapping = ColumnMapping(target="target", prediction="prediction")

    report = Report(metrics=[DataDriftPreset(), ClassificationPreset()])
    report.run(reference_data=data, current_data=data, column_mapping=column_mapping)
    report.save_html("reports/evidently_report.html")

    print("Report saved at reports/evidently_report.html")
    os.chdir("reports")
    print(f"Serving report on http://127.0.0.1:{PORT}")
    webbrowser.open(f"http://127.0.0.1:{PORT}/evidently_report.html")
    socketserver.TCPServer(
        ("", PORT), http.server.SimpleHTTPRequestHandler
    ).serve_forever()


if __name__ == "__main__":
    serve()
