import requests, json, time, os

interval = .100
output_dir = 'data'
debug = False
base_url = 'https://veiculos.fipe.org.br/api/veiculos/'

def output(s):
    if debug:
        print(s)

def post(url, params):
    
    if not url.startswith(base_url):
        url = base_url + url

    if len(params.items()):
        url += '?'
        for key, value in params.items():
            url += '{key}={value}&'.format(key=key, value=value)
        url = url[:-1]

    request_completed = False
    exception_counter = 0
    while not request_completed:
        try:
            result = requests.post(url)

            while not result.ok:
                output('Could not query for "{url}". Trying again after {interval:0.0f} milliseconds.'.format(url=url, interval=interval*1000))
                time.sleep(interval)
                result = requests.post(url)

            request_completed = True        
            
            output('Successfully queried "{url}".'.format(url=url))
            return json.loads(result.text)

        except Exception as e:
            exception_counter += 1
            print('=== EXCEPTION ===\n{}'.format(e))
            request_completed = False

            if exception_counter >= 10:
                raise Exception('More than 10 exceptions.')


def scrap():

    done = False

    processed_makes = set()
    processed_models = set()
    processed_versions = set()

    makes_result = None

    while not done:
        
        try:

            if not makes_result:
                makes_result = post('ConsultarMarcas', {
                    'codigoTabelaReferencia':247,
                    'codigoTipoVeiculo': 1,
                })   

            for make in makes_result:
                make_key = str(make['Value'])

                if not make_key in processed_makes:
                    make_id = make['Value']
                    models = post('ConsultarModelos', {
                        'codigoTabelaReferencia':247,
                        'codigoTipoVeiculo': 1,
                        'codigoMarca': make_id,
                    })
                    make['models'] = models['Modelos']
                    
                    for model in make['models']:
                        model_id = model['Value']
                        model_key = '_'.join([str(make_id), str(model_id)])

                        if not model_key in processed_models:
                            
                            versions = post('ConsultarAnoModelo', {
                                'codigoTabelaReferencia':247,
                                'codigoTipoVeiculo': 1,
                                'codigoMarca': make_id,
                                'codigoModelo': model_id,
                            })

                            model['versions'] = versions

                            for version in versions:
                                version_id = version['Value']
                                version_key = '_'.join([str(make_id), str(model_id), str(version_id)])

                                if not version_key in processed_versions:
                                    
                                    version_year, version_fuel_type = version_id.split('-')
                                    
                                    version_details = post('ConsultarValorComTodosParametros', {
                                        'codigoTabelaReferencia':247,
                                        'codigoTipoVeiculo': 1,
                                        'codigoMarca': make_id,
                                        'codigoModelo': model_id,
                                        'anoModelo': version_year,
                                        'codigoTipoCombustivel': version_fuel_type,
                                        'tipoVeiculo': 'carro',
                                        'tipoConsulta': 'tradicional',
                                    })

                                    version['details'] = version_details

                                    print('Car retrieved => ({year}) - {make} {car} - {timestamp}'.format(
                                        make=version['details']['Marca'], 
                                        car=version['details']['Modelo'], 
                                        timestamp=version['details']['DataConsulta'],
                                        year=str(version['details']['AnoModelo'])
                                    ))
                                    processed_versions.add(version_key)
                            
                            processed_models.add(model_key)
                    
                    processed_makes.add(make_id)
            
            done = True

        except Exception as e:
            done = False
            print('=== EXCEPTION ===\n{}'.format(e))
            output('Exception occurred. Retrying...')

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