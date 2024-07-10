import subprocess


command = "conda run -n carnumber_paddleocr paddleocr --image_dir temp.jpg --lang korean | grep -A 1 'ppocr INFO'"
result = subprocess.run(
    # ['conda', 'run', '-n', 'carnumber_paddleocr', 'paddleocr', '--image_dir', 'temp.jpg', '--lang', 'korean', '|', 'grep', '-A', '1', 'ppocr INFO'],
    command,
    capture_output=True, text=True, shell=True
)
# os.remove("temp.jpg")  # Remove the temporary file after processing
print(result.stdout)