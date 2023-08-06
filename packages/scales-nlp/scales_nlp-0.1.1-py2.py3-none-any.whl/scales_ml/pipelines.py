from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification
import torch
from toolz import partition_all
from tqdm import tqdm
from scales_nlp.utils import convert_default_binary_outputs, config

def pipeline(pipeline_name, task=None, **kwargs):
    if kwargs.get('use_auth_token', False) == True and 'HUGGING_FACE_TOKEN' in config:
        kwargs['use_auth_token'] = config['HUGGING_FACE_TOKEN']

    if task is not None:
        return task_pipeline(pipeline_name, task, **kwargs)
    elif pipeline_name.startswith('ontology-'):
        kwargs['use_auth_token'] = kwargs.get('use_auth_token', True)
        return OntologySingleLabelPipeline('scales-okn/%s' % pipeline_name, **kwargs)
    elif pipeline_name == 'entity-resolution':
        kwargs['use_auth_token'] = kwargs.get('use_auth_token', True)
        return EntityResolutionPipeline('scales-okn/%s' % pipeline_name, **kwargs)
    raise Exception("'%s' is not a valid pipeline name.  If '%s' is a model name, please specify the task argument" % pipeline_name, pipeline_name)


def task_pipeline(model_name, task, **kwargs):
    if task == 'classification':
        return ClassificationPipeline(model_name, **kwargs)
    raise Exception("'%s' is not a valid task name.  This should be one of 'classifier' or 'ner'" % task)

class BasePipeline(object):
    def __init__(self, model_name, max_length=512, device=None, use_auth_token=False):
        self.device = device if device is not None else -1 if not torch.cuda.is_available() else torch.cuda.current_device()
        self.max_length = max_length
        self.use_auth_token = use_auth_token
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=self.use_auth_token)
    
    def place_on_device(self, obj):
        if self.device >= 0:
            return obj.to(self.device)
        else:
            return obj.to('cpu')

    def process_inputs(self, examples):
        return examples
    
    def process_predictions(self, predictions):
        return predictions
    
    def get_inputs(self, texts):
        return self.tokenizer(texts, padding='max_length', max_length=self.max_length, truncation=True, return_tensors='pt')
    
    def generate_batches(self, examples, batch_size, verbose):
        examples = self.process_inputs(examples)
        batches = list(partition_all(batch_size, examples))
        for batch in tqdm(batches, disable=not verbose):
            yield self.place_on_device(self.get_inputs(list(batch)))


class ClassificationPipeline(BasePipeline):
    def __init__(self, model_name, multi_label=False, num_labels=None, **kwargs):
        super().__init__(model_name, **kwargs)
        self.multi_label = multi_label

        model_args = {'use_auth_token': self.use_auth_token}
        if num_labels is not None:
            model_args['num_labels'] = num_labels

        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, **model_args)
        self.model = self.place_on_device(self.model)

    def __call__(self, examples, return_scores=False, prediction_threshold=0.5, batch_size=4, verbose=True, shuffle=False):
        predictions = []
        for batch in self.generate_batches(examples, batch_size, verbose):
            outputs = self.model(**batch)
            logits = outputs.logits.detach().cpu()

            if self.multi_label or self.model.num_labels == 1:
                scores = torch.sigmoid(logits)
            else:
                scores = torch.softmax(logits, dim=-1)
            
            for i in range(len(scores)):
                prediction = {self.model.config.id2label[label_id]: score.item() for label_id, score in enumerate(scores[i])}
                if not return_scores:
                    if self.multi_label:
                        prediction = [label for label, score in prediction.items() if score > prediction_threshold]
                    else:
                        prediction = max(prediction.items(), key=lambda x: x[1])[0]
                predictions.append(prediction)
        
        return self.process_predictions(predictions)


## Custom Pipelines

class EntityResolutionPipeline(ClassificationPipeline):
    def process_inputs(self, examples):
        if not any(isinstance(examples[0], x) for x in [list, tuple]):
            raise Exception('Entity resolution pipeline requires a list of pairs of names e.g. [["Jane", "Doe"], ["John", "Smith"]]')
        return ["%s vs. %s" % (x[0], x[1]) for x in examples]

    def process_predictions(self, predictions):
        return convert_default_binary_outputs(predictions)


class OntologySingleLabelPipeline(ClassificationPipeline):
    def process_predictions(self, predictions):
        return convert_default_binary_outputs(predictions)




