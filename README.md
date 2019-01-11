# Seq2Seq-Chatbot
Using seq2seq model to train a simple chatbot.

### Training

```
python train.py --batch-size 128 --num-epochs 30 -lr 0.001
```

### Inference

```
python test.py
```

### Inference (Web)

```
cd mysite/
python manage.py (*.*.*.*:*)
```

*192.168.\*.\*:\** is your IP address and port which is optional.



## Corpus

* Cornell Movie Dataset
* Twitter Dialog Dataset
* Mixed Dataset (including cornell, twitter, greeting, history, conversation and so on) maybe will be updated in the future.



