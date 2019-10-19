import requests, json, time, os

interval = .100
output_dir = 'data'
debug = True

def output(s):
    if debug:
        print(s)

def get(url):
    
    result = requests.get(url)

    while not result.ok:
        output('Could not query for "{url}". Trying again after {interval:0.0f} milliseconds.'.format(url=url, interval=interval*1000))
        time.sleep(interval)
        result = requests.get(url)
    
    output('Successfully queried "{url}".'.format(url=url))
    return json.loads(result.text)

def scrap():
    makes_result = get('http://fipeapi.appspot.com/api/1/carros/marcas.json')

    for make in makes_result:
        make_id = make['id']
        models = get('http://fipeapi.appspot.com/api/1/carros/veiculos/{make_id}.json'.format(make_id=make_id))
        make['models'] = models

        for model in models:
            model_id = model['id']
            versions = get('http://fipeapi.appspot.com/api/1/carros/veiculo/{make_id}/{model_id}.json'.format(make_id=make_id, model_id=model_id))

            model['versions'] = versions

            for version in versions:
                version_id = version['id']
                version_details = get('http://fipeapi.appspot.com/api/1/carros/veiculo/{make_id}/{model_id}/{version_id}.json'.format(make_id=make_id, model_id=model_id, version_id=version_id))

                version['details'] = version_details

    output('Car models successfully retrieved. Outputting file...')

    with open(os.path.join(output_dir, 'cars.json'), 'w') as json_file:
        json.dump(makes_result, json_file)

    output('Done.')
    output('\n\n\n\n\n\n==================== FINISHED ====================\n\n\n\n\n\n')

def init_defaults():
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

def main():
    print('Retrieving data...')
    init_defaults()
    scrap()
    print('All data retrieved.')

# ------------------------------------------------------------------------------------------ #

if __name__ == '__main__':
    main()