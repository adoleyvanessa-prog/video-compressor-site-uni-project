import os
import time
import subprocess
import argparse

def compress_video(input_path, codec, crf, preset):
    input_name = os.path.basename(input_path)
    name, ext = os.path.splitext(input_name)
    output_folder = "compressed"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{name}_{codec}.mp4")

    print(f"Compressing {input_name} with {codec.upper()} (CRF {crf}, preset: {preset})...")

    # Prepare FFmpeg command
    command = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", codec,
        "-crf", str(crf),
        "-preset", preset,
        "-c:a", "aac", "-b:a", "128k",
        output_path
    ]

    start_time = time.time()
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time.time()

    time_taken = end_time - start_time

    # Estimate energy using 15W TDP (from Intel U-series spec)
    average_power_watts = 15
    energy_used = time_taken * average_power_watts

    # Get file sizes in MB
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)

    # Output results
    print(f"RESULT_ORIGINAL_SIZE={original_size:.2f}")
    print(f"RESULT_COMPRESSED_SIZE={compressed_size:.2f}")
    print(f"RESULT_TIME={time_taken:.2f}")
    print(f"RESULT_ENERGY={energy_used:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress a video and estimate energy.")
    parser.add_argument("--input", required=True, help="Path to input video")
    parser.add_argument("--codec", required=True, choices=["h264", "h265"], help="Codec to use")
    parser.add_argument("--crf", type=int, default=28, help="CRF value")
    parser.add_argument("--preset", default="slow", help="FFmpeg preset")

    args = parser.parse_args()

    codec_map = {
        "h264": "libx264",
        "h265": "libx265"
    }

    codec_lib = codec_map[args.codec]

    if not os.path.exists(args.input):
        print(f"[ERROR] Input file {args.input} not found!")
    else:
        compress_video(args.input, codec_lib, args.crf, args.preset)














