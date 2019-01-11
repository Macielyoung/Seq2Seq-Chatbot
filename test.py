import time

import click
import numpy as np
import tensorflow as tf
import tensorlayer as tl

from sklearn.utils import shuffle
from tensorlayer.layers import DenseLayer, EmbeddingInputlayer, Seq2Seq, retrieve_seq_length_op2

from data.twitter import data

sess_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)

# infer response coresponding to query
def infer(query):
	metadata = initial_setup()

	src_vocab_size = len(metadata['idx2w']) # 8002 (0~8001)
	emb_dim = 1024

	word2idx = metadata['w2idx']   # dict  word 2 index
	idx2word = metadata['idx2w']   # list index 2 word

	unk_id = word2idx['unk']   # 1
	pad_id = word2idx['_']     # 0

	start_id = src_vocab_size  # 8002
	end_id = src_vocab_size + 1  # 8003

	word2idx.update({'start_id': start_id})
	word2idx.update({'end_id': end_id})
	idx2word = idx2word + ['start_id', 'end_id']

	src_vocab_size = tgt_vocab_size = src_vocab_size + 2

    # Init Session
	tf.reset_default_graph()
	sess = tf.Session(config=sess_config)

    # Inference Data Placeholders
	encode_seqs2 = tf.placeholder(dtype=tf.int64, shape=[1, None], name="encode_seqs")
	decode_seqs2 = tf.placeholder(dtype=tf.int64, shape=[1, None], name="decode_seqs")

	net, net_rnn = create_model(encode_seqs2, decode_seqs2, src_vocab_size, emb_dim, is_train=False, reuse=False)
	y = tf.nn.softmax(net.outputs)

    # Init Vars
	sess.run(tf.global_variables_initializer())

    # Load Model
	tl.files.load_and_assign_npz(sess=sess, name='model.npz', network=net)

	"""
	Inference using pre-trained model
	"""
	def inference(seed):
	    seed_id = [word2idx.get(w, unk_id) for w in seed.split(" ")]
	    
	    # Encode and get state
	    state = sess.run(net_rnn.final_state_encode,
	                    {encode_seqs2: [seed_id]})
	    # Decode, feed start_id and get first word [https://github.com/zsdonghao/tensorlayer/blob/master/example/tutorial_ptb_lstm_state_is_tuple.py]
	    o, state = sess.run([y, net_rnn.final_state_decode],
	                    {net_rnn.initial_state_decode: state,
	                    decode_seqs2: [[start_id]]})
	    w_id = tl.nlp.sample_top(o[0], top_k=3)
	    w = idx2word[w_id]
	    # Decode and feed state iteratively
	    sentence = [w]
	    for _ in range(30): # max sentence length
	        o, state = sess.run([y, net_rnn.final_state_decode],
	                        {net_rnn.initial_state_decode: state,
	                        decode_seqs2: [[w_id]]})
	        w_id = tl.nlp.sample_top(o[0], top_k=2)
	        w = idx2word[w_id]
	        if w_id == end_id:
	            break
	        sentence = sentence + [w]
	    return sentence

    # infer
	sentence = inference(query)
	response = ' '.join(sentence)
	return response

"""
Creates the LSTM Model
"""
def create_model(encode_seqs, decode_seqs, src_vocab_size, emb_dim, is_train=True, reuse=False):
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

"""
Initial Setup
"""
def initial_setup():
	metadata, idx_q, idx_a = data.load_data(PATH='data/twitter/')
	return metadata

if __name__ == '__main__':
	# metadata = initial_setup()
	# print(metadata)
	while True:
		input_seq = input('Enter Query: ')
		response = infer(input_seq)
		print(" >", response)