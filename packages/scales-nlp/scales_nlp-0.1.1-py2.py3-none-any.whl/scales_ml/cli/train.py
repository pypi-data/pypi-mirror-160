import click
from scales_nlp import train as run_train
from scales_nlp.utils import DEFAULT_TRAINING_ARGS
import pandas as pd

@click.command()
@click.argument('data-path')
@click.option('--output-dir', default='outputs', help='Path to save model outputs')
@click.option('--task', default=None, help='Task to train')
@click.option('--model-name', default=DEFAULT_TRAINING_ARGS['model_name'], help='Huggingface model name')
@click.option('--epochs', default=DEFAULT_TRAINING_ARGS['epochs'], help='Number of training epochs')
@click.option('--train-batch-size', default=DEFAULT_TRAINING_ARGS['train_batch_size'], help='Train batch size')
@click.option('--eval-batch-size', default=DEFAULT_TRAINING_ARGS['eval_batch_size'], help='Evaluation batch size')
@click.option('--gradient-accumulation-steps', default=DEFAULT_TRAINING_ARGS['gradient_accumulation_steps'], help='Artificially increase the train batch size')
@click.option('--max-length', default=DEFAULT_TRAINING_ARGS['max_length'], help='Truncate inputs to max token sequence length')
@click.option('--learning-rate', default=DEFAULT_TRAINING_ARGS['learning_rate'], help='Learning rate')
@click.option('--warmup-ratio', default=DEFAULT_TRAINING_ARGS['warmup_ratio'], help='Learning rate warmup')
@click.option('--weight-decay', default=DEFAULT_TRAINING_ARGS['weight_decay'], help='Weight decay for AdamW')
@click.option('--eval-split', default=DEFAULT_TRAINING_ARGS['eval_split'], help='Proportion of data to use for evaluation')
@click.option('--metric', default=None, help='Name of metric to use for evaluation')
@click.option('--save-steps', default=DEFAULT_TRAINING_ARGS['save_steps'], help='Save model checkpoint every n steps')
@click.option('--push', default=None, help='model id to push to hub')
@click.option('--overwrite/no-overwrite', default=False, help='Overwrite output dir if it exists')
@click.option('--multi-label-delimiter', default='|', help='Delimiter for splitting labels in multi-label-classification task')
def train(
        data_path, output_dir, task, model_name, epochs, 
        train_batch_size, eval_batch_size, gradient_accumulation_steps,
        max_length, learning_rate, warmup_ratio, weight_decay,
        eval_split, metric, save_steps, overwrite, push, multi_label_delimiter):
    
    data = pd.read_csv(data_path)
    texts = list(data['text'].values)
    labels = list(data['label'].values)
    if task == 'multi-label-classification':
        labels = [labels.split(multi_label_delimiter) for labels in labels]
        
    run_train(
        output_dir, texts, labels, 
        model_name=model_name, task=task, max_length=max_length, 
        eval_split=eval_split, metric=metric, epochs=epochs,
        train_batch_size=train_batch_size, eval_batch_size=eval_batch_size, 
        gradient_accumulation_steps=gradient_accumulation_steps, learning_rate=learning_rate,
        warmup_ratio=warmup_ratio, weight_decay=weight_decay,
        save_steps=save_steps, push=push, overwrite=overwrite,
    )

if __name__ == '__main__':
    train()