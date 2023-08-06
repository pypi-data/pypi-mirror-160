from datasets import load_metric
import numpy as np

acc_metric = load_metric("accuracy")
f1_metric = load_metric("f1")
precision_metric = load_metric("precision")
recall_metric = load_metric("recall")

def f1_score(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        'accuracy': acc_metric.compute(predictions=predictions, references=labels)['accuracy'],
        'f1': f1_metric.compute(predictions=predictions, references=labels)['f1'],
        'precision': precision_metric.compute(predictions=predictions, references=labels)['precision'],
        'recall': recall_metric.compute(predictions=predictions, references=labels)['recall'],
    }


metrics = {
    'f1_score': f1_score,
}

