from flask import Flask, Response
import time
import random

app = Flask(__name__)

def event_stream():
    while True:
        # Generate some dummy metric data
        data = random.randint(1, 100)
        yield f"data: {data}\n\n"
        time.sleep(1)

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
      <body>
        <h1>Real-time Metrics</h1>
        <div id="data"></div>
        <script>
          var source = new EventSource("/stream");
          source.onmessage = function(event) {
            document.getElementById("data").innerHTML = "Metric: " + event.data;
          };
        </script>
      </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
