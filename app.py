from flask import Flask, jsonify, render_template, request
from audio import Input
from RecordAndMetronome import metronome, record_audio
import threading

app = Flask(__name__)

# Create an instance of the Input class
input_handler = Input()
stop_event = threading.Event()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Get frequency, note, next note, prior note, slider position, and octave
    frequency, note, next_note, prior_note, slider_position, octave = input_handler.get_musical_values()
    return jsonify({
        'frequency': frequency,
        'note': note,
        'next_note': next_note,
        'prior_note': prior_note,
        'slider_position': slider_position,
        'octave': octave
    })

@app.route('/metronome/start', methods=['POST'])
def start_metronome():
    bpm = request.json.get('bpm', 120)
    duration = request.json.get('duration', 60)
    threading.Thread(target=metronome, args=(bpm, duration, stop_event)).start()
    return jsonify({'status': 'Metronome started'})

@app.route('/metronome/stop', methods=['POST'])
def stop_metronome():
    stop_event.set()
    return jsonify({'status': 'Metronome stopped'})

@app.route('/record/start', methods=['POST'])
def start_recording():
    duration = request.json.get('duration', 10)
    output_file = request.json.get('output_file', 'output.wav')
    threading.Thread(target=record_audio, args=(duration, output_file, stop_event)).start()
    return jsonify({'status': 'Recording started'})

@app.route('/record/stop', methods=['POST'])
def stop_recording():
    stop_event.set()
    return jsonify({'status': 'Recording stopped'})

if __name__ == "__main__":
    app.run(debug=True)
