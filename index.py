import time

import services.file as file
import services.scrap as scrap
import services.utils as utils

# 'https://www.salario.com.br/tabela-salarial/?cargos={letter}' -> all jobs by letter
# 'https://www.salario.com.br/profissao/' -> job page
# 'https://www.salario.com.br/tabela-por-localidade/' -> all states salaries

def createFiles ():
    file.writeFile(['index', 'cbo', 'cargo', 'idPost'], 'clean-jobs')
    file.writeFile(['index', 'cbo', 'cargo', 'idPost'], 'jobs')
    file.writeFile(['index', 'cbo', 'cargo'], 'errors')

def makeJobs (letters = 'abcdefghijklmnopqrstuvwxyz'):
    for letter in letters:
        utils.porcentage(letters.index(letter), letters.__len__())
        index = file.readFile('clean-jobs').__len__()
        jobs = scrap.get_all_jobs_by_letter(letter, index)
        if (jobs):
            for job in jobs:
                writebleJob = [job['index'], job['cbo'], job['cargo'], job['idPost']]
                file.changeFile(writebleJob, 'clean-jobs')

def getIdsPost ():
    jobs = file.readFile('clean-jobs')
    for job in jobs:
        utils.porcentage(jobs.index(job), jobs.__len__())
        if job['idPost'] == '':
            idPost = scrap.get_id_post_by_job(job)
            if (idPost):
                job['idPost'] = idPost
                file.changeFile([job['index'], job['cbo'], job['cargo'], job['idPost']], 'jobs')

def getStates ():
    jobs = file.readFile('jobs')
    for job in jobs:
        utils.porcentage(jobs.index(job), jobs.__len__())
        if job['idPost'] != '':
            states = scrap.get_states_defered(job['cbo'], job['cargo'], job['idPost'])
            filename = 'jobs/'+utils.normalize(job['cargo'])
            file.writeFile(['estado', 'salario'], filename)
            for state in states:
                if (state):
                    file.changeFile([state['estado'], state['salario']], filename)

def __init__ ():
    print('Criando arquivos...')
    createFiles()
    print('Adicionando cargos...')
    makeJobs()
    print('Buscando os Post ids...')
    getIdsPost()
    print('Buscando os salários...')
    getStates()

__init__()