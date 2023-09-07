from bs4 import BeautifulSoup
import requests

import services.utils as utils
import services.file as file

def get_all_jobs_by_letter (letter, index = 0):
    url = 'https://www.salario.com.br/tabela-salarial/?cargos=' + letter.upper()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='listas')

    jobs = []
    try: 
        for tr in table.find_all('tr'):
            index += 1
            tds = tr.find_all('td')
            if len(tds) > 0:
                jobs.append({
                    'index': index,
                    'cbo': tds[0].text,
                    'cargo': tds[1].text,
                    'idPost': ''
                })
        return jobs
    except:
        return False

def get_id_post_by_job (job):
    try: 
        urls = [
            'https://www.salario.com.br/profissao/' + utils.normalize(job['cargo']) + '-cbo-' + job['cbo'],
            'https://www.salario.com.br/profissao/' + utils.normalize(job['cargo']) + '-' + job['cbo']
        ]
        headers = requests.get(urls[0]).headers
        idPost = utils.checkIdPost(headers['Link'])
        if (idPost):
            return idPost
        else:
            headers = requests.get(urls[1]).headers
            idPost = utils.checkIdPost(headers['Link'])
            if (idPost):
                return idPost
            else:
                file.changeFile([job['index'], job['cbo'], job['cargo']], 'errors')
                return False
    except:
        file.changeFile([job['index'], job['cbo'], job['cargo']], 'errors')
        return False

def get_states_defered (cbo, cargo, idPost):
    url = 'https://www.salario.com.br/tabela-por-localidade/'
    formData = {
        "cbo": cbo,
        "cargo": cargo,
        "tipo_tabela": 'tabela_estados',
        "idPost": idPost
    }
    page = requests.post(url, data=formData)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='listas')

    try:
        states = []

        for tr in table.find('tbody').find_all('tr'):
            td =  list(filter(lambda item: item != '', tr.text.split('\n')))
            if len(td) > 1:
                states.append({
                    'estado': td[0],
                    'salario': td[3]
                })
                
        return states
    except:
        return False