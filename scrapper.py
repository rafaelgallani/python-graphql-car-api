import requests, json, time, os

interval = .100
output_dir = 'data'

def get(url):
    
    result = requests.get(url)

    while not result.ok:
        print('Could not query for "{url}". Trying again after {interval:0.0f} milliseconds.'.format(url=url, interval=interval*1000))
        time.sleep(interval)
        result = requests.get(url)
    
    print('Successfully queried "{url}".'.format(url=url))
    return json.loads(result.text)

def scrap():
    makes_result = get('http://fipeapi.appspot.com/api/1/carros/marcas.json')

    for make in makes_result:
        models = get('http://fipeapi.appspot.com/api/1/carros/veiculos/{make}.json'.format(make = make['id']))
        make['models'] = models

    print('Car models successfully retrieved. Outputting file...')
    with open(os.path.join(output_dir, 'cars.json'), 'w') as output:
        json.dump(makes_result, output)

    print('Done.')
    print('\n\n\n\n\n\n==================== FINISHED ====================\n\n\n\n\n\n')

def init_defaults():
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

def main():
    init_defaults()
    scrap()

# ------------------------------------------------------------------------------------------ #

if __name__ == '__main__':
    main()