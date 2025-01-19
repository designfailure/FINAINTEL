from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import os
from typing import List, Dict

class DataHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            query_components = parse_qs(parsed_path.query)
            metric = query_components.get('metric', ['sentiment'])[0]
            
            data = self.get_data(metric)
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404)

    def get_data(self, metric: str) -> List[Dict]:
        # Load the most recent results file
        results_dir = 'data/processed'
        files = os.listdir(results_dir)
        if not files:
            return []
        
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(results_dir, f)))
        with open(os.path.join(results_dir, latest_file), 'r') as f:
            results = json.load(f)
        
        if metric == 'sentiment':
            return [
                {
                    'target': article['title'],
                    'datapoints': [
                        [article['sentiment']['scores']['positive'], article['sentiment']['scores']['neutral'], article['sentiment']['scores']['negative']]
                    ]
                }
                for article in results
            ]
        elif metric == 'evaluation':
            return [
                {
                    'target': 'ROUGE Scores',
                    'datapoints': [
                        [results[0]['evaluation']['rouge1_f1'], results[0]['evaluation']['rouge2_f1'], results[0]['evaluation']['rougeL_f1']]
                    ]
                }
            ]
        else:
            return []

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, DataHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

