import click
import json
from pathlib import Path
from scales_nlp.utils import CONFIG_KEYS, CONFIG_PATH, DEVELOPER_CONFIG_KEYS, load_json

@click.command()
@click.option('--reset/--no-reset', default=False, help='Delete existing keys in config')
@click.option('--dev/--no-dev', default=False, help='Developer mode')

def configure(reset, dev):
    config = {}
    if CONFIG_PATH.exists() and not reset:
        config = load_json(CONFIG_PATH)
    elif dev:
        developer_config_path = Path('/home/nathan/scales-nlp/developer_config.json')
        if developer_config_path.exists():
            config = load_json(developer_config_path)
    
    print('(leave blank to keep existing value)')
    config_keys = CONFIG_KEYS + DEVELOPER_CONFIG_KEYS if dev else CONFIG_KEYS
    for key in config_keys:
        current_value = config.get(key, None)
        prompt = key
        if current_value is not None:
            mask_len = max([len(current_value) - 4, 0])
            masked_value = '*' * mask_len + current_value[mask_len:]
            prompt += ' [{}]'.format(masked_value)
        value = input(prompt + ': ')
        if not value:
            value = current_value
        config[key] = value
    
    with open(CONFIG_PATH, 'w') as w:
        w.write(json.dumps(config, indent=4))
    print('configuration saved to {}'.format(CONFIG_PATH.resolve()))

if __name__ == '__main__':
    configure()