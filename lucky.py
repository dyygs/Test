# coding: utf-8
import time
import json
import requests
import webbrowser
from urllib.parse import quote


def search_keyword(qusetion, answers):

    header = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Host":
        "www.baidu.com",
        "Cache-Control":
        "no-cache"
    }
    counts = []

    if '不' in qusetion:
        copy_qusetion = qusetion
        qusetion = qusetion.replace('不', '')
        copy_url = 'https://www.baidu.com/s?wd=' + quote(copy_qusetion)
        url = 'https://www.baidu.com/s?wd=' + quote(qusetion)
        webbrowser.open(copy_url)
        req = requests.get(url=url, headers=header).text
        for i in range(len(answers)):
            counts.append(req.count(answers[i]))
        index = counts.index(min(counts))
        print(answers[index] + " : " + str(counts[index]))
        print('******************************************')

    else:
        url = 'https://www.baidu.com/s?wd=' + quote(qusetion)
        webbrowser.open(url)
        req = requests.get(url=url, headers=header).text
        for i in range(len(answers)):
            counts.append(req.count(answers[i]))
        index = counts.index(max(counts))
        if (counts[index] == 0):
            print('无结果')
        else:
            print(answers[index] + " : " + str(counts[index]))
            print('******************************************')
    time.sleep(5)


def get_question(lastQuestion):
    resp = requests.get(
        'http://htpmsg.jiecaojingxuan.com/msg/current', timeout=4).text

    # resp = requests.get('http://localhost:8000/sample.json',
    #                     ).text
    question = ''
    resp_dict = json.loads(resp)
    if resp_dict['msg'] != 'no data':
        question = resp_dict['data']['event']['desc']
        question = question[question.find('.') + 1:question.find('?')]
        answers = eval(resp_dict['data']['event']['options'])
        # question = '哪种动物的乳汁最适合替代人类母乳?'
        # answers = ['牛', '羊', '驴奶']
        if question != lastQuestion:
            print('******************************************')
            print(question)
            print(answers)
            print('******************************************')
            search_keyword(question, answers)
    else:
        question = lastQuestion  
    return question

if __name__ == '__main__':
    lastQuestion = ''
    while True:
        # print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        lastQuestion = get_question(lastQuestion)
        time.sleep(1)