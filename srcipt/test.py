from prepare import prepare
from static import *
import json

if __name__ == '__main__':
    
    input_file = testmedia_dir + '/origin.mov'

    with open(config_dir + '/config.json', 'r') as f:
        convert_targets = json.load(f)['convert_targets']

    prepare(input_file, 15, testmedia_dir, convert_targets)