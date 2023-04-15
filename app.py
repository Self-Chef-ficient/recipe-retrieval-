from flask_cors import CORS
import time
import random
from flask import Flask, request, render_template,redirect,session
import os
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import numpy as np
from args import get_parser
import pickle
from model import get_model
from torchvision import transforms
from output import prepare_output
from PIL import Image
import sys
import json
from io import BytesIO

app = Flask(__name__)
app.secret_key=os.urandom(24)


@app.route('/getRecipe', methods=['GET', 'POST'])
def getRecipe():   
	data_dir = 'data'
	use_gpu = False
	device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
	map_loc = None if torch.cuda.is_available() and use_gpu else 'cpu' 
	ingrs_vocab = pickle.load(open(os.path.join(data_dir, 'ingr_vocab.pkl'), 'rb'))
	vocab = pickle.load(open(os.path.join(data_dir, 'instr_vocab.pkl'), 'rb'))

	ingr_vocab_size = len(ingrs_vocab)
	instrs_vocab_size = len(vocab)
	output_dim = instrs_vocab_size

	t = time.time()
	import sys; sys.argv=['']; del sys
	args = get_parser()
	args.maxseqlen = 15
	args.ingrs_only=False
	model = get_model(args, ingr_vocab_size, instrs_vocab_size)
	# Load the trained model parameters
	model_path = os.path.join(data_dir, 'modelbest.ckpt')
	model.load_state_dict(torch.load(model_path, map_location=map_loc))
	model.to(device)
	model.eval()
	model.ingrs_only = False
	model.recipe_only = False
	transf_list_batch = []
	transf_list_batch.append(transforms.ToTensor())
	transf_list_batch.append(transforms.Normalize((0.485, 0.456, 0.406), 
												(0.229, 0.224, 0.225)))
	to_input_transf = transforms.Compose(transf_list_batch)
	greedy = [True, False, False, False]
	beam = [-1, -1, -1, -1]
	temperature = 1.0
	numgens = len(greedy)
	image_folder = os.path.join(data_dir, 'demo_imgs')
	if request.method == 'GET':
		return render_template('rrt.html', value='hi')
		#return "Working hit the post method"
	if request.method == 'POST':
		print(request.files)
		if 'file' not in request.files:
			print('file not uploaded')
		else:
			file = request.files['file']
			image2 = file.read()
			image = Image.open(BytesIO(image2))
		transf_list = []
		transf_list.append(transforms.Resize(256))
		transf_list.append(transforms.CenterCrop(224))
		transform = transforms.Compose(transf_list)
		image_transf = transform(image)
		image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)
		num_valid = 1
		res = []
		for i in range(numgens):
			with torch.no_grad():
				outputs = model.sample(image_tensor, greedy=greedy[i], 
									temperature=temperature, beam=beam[i], true_ingrs=None)
				
			ingr_ids = outputs['ingr_ids'].cpu().numpy()
			recipe_ids = outputs['recipe_ids'].cpu().numpy()
				
			outs, valid = prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)
			
			if valid['is_valid']:
				ret_json = {}
				ret_json['Recipe'] = num_valid
				num_valid+=1
				ret_json['Title'] = outs['title']
				ret_json['Ingredients'] = ', '.join(outs['ingrs'])
				ret_json['Instructions'] ='-'.join(outs['recipe'])
				res.append(ret_json)

			else:
				pass
				print ("Not a valid recipe!")
				print ("Reason: ", valid['reason'])
		return json.dumps(res)
		
if __name__ == '__main__':
	app.run(debug=False)