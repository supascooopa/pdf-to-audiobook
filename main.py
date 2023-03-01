from flask import Flask, render_template, request, Response
from io import BytesIO
from pdf_extractor import read_pdf
from aws_polly import calling_polly


app = Flask("__app__")


@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        # requesting file
        pdf_file = request.files
        # streaming the file and reading it as bytes
        pdf_byte = pdf_file.get("file").stream.read()
        # changing the bytes into BytesIO to be able to feed it into read_pdf function
        io = BytesIO(pdf_byte)
        # extracting text from PDF
        pdf_text = read_pdf(io)
        # feeds the string extracted from PDF, to AWS polly and returns bytes representation of response data
        audiobook_bytes = calling_polly(pdf_text)
        return Response(audiobook_bytes,
                        mimetype="audio/mpeg",
                        headers={"Content-Disposition": "attachment;filename=your_audiobook.mp3"})
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

