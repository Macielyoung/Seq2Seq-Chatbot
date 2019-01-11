from django.shortcuts import render
from django.http import HttpResponse
from infer import SeqModel
import json

seq2seq = SeqModel()
metadata = seq2seq.load_data()
seq2seq.load_model(metadata)

# Create your views here.
def index(request):
	query = request.GET.get('query', '')
	qa_pair = {}
	qa_pair['query'] = query
	answer = seq2seq.infer(query)
	qa_pair['answer'] = answer
	qa_json = json.dumps(qa_pair)
	response = HttpResponse(qa_json)
	response.__setitem__("Access-Control-Allow-Origin", "*")
	return response