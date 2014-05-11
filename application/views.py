"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, send_file
from werkzeug.utils import secure_filename

from application import app
from pyPdf import PdfFileWriter, PdfFileReader
import StringIO

ALLOWED_EXTENSIONS = set(['pdf'])
	
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			stream = StringIO.StringIO()
			
			filename = secure_filename(file.filename)
			input_pdf = PdfFileReader(file)
			output_pdf = PdfFileWriter()
			
			total_pages = input_pdf.getNumPages()
			for page in xrange(total_pages - 1, -1, -1):
				output_pdf.addPage(input_pdf.getPage(page))
		
			output_pdf.write(stream)
			stream.seek(0)
			
			return send_file(stream, attachment_filename=filename, as_attachment=True)
	return render_template('homepage.html')

def warmup():
	"""App Engine warmup handler
	See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

	"""
	return ''

