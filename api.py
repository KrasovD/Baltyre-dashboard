import json
import pprint
from fast_bitrix24 import Bitrix
import time
from datetime import datetime, timedelta
# замените на ваш вебхук для доступа к Bitrix24
import webhook as web
b = Bitrix(web.webhook)

def find_managers_name(manager_id: list) -> dict:

    managers = b.get_by_ID('user.get', manager_id, 'id')
    m_dict = dict()
    for id in manager_id:
        m_dict[id] = managers[str(id)][0]['NAME'] + ' ' + managers[str(id)][0]['LAST_NAME']
    return m_dict

def find_companys_name(company_ids: list) -> dict: 
    c_dict = dict()
    #try:
    '''        with open('files/companys.json', 'r') as comp:
            companys = json.load(comp)
    except:
        with open('files/companys.json', 'w') as comp:'''
    companys = b.get_all('crm.company.list')

    for company in companys:
        if company['ID'] in company_ids:
            c_dict[company['ID']] = company['TITLE']
    return c_dict

class Deal():
    def _stage(self, stage_id):
        d_stage = {
            'WON': 'Выиграна', 'LOSE': 'Проиграна', 
            'FINAL_INVOICE': 'Выставлен счет', 
            'NEW': 'Новая', '1': '1 этап', 
            '2': '2 этап', '3': '3 этап',
            'EXECUTING': 'В работе'}
        try:
            return d_stage[stage_id]
        except:
            return stage_id
        

    def __init__(self, ID, TITLE, TYPE_ID, STAGE_ID, OPPORTUNITY,
                COMPANY_ID, BEGINDATE, CLOSEDATE, ASSIGNED_BY_ID,
                **kwargs) -> None:
        self.id = ID # ид сделки
        self.title = TITLE # название
        self.type = TYPE_ID # тип
        self.stage = STAGE_ID #self._stage(STAGE_ID) # этап
        self.sum = OPPORTUNITY # сумма
        self.company = COMPANY_ID # ид компании
        if BEGINDATE:
            self.begin = datetime.strptime(BEGINDATE, '%Y-%m-%dT%H:%M:%S+03:00') # дата открытии сделки
        if CLOSEDATE:
            self.close = datetime.strptime(CLOSEDATE, '%Y-%m-%dT%H:%M:%S+03:00') # дата закрытии сделки
        self.manager_id = ASSIGNED_BY_ID # ид ответсвенного менеджера

    def __repr__(self) -> str:
        return '{}  Компания: {}    Сумма: {}'.format(
            self.title, 
            self.company,
            self.sum
            )


def all_managers_deals():
    #deal = Deal(**b.get_by_ID('crm.deal.get', [2418], 'id')['2418']) # инфо о сделке 
    b.slow(5)
    date_now = datetime.now() 
    deals_list = list()
    manager_deals = dict() #  все сделки менеджеров 
    company_set = set() # список компаний
    [deals_list.append(Deal(**deal)) for deal in b.get_all('crm.deal.list')] 
    
    #отбор сделок текущего месяца 
    for deal in deals_list:
        if deal.stage !='WON' or (deal.stage == 'WON' and (deal.close.month, deal.close.year) == (date_now.month, date_now.year)): 
            try:
                manager_deals[deal.manager_id].append(deal)
            except:
                manager_deals[deal.manager_id] = list()
            if deal.company != '0':
                company_set.add(deal.company)
    companys = find_companys_name(company_set)
    managers = find_managers_name(manager_deals.keys())
    
    for manager in manager_deals:
        data = dict()
        data[managers[manager]] = dict()
        for deal in manager_deals[manager]:
            try:
                deal.company = companys[deal.company]
            except:
                deal.company = '-'
            try:
                data[managers[manager]][deal.stage].append(deal)
            except:
                data[managers[manager]][deal.stage] = list()
                data[managers[manager]][deal.stage].append(deal)
                data[managers[manager]]['sum/' + deal.stage] = 0
            data[managers[manager]]['sum/' + deal.stage] += round(float(deal.sum))
        try:
            data[managers[manager]]['sum/WON']
        except:
            data[managers[manager]]['sum/WON'] = 0

        yield data


def all_json():
    #deal = Deal(**b.get_by_ID('crm.deal.get', [2418], 'id')['2418']) # инфо о сделке 
    b.slow(5)
    date_now = datetime.now() 
    deals_list = list()
    manager_deals = dict() #  все сделки менеджеров 
    company_set = set() # список компаний
    [deals_list.append(Deal(**deal)) for deal in b.get_all('crm.deal.list')] 
    
    #отбор сделок текущего месяца 
    for deal in deals_list:
        if deal.stage !='WON' or (deal.stage == 'WON' and (deal.close.month, deal.close.year) == (date_now.month, date_now.year)): 
            try:
                manager_deals[deal.manager_id].append(deal)
            except:
                manager_deals[deal.manager_id] = list()
            if deal.company!= '0':
                company_set.add(deal.company)
            else:
                company_set.add('-')
    companys = find_companys_name(company_set)
    managers = find_managers_name(manager_deals.keys())
    
    for manager in manager_deals:
        data = dict()
        data[managers[manager]] = dict()
        for deal in manager_deals[manager]:
            try:
                deal.company = companys[deal.company]
            except:
                pass
            try:
                data[managers[manager]][deal.stage].append(deal.__repr__())
            except:
                data[managers[manager]][deal.stage] = list()
                data[managers[manager]][deal.stage].append(deal.__repr__())
                data[managers[manager]]['sum/' + deal.stage] = 0
            data[managers[manager]]['sum/' + deal.stage] += round(float(deal.sum))
        try: 
            data[managers[manager]]['sum/Выиграна']
        except:
            data[managers[manager]]['sum/Выиграна'] = 0
        yield data

if __name__ == '__main__':
    b = Bitrix(web.webhook)

    print(b.get_by_ID('crm.company.get', [2]))



