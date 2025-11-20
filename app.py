from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import subprocess
import uuid
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'avi', 'mov'}
MAX_DURATION = 180  # 3 minutes

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_video_duration(filepath):
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            filepath
        ], capture_output=True, text=True)

        duration_info = json.loads(result.stdout)
        return float(duration_info["format"]["duration"])
    except Exception as e:
        print(f"Error reading duration: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['video']
        codec = request.form.get('codec', 'h265')
        crf = request.form.get('crf', '30')
        preset = request.form.get('preset', 'medium')

        if file and allowed_file(file.filename):
            unique_name = f"{uuid.uuid4().hex}_{file.filename}"
            input_path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(input_path)

            duration = get_video_duration(input_path)
            if duration is None or duration > MAX_DURATION:
                os.remove(input_path)
                flash("❌ Video must be 3 minutes or less.")
                return redirect(url_for('upload'))

            try:
                proc = subprocess.run([
                    "python3", "compress_and_measure.py",
                    "--input", input_path,
                    "--codec", codec,
                    "--crf", crf,
                    "--preset", preset
                ], check=True, capture_output=True, text=True)

                output_lines = proc.stdout.splitlines()
                result = {}
                for line in output_lines:
                    if line.startswith("RESULT_"):
                        key, value = line.split("=")
                        result[key] = value

                codec_map = {
                "h264": "libx264",
                "h265": "libx265"
                                  }
                compressed_name = f"{os.path.splitext(unique_name)[0]}_{codec_map[codec]}.mp4"
                compressed_path = os.path.join(COMPRESSED_FOLDER, compressed_name)

                print("🔍 Checking for compressed file:", compressed_path)

                if not os.path.exists(compressed_path):
                    flash("❌ Compression finished, but file not found.")
                    return redirect(url_for('upload'))

                return render_template("upload.html", success=True,
                                       video=compressed_name,
                                       original_size=result.get("RESULT_ORIGINAL_SIZE"),
                                       compressed_size=result.get("RESULT_COMPRESSED_SIZE"),
                                       time_taken=result.get("RESULT_TIME"),
                                       energy=result.get("RESULT_ENERGY"))

            except subprocess.CalledProcessError as e:
                flash("❌ Compression failed.")
                print("Error:", e.stderr)
                return redirect(url_for('upload'))

        else:
            flash("❌ Invalid file type.")
            return redirect(url_for('upload'))

    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(COMPRESSED_FOLDER, filename)
    if not os.path.exists(file_path):
        flash("❌ Compressed file not found.")
        return redirect(url_for('upload'))
    return send_from_directory(COMPRESSED_FOLDER, filename, as_attachment=True)

@app.route('/cleanup', methods=['POST'])
def cleanup():
    for folder in ['uploads', 'compressed']:
        for f in os.listdir(folder):
            try:
                os.remove(os.path.join(folder, f))
            except Exception as e:
                print(f"Failed to delete {f}: {e}")
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)




