#-*-coding:GBK -*-
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import random
import copy
from app01.gift_list import all_gift_list
# Create your views here.

luckey_men = ""
def choose_people(request):



    global luckey_men


    if request.method == 'GET':

        # 重置按钮
        if request.GET.get('is_restart'):
            luckey_men = ""

        luckey_men_list = luckey_men.split(',')
        print(luckey_men_list)
        return render(request, "choose_people.html", {"luckey_men" : luckey_men, "luckey_men_list" : luckey_men_list})

    else:
        if request.POST.getlist('luckymen'):

            for i, item in enumerate(request.POST.getlist('luckymen')):
                if i == 0:
                    luckey_men = item
                else:
                    luckey_men += "," + item
            return HttpResponse('ok')

        else:
            response = {"is_success" : True}
            return JsonResponse(response)



del_gift_list = []

def choose_gift(request):

    if request.method == 'GET':

        gift_list = []
        print(del_gift_list)

        for gift in all_gift_list:
            if gift in del_gift_list:
                pass
            else:
                gift_list.append(gift)



        #这里是为了最后，当礼物没有8个了，补充的礼物卡



        if len(gift_list) >= 8:
            sample_list = random.sample(gift_list, 8)

            sample_list = copy.deepcopy(sample_list)
            for item in sample_list:
                item['is_click'] = True

        else:

            # 不足8个礼物后，剩余的礼物仍然需要点击事件
            for item in gift_list:
                item['is_click'] = True

            # 补充的遗憾牌不能点击
            for i in range(8 - len(gift_list)):
                gift_list.append({"name" : "很遗憾！", "is_click" : False})
            sample_list = random.sample(gift_list, 8)


        print(sample_list)
        return render(request, "choose_gift.html", {"gift_list" : sample_list, "del_gift_list" : len(del_gift_list), "gift_left" : 75-len(del_gift_list)})



    else:
        if request.POST.get('is_restart'):
            del_gift_list.clear()
        else:
            del_gift_list.append({"numbering" : int(request.POST.get('delte_gift_numbering').strip()), "name" : request.POST.get('delte_gift_name').strip()})
        return HttpResponse('ok')


