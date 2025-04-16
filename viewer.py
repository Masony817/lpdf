from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route("/")
def index():
    # a simple html page to view the lpdf
    
    return """
    <html>
    <head>
        <title>LPDF Viewer</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.js" integrity="sha512-VzYHEjQVpgu4ZP+EkBnM9cHLUyfU8xtnLGU8dBG2z7Dv45BoO31c+G5CGb/0+Q/g6P+P2LqK/fX2/1a1bM+7UQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    </head>
    <body>
        <h1>LPDF Viewer</h1>
        <embed id="pdf-embed" src="/lpdf" type="application/pdf" width="100%" height="800px" />

        <script>
            // Connect to the Socket.IO server running on the incrementer app
            console.log('Attempting to connect to WebSocket at http://localhost:5001');
            const socket = io('http://localhost:5001');

            socket.on('connect', () => {
                console.log('[Viewer WS] Connected successfully!');
            });

            // Listen for the 'pdf_updated' event
            socket.on('pdf_updated', () => {
                console.log('[Viewer WS] Received pdf_updated event.');
                const embedElement = document.getElementById('pdf-embed');
                const newSrc = '/lpdf?t=' + new Date().getTime();
                console.log('[Viewer WS] Updating embed src to:', newSrc);
                // Append timestamp to force reload and avoid cache
                embedElement.src = newSrc;
                // Try forcing a reload on the embed element directly (might work in some browsers)
                // embedElement.contentDocument.location.reload(true);
            });

            socket.on('disconnect', () => {
                console.log('[Viewer WS] Disconnected from WebSocket server');
            });

            socket.on('connect_error', (err) => {
              console.error('[Viewer WS] Connection error:', err);
            });
        </script>
    </body>
    </html>
    """

@app.route("/lpdf")
def serve_lpdf():
    filename = "demo.lpdf"
    print(f'[Viewer] Request received for /lpdf. Checking for file: {filename}') # Log request
    if os.path.exists(filename):
        print(f'[Viewer] File {filename} found. Serving...') # Log file found
        return send_file(
            filename,
            mimetype="application/pdf",
            as_attachment=False,
            download_name="demo.pdf"
        )
    else:
        return "LPDF file not found", 404

if __name__ == "__main__":
    app.run(port=5000)