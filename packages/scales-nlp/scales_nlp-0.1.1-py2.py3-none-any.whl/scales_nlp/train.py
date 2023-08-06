from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification
from transformers import TrainingArguments, Trainer
from datasets import Dataset
import torch
import numpy as np
import pandas as pd
from pathlib import Path
import click
import shutil 
import os
from scales_nlp.metrics import metrics
from scales_nlp.utils import DEFAULT_TRAINING_ARGS, config

def convert_to_dataset(texts, labels, tokenizer, max_length):
    inputs = tokenizer(texts, padding="max_length", max_length=max_length, truncation=True)
    inputs['label'] = labels
    return Dataset.from_dict(inputs)

def infer_task_from_labels(labels):
    if any(isinstance(labels[0], x) for x in (str, int, bool)):
        return 'classification'
    elif isinstance(labels[0], list):
        for label_set in labels:
            if len(label_set) > 0:
                if any(isinstance(label_set[0], x) for x in (str, int)):
                    return 'multi-label-classification'
                elif isinstance(label_set[0], dict):
                    return 'ner'
    raise Exception("Unable to infer task type")

def train(
        output_dir, texts, labels, 
        model_name=DEFAULT_TRAINING_ARGS['model_name'], task=None, max_length=DEFAULT_TRAINING_ARGS['max_length'],
        eval_split=DEFAULT_TRAINING_ARGS['eval_split'], metric=None, epochs=DEFAULT_TRAINING_ARGS['epochs'], 
        train_batch_size=DEFAULT_TRAINING_ARGS['train_batch_size'], eval_batch_size=DEFAULT_TRAINING_ARGS['eval_batch_size'],
        gradient_accumulation_steps=DEFAULT_TRAINING_ARGS['gradient_accumulation_steps'],
        learning_rate=DEFAULT_TRAINING_ARGS['learning_rate'], warmup_ratio=DEFAULT_TRAINING_ARGS['warmup_ratio'],
        weight_decay=DEFAULT_TRAINING_ARGS['weight_decay'], save_steps=DEFAULT_TRAINING_ARGS['save_steps'],
        push=None, overwrite=False, callbacks=[]):

    if task is None:
        task = infer_task_from_labels(labels)
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    if task == 'classification':
        label_names = list(sorted(list(set(labels))))
        labels = [label_names.index(label) for label in labels]
    elif task == 'multi-label-classification':
        label_names = list(sorted(list(set([x for y in labels for x in y]))))
        labels = [[int(label_names[i] in label_set) for i in range(len(label_names))] for label_set in labels]
    
    data = list(zip(texts, labels))
    np.random.shuffle(data)
    split = int(eval_split * len(data))

    train_data = {'texts': [x[0] for x in data[split:]], 'labels': [x[1] for x in data[split:]]}
    eval_data = {'texts': [x[0] for x in data[:split]], 'labels': [x[1] for x in data[:split]]}
    train_dataset = convert_to_dataset(**train_data, tokenizer=tokenizer, max_length=max_length)
    eval_dataset = convert_to_dataset(**eval_data, tokenizer=tokenizer, max_length=max_length)

    if metric is not None:
        compute_metrics = metrics[metric]
    else:
        compute_metrics = metrics['f1_score']
    
    if task == 'multi-label-classification':
        trainer_class = Trainer
    else:
        trainer_class = Trainer

    if 'classification' in task:
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(label_names))
        model.config.label2id = {label_names[i]: i for i in range(len(label_names))}
        model.config.id2label = {i: label_names[i] for i in range(len(label_names))}
    elif task == 'ner':
        model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(label_names))


    output_dir = Path(output_dir)
    args = TrainingArguments(
        output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=eval_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        warmup_ratio=warmup_ratio,
        weight_decay=weight_decay,
        eval_steps=save_steps,
        save_steps=save_steps,
        evaluation_strategy='steps',
        load_best_model_at_end=True,
        save_total_limit=1,
        logging_steps=5,
        hub_strategy='end',
        hub_model_id=push,
        hub_token=config['HUGGING_FACE_TOKEN'],
        push_to_hub=push is not None,
    )

    if output_dir.exists():
        if overwrite:
            shutil.rmtree(output_dir)
        else:
            raise Exception("Output directory already exists, please use the overwrite argument to overwrite it")


    trainer = trainer_class(
        model=model,
        tokenizer=tokenizer,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
    )
    for callback in callbacks:
        trainer.add_callback(callback)

    trainer.train()
    results = trainer.evaluate()
    print(results)

    trainer.save_model(output_dir)
    print("Model saved to", output_dir.resolve())

