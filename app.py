from flask import Flask, jsonify, render_template
from audio import Input

app = Flask(__name__)

# Create an instance of the Input class
input_handler = Input()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Get frequency, note, and octave
    frequency, note, octave = input_handler.get_musical_values()
    return jsonify({
        'frequency': frequency,
        'note': note,
        'octave': octave
    })

if __name__ == "__main__":
    app.run(debug=True)
