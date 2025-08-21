from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.conf.urls.static import static
from django.conf import settings
from PIL import Image
import os

#os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
#tf.disable_v2_behavior()

static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static',)
##############################################################################################################
# just a function for files uploading
def handle_uploaded_file(path, f):
	with open(path, 'wb') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
# Create your views here.
##############################################################################################################
def about(request):

	scripting = [
		#{"name" : "", "version" : "", "url" : r""},
		{"name" : "Python", "version" : "3.5.2", "url" : r'https://www.python.org/'},
		{"name" : "Django", "version" : "1.10.3", "url" : r"https://www.djangoproject.com/"},
		{"name" : "Javascript", "version" : None, "url" : r"https://www.javascript.com/"},
	]

	databases = [
		{"name" : "SQLite", "version" : "3", "url" : r"https://sqlite.org/"},
		]

	parergon = [
		{"name" : "Bootsrtap", "version" : "3.3.7", "url" : r"http://getbootstrap.com/"},
		{"name" : "jQuery", "version" : "3.1.1", "url" : r"https://jquery.com/"},
		{"name" : "Cropper", "version" : "2.3.4", "url" : r"https://fengyuanchen.github.io/cropper/"},
	]

	recognition =  [
		{"name" : "TensorFlow", "version" : "r0.12.0 rc0", "url" : r"https://www.tensorflow.org"},
		]

	context = {
		'scripting' : scripting,
		'databases' : databases,
		'parergon' : parergon,
		'recognition' : recognition,
		}

	return render (request, 'core/about.html', context)

##############################################################################################################

def contribute(request):
	if request.method == 'GET':
		# if user is just redirected to this page
		form = UploadFileForm()
	elif request.method == 'POST':
		# if user is submitting mage
		form = UploadFileForm(request.POST, request.FILES)
		print ('post content')
		for i in request.POST:
			print (i, request.POST[i])
		print ('End of POST content')

		if form.is_valid():
			print ('Valid form')
			# if form is filed - substitute currently viewed image
			image_src = os.path.join('core','images', 'library_uploads', str(request.FILES['file']))			
			path = os.path.join(static_folder, image_src)
			print (path)
			handle_uploaded_file(path, request.FILES['file'])
			with open (os.path.join(static_folder, 'core','images', 'library_uploads', 'uploads_list.txt'), 'a') as out_file:
				line = str(request.FILES['file']) + '  ---  ' + request.POST['specie']
				out_file.write(line)
				out_file.write(os.linesep)
		else:
			print ('Invalid form')
			for i in form.errors:
				print (i)
				print (form[i])
			#print (str(request.FILES['file']))

	return render (request, 'core/contribute.html', {'form': form})

##############################################################################################################

def recognize(request):
	if request.method == 'GET':
		# if user is just redirected to this page
		form = UploadFileForm()
		form_reply = ["Run identification to get results or replace the picture"]
		# just picture as example
		image_src = os.path.join('core','images', 'IMG_3286.JPG')

	elif request.method == 'POST':
		# if user replaced the image or started identification
		form = UploadFileForm(request.POST, request.FILES)
		form_reply = []

		if form.is_valid():
			# if form is filed - substitute currently viewed image
			image_src = os.path.join('core','images', 'uploads', str(request.FILES['file']))
			
			path = os.path.join(static_folder, image_src)
			handle_uploaded_file(path, request.FILES['file'])
			form_reply += ['Run the recognition to see the result']
		else:
			# basic static folder for this application
			folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static',)
			# if user initiated recognition
			image_src = request.POST['file_name']
			recognition_mode = request.POST['optionsRadios']
			# defining, what exactly to recognize
			if recognition_mode=="whole":
				pass
			else:
				# responce is 4 floats, separatd with commas
				# but system thinks it is string
				params = [int(float(item)) for item in str(request.POST['selected_info']).split(',')]
				x0 = params[0]	# Left
				y0 = params[1]	# Top
				x1 = x0 + params[2]	# Right
				y2 = y0 + params[3]	# Bottom			
				
				img = Image.open(os.path.join(folder, image_src))
				# Cropping image according to selected region
				img2 = img.crop ((x0, y0, x1, y2))
				img2_src = os.path.join('core','images', 'crops', os.path.basename(str(request.POST['file_name'])))
				# save image on server
				img2.save (os.path.join (static_folder, img2_src))
				image_src = img2_src				

			for i in identify (os.path.join (static_folder, image_src)):
				form_reply += [i]

	return render (request, 'core/recognize.html', { 'image_src' : image_src,'form' : form,'form_reply' : form_reply} )

##############################################################################################################

def identify (image_path):
	# template for output
	output = []
	# project_base_dir
	tf_folder = os.path.join(os.path.dirname(os.path.dirname(settings.BASE_DIR)), 'tf')
	graph_file = os.path.join (tf_folder, 'graph.pb')
	label_file = os.path.join (tf_folder, 'labels.txt')
	image_file = image_path
	# read the content of file
	image_data = tf.io.gfile.GFile (image_file, 'rb').read()
	# read labels
	label_lines = [line.rstrip() for line in tf.io.gfile.GFile(label_file)]
	# load analysis graph
	with tf.io.gfile.GFile(graph_file, 'rb') as f:
		graph_def = tf.compat.v1.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

	with tf.compat.v1.Session() as sess:
		softmax_tensor = sess.graph.get_tensor_by_name ('final_result:0')

		predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0' : image_data})

		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
		line = 'Probabilities, that sample belongs to certain genera:'
		output +=[line, ' ']
		for node_id in top_k[:5]:
			line = str(label_lines[node_id]).title() + ' ' + str(round(100.0*predictions[0][node_id], 3)) + '%'
			output +=[line]
	return output