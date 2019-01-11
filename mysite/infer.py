import time

import numpy as np
import tensorflow as tf
import tensorlayer as tl

from sklearn.utils import shuffle
from tensorlayer.layers import DenseLayer, EmbeddingInputlayer, Seq2Seq, retrieve_seq_length_op2

from data.twitter import data

sess_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)

# Seq2Seq Model
class SeqModel():
	sess = None
	net = None
	net_rnn = None
	src_vocab_size = 0
	word2idx = None
	idx2word = None
	unk_id = 0
	pad_id = 0
	start_id = 0
	end_id = 0
	y = None
	encode_seqs = None
	decode_seqs = None

	# load dataset
	def load_data(self):
		metadata, idx_q, idx_a = data.load_data(PATH='data/twitter/')
		return metadata

	"""
	Creates the LSTM Model
	"""
	def create_model(self, encode_seqs, decode_seqs, src_vocab_size, emb_dim, is_train=True, reuse=False):
		with tf.variable_scope("model", reuse=reuse):
	    	# for chatbot, you can use the same embedding layer,
	    	# for translation, you may want to use 2 seperated embedding layers
			with tf.variable_scope("embedding") as vs:
				net_encode = EmbeddingInputlayer(
					inputs = encode_seqs,
					vocabulary_size = src_vocab_size,
					embedding_size = emb_dim,
					name = 'seq_embedding')
				vs.reuse_variables()
				net_decode = EmbeddingInputlayer(
					inputs = decode_seqs,
					vocabulary_size = src_vocab_size,
					embedding_size = emb_dim,
					name = 'seq_embedding')

			net_rnn = Seq2Seq(net_encode, net_decode,
					cell_fn = tf.nn.rnn_cell.LSTMCell,
					n_hidden = emb_dim,
					initializer = tf.random_uniform_initializer(-0.1, 0.1),
					encode_sequence_length = retrieve_seq_length_op2(encode_seqs),
					decode_sequence_length = retrieve_seq_length_op2(decode_seqs),
					initial_state_encode = None,
					dropout = (0.5 if is_train else None),
					n_layer = 3,
					return_seq_2d = True,
					name = 'seq2seq')

			net_out = DenseLayer(net_rnn, n_units=src_vocab_size, act=tf.identity, name='output')
		return net_out, net_rnn

	def load_model(self, metadata):
		self.src_vocab_size = len(metadata['idx2w'])
		emb_dim = 1024

		self.word2idx = metadata['w2idx']
		self.idx2word = metadata['idx2w']

		self.unk_id = self.word2idx['unk']
		self.pad_id = self.word2idx['_']

		self.start_id = self.src_vocab_size
		self.end_id = self.src_vocab_size + 1

		self.word2idx.update({'start_id': self.start_id})
		self.word2idx.update({'end_id': self.end_id})
		self.idx2word = self.idx2word + ['start_id', 'end_id']

		self.src_vocab_size = self.src_vocab_size + 2

		# Init Session
		tf.reset_default_graph()
		self.sess = tf.Session(config=sess_config)

    	# Inference Data Placeholders
		self.encode_seqs = tf.placeholder(dtype=tf.int64, shape=[1, None], name="encode_seqs")
		self.decode_seqs = tf.placeholder(dtype=tf.int64, shape=[1, None], name="decode_seqs")

		self.net, self.net_rnn = self.create_model(self.encode_seqs, self.decode_seqs, self.src_vocab_size, emb_dim, is_train=False, reuse=False)
		self.y = tf.nn.softmax(self.net.outputs)

		# Init Vars
		self.sess.run(tf.global_variables_initializer())

		# Load Model
		tl.files.load_and_assign_npz(sess=self.sess, name='model-25.npz', network=self.net)

	def infer(self, seed):
		seed_id = [self.word2idx.get(w, self.unk_id) for w in seed.split(" ")]

		# Encode and get state
		y = tf.nn.softmax(self.net.outputs)
		state = self.sess.run(self.net_rnn.final_state_encode,
			{self.encode_seqs: [seed_id]})
		# Decode, feed start_id and get first word [https://github.com/zsdonghao/tensorlayer/blob/master/example/tutorial_ptb_lstm_state_is_tuple.py]
		o, state = self.sess.run([y, self.net_rnn.final_state_decode],
			{self.net_rnn.initial_state_decode: state,
			self.decode_seqs: [[self.start_id]]})
		w_id = tl.nlp.sample_top(o[0], top_k=3)
		w = self.idx2word[w_id]
		# Decode and feed state iteratively
		sentence = [w]
		for _ in range(30): # max sentence length
			o, state = self.sess.run([y, self.net_rnn.final_state_decode],
				{self.net_rnn.initial_state_decode: state,
				self.decode_seqs: [[w_id]]})
			w_id = tl.nlp.sample_top(o[0], top_k=2)
			w = self.idx2word[w_id]
			if w_id == self.end_id:
				break
			sentence = sentence + [w]
		response = ' '.join(sentence)
		return response

if __name__ == "__main__":
	seq = SeqModel()
	metadata = seq.load_data()
	seq.load_model(metadata)
	while True:
		query = input('Enter Query: ')
		response = seq.infer(query)
		print(" >", response)

