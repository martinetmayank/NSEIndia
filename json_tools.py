import json


def write_oa(response):
    filename = 'oa_data.json'
    file = open(filename, mode='w+')
    print('Data is being written to the file', filename, '...')
    file.write(json.dumps(response, sort_keys=True, indent=4))
    file.close()
