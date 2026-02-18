from flask import Flask, render_template, request
import grpc
import tempconv_pb2
import tempconv_pb2_grpc
import os

app = Flask(__name__)

# Backend address (can be overridden by env var for Cloud Run)
BACKEND_HOST = os.environ.get('BACKEND_HOST', 'localhost')
BACKEND_PORT = os.environ.get('BACKEND_PORT', '50051')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            temp_val = float(request.form['value'])
            conversion_type = request.form['type']
            
            # Connect to gRPC backend
            # Note: For Cloud Run, might need secure channel if using HTTPS, but usually internal traffic is insecure or uses specialized creds.
            # Localhost is insecure.
            target = f'{BACKEND_HOST}:{BACKEND_PORT}'
            print(f"Connecting to backend at {target}")
            
            with grpc.insecure_channel(target) as channel:
                stub = tempconv_pb2_grpc.TempConvServiceStub(channel)
                
                if conversion_type == 'c2f':
                    response = stub.CelsiusToFahrenheit(tempconv_pb2.TempRequest(value=temp_val))
                    result = f"{temp_val}°C = {response.value:.2f}°F"
                else:
                    response = stub.FahrenheitToCelsius(tempconv_pb2.TempRequest(value=temp_val))
                    result = f"{temp_val}°F = {response.value:.2f}°C"
        except Exception as e:
            result = f"Error: {e}"
                
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
