# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------------
# Deal Or No Deal
# Copyright © 2022-2024 Sergey Chernov aka Gamer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random as rnd
from enum import Enum
import codecs
import time
from threading import Timer
import statistics as st
root = tk.Tk()
root.geometry("1160x800")
root.resizable(width=False, height=False)
cases_pos_x = [2,3.5,5,6.5,8,9.5,11, 2.5,4,5.5,7,8.5,10, 3,4.5,6,7.5,9, 3.5,5,6.5,8]
cases_pos_y = [1]*7 +[2.5]*6 +[4]*5 +[5.5]*4
cases_size = [75, 50] #60, 40
canvas = tk.Canvas(root, width=800, height=630, bg='#dfdfdf')
canvas.place(x=5,y=5)
valizy = []
nomera = []
sums_on_tableau = []
swap_was_offered = False
cases_listofdicts = []
deal_was_made = False
winnings = 0


class chumodan(Enum):
    choosing = 0
    open_enabled = 1
    open_disabled = 2
    swap_cases = 3
    open_your_own = 4
    end = 5


def doSomething():
    if tk.messagebox.askyesno("Exit", "Do you want to quit the application?"):
        log.close()
        root.destroy()


def until_next_offer(qq):
    l = 0
    while True:
        qq-=1
        l+=1
        if (qq in bank):
            break
    return l


def number_of_zeros(i):
    countZero = 0
    while (i % 10 == 0):
        i //= 10
        countZero += 1
    return countZero


def offer_money(ok):
    global offer
    m = st.mean(ok)
    md = st.median(ok)
    if (len(ok) > 4) or (max(ok) > 5):
        offer = (m + md) / 2
        if (len(ok) >= 4):
            offer = offer * ((19 - len(ok)) / 3) / 7.5
            offer = offer * rnd.randint(90, 110) // 100
        elif (len(ok) == 3):
            offer = st.mean(ok)
        elif (len(ok) == 2):
            offer = rnd.uniform(ok[0] * 0.65 + ok[1] * 0.35, ok[0] * 0.4 + ok[1] * 0.6)
        offer = int(offer)
    else:
        offer = st.mean(ok)
    noz = number_of_zeros(max(ok))
    if (noz >= 4):
        offer = int(round(offer, (rnd.randint(-3, -2))))
    elif (noz == 3) or (max(ok) == 2500):
        offer = int(round(offer, (rnd.randint(-2, -1))))
    elif (max(ok) >= 50):
        offer = int(round(offer, 0))
    else:
        offer = round(offer, 2)
    return offer

def offer_swap():
    global stage
    if not(deal_was_made):
        log.write("Банк предлагает обмен.\n")
        if tk.messagebox.askyesno("ОБМЕН", "Банк предлагает поменять чемодан. Вы согласны?"):
            stage = chumodan.swap_cases
            log.write("Игрок соглашается.")
            tk.messagebox.showinfo("Выбор", "Выберите чемодан, на который хотите поменять свой")
        else:
            stage = chumodan.open_enabled
            if len(sums) > 4:
                tk.messagebox.showinfo("Откройте ещё чемодан",
                                       "До предложения банка осталось чемоданов: " + str(until_next_offer(len(sums))))
    else:
        log.write("Банк предложил бы обмен.\n")
        if tk.messagebox.askyesno("ОБМЕН", "Банк предложил бы поменять чемодан. Вы согласились бы?"):
            stage = chumodan.swap_cases
            log.write("Игрок соглашается.")
            tk.messagebox.showinfo("Выбор", "Выберите чемодан, на который хотите поменять свой")
        else:
            stage = chumodan.open_enabled



def bank_offer(ip):
    global deal_was_made, stage, swap_was_offered, winnings
    oii = offer_money(ip)
    if (len(ip)>7) or (swap_was_offered):
        if (deal_was_made is False):
            log.write("Банк предлагает "+str(oii)+'.\n')
            if tk.messagebox.askyesno("Предложение банка", "Банк предлагает "+str(oii)+". Вы согласны на сделку?"):
                deal_was_made = True
                winnings = oii
                log.write("Игрок соглашается на сделку \n")
                tk.messagebox.showinfo("Сделка!", "Вы согласились на сделку и выиграли "+str(oii)+". Но что было бы, если бы вы играли дальше?")
            else:
                log.write("Игрок отказывается от сделки \n")
                stage = chumodan.open_enabled
            if len(sums) > 4:
                tk.messagebox.showinfo("Откройте ещё чемодан",
                                       "До предложения банка осталось чемоданов: " + str(
                                           until_next_offer(len(sums))))
        else:
            log.write("Банк предложил бы " + str(oii) + '.\n')
            tk.messagebox.showinfo("Предложение банка", "Банк предложил бы " + str(oii))
            if len(sums) > 4:
                tk.messagebox.showinfo("Откройте ещё чемодан",
                                       "До предложения банка осталось чемоданов: " + str(
                                           until_next_offer(len(sums))))
        stage = chumodan.open_enabled
    else:
        master = rnd.randint(0, 99)
        if (master>=15): #10
            if (deal_was_made is False):
                log.write("Банк предлагает " + str(oii) + '.\n')
                if tk.messagebox.askyesno("Предложение банка",
                                          "Банк предлагает " + str(oii) + ". Вы согласны на сделку?"):
                    deal_was_made = True
                    winnings = oii
                    log.write("Игрок соглашается на сделку \n")
                    tk.messagebox.showinfo("Сделка!", "Вы согласились на сделку и выиграли " + str(
                        oii) + ". Но что было бы, если бы вы играли дальше?")
                else:
                    log.write("Игрок отказывается от сделки \n ")
                    stage = chumodan.open_enabled
                if len(sums) > 4:
                    tk.messagebox.showinfo("Откройте ещё чемодан",
                                           "До предложения банка осталось чемоданов: " + str(
                                               until_next_offer(len(sums))))
            else:
                log.write("Банк предложил бы " + str(oii) + '.\n')
                tk.messagebox.showinfo("Предложение банка", "Банк предложил бы " + str(oii))
                if len(sums) > 4:
                    tk.messagebox.showinfo("Откройте ещё чемодан",
                                           "До предложения банка осталось чемоданов: " + str(
                                               until_next_offer(len(sums))))
            stage = chumodan.open_enabled
        else:
            swap_was_offered = True
            offer_swap()
    pass



def place(event, t):
    global stage, winnings
    p = 400
    r = 500
    if stage==chumodan.choosing:
        canvas.coords(valizy[t], p, r, p+cases_size[0], r+cases_size[1])
        x, y, x1, y1 = canvas.coords(valizy[t])
        canvas.coords(nomera[t], (x+x1)//2, (y+y1)//2)
        stage = chumodan.open_disabled
        log.write("Игрок выбирает чемодан номер "+str(t+1)+".\n")
        cases_listofdicts[t]['own'] = True
        #print(cases_listofdicts[t]['sum']) #для отладки
        tk.messagebox.showinfo("Откройте ещё чемодан",
                               "До предложения банка осталось чемоданов: " + str(until_next_offer(len(sums))))
        stage = chumodan.open_enabled
    elif stage==chumodan.open_enabled and not (cases_listofdicts[t]['own']):
        stage = chumodan.open_disabled
        tk.messagebox.showinfo("Внимание!", "Открываем чемодан номер "+str(t+1)+"!")
        canvas.delete("case"+str(t))
        #print(sums)
        #print(cases_listofdicts[t]['sum'])
        sums_on_tableau[nat_order.index(cases_listofdicts[t]['sum'])].place_forget()
        sums.pop(sums.index(cases_listofdicts[t]['sum']))
        cases_listofdicts[t]['in_game'] = False
        tk.messagebox.showinfo("Открытие", "В чемодане было " + str(cases_listofdicts[t]['sum']))
        log.write("В чемодане номер " + str(t+1) + " было " + str(cases_listofdicts[t]['sum']) + '\n')
        if len(sums) not in bank:
            stage = chumodan.open_enabled
            if len(sums)>4:
                tk.messagebox.showinfo("Откройте ещё чемодан", "До предложения банка осталось чемоданов: "+str(until_next_offer(len(sums))))
            elif (len(sums)==1):
                stage = chumodan.open_your_own
                tk.messagebox.showinfo("Откройте свой чемодан", "В нём должно быть "+str(sums[0]))
        else:
            stage = chumodan.open_disabled
            bank_offer(sums)
    elif stage == chumodan.swap_cases:
        if not (cases_listofdicts[t]['own']):
            ashash = next((i for i, x in enumerate(cases_listofdicts) if x["own"] is True), None)
            #print(ashash)
            x, y, x1, y1 = canvas.coords(valizy[ashash])
            u, k, u1, k1 = canvas.coords(valizy[t])
            cases_listofdicts[ashash]['own'] = False
            cases_listofdicts[t]['own'] = True
            canvas.coords(valizy[ashash], u,k,u1,k1)
            canvas.coords(valizy[t], x, y, x1, y1)
            canvas.coords(nomera[ashash], (u + u1) // 2, (k + k1) // 2)
            canvas.coords(nomera[t], (x + x1) // 2, (y + y1) // 2)
            log.write("Игрок меняет чемодан номер "+str(ashash+1)+" на чемодан номер "+str(t+1)+".\n")
            stage = chumodan.open_enabled
            if len(sums)>4:
                tk.messagebox.showinfo("Откройте ещё чемодан", "До предложения банка осталось чемоданов: "+str(until_next_offer(len(sums))))
            pass #дописать
    elif stage == chumodan.open_your_own:
        if (cases_listofdicts[t]['own']):
            tk.messagebox.showinfo("У нас всё честно", "В чемодане было " + str(cases_listofdicts[t]['sum']))
            canvas.delete("case" + str(t))
            log.write("В чемодане " + str(t + 1) + " (чемодане игрока) было " + str(cases_listofdicts[t]['sum']) + '\n')
            stage = chumodan.end
            if not (deal_was_made):
                winnings = cases_listofdicts[t]['sum']
            tk.messagebox.showinfo("Поздравляем!", "Вы выиграли "+str(winnings))
            log.write("Выигрыш: "+str(winnings))






for i in range(len(cases_pos_y)):
    q = 15+cases_size[0]*(cases_pos_x[i]-1.8)
    q1 = 15+cases_size[1]*(cases_pos_y[i]-1)
    a = canvas.create_rectangle(q, q1, q+cases_size[0], q1+cases_size[1], fill = '#ffffff', outline = '#222222', tag = "case"+str(i))
    valizy.append(a)
    x, y, x1, y1 = canvas.coords(valizy[i])
    #print('Чемодан номер '+str(i+1)+': '+str(x)+' ' +str(y)+' '+str(x1)+' '+str(y1)+' ')
    f = canvas.create_text((x+x1)//2, (y+y1)//2, text=str(i+1), font=('Arial', 35), tag="case"+str(i))
    nomera.append(f)
    canvas.tag_bind("case"+str(i), "<Button-1>", lambda event, h=i: place(event, h))


log = codecs.open('log.txt', 'a', "utf_8_sig")
sums = [0.01, 0.10, 1, 5, 10, 50, 100, 500, 1000, 2500, 5000, 10000, 15000, 25000, 50000, 100000, 200000, 300000, 500000, 1000000, 1500000, 3000000]
nat_order = sums.copy()
bank = [16, 13, 10, 7, 4, 2]
c = rnd.randint(0, 1)
if (c!=0):
    bank.append(3)
bank.sort(reverse=True)

pinigai = ttk.LabelFrame(root, text = "Суммы в игре", width = 215, height=420)
pinigai.place(x=828, y = 5)
rnd.shuffle(sums)

for d in range(len(valizy)):
    e = tk.Label(pinigai, width=11, height=1)
    sums_on_tableau.append(e)
    sums_on_tableau[d]['bg'] = "#ff9f00"
    sums_on_tableau[d]['fg'] = "#000000"
    sums_on_tableau[d]["text"] = str(nat_order[d])
    sums_on_tableau[d]["justify"] = tk.CENTER
    c = len(valizy)//2
    sums_on_tableau[d].place(x=5+105*(d//c), y=5 + 35*(d % c))
    dict = {}
    dict["own"] = False
    dict["in_game"] = True
    dict["sum"] = sums[d]
    #cases_listofdicts.append(dict)
    #print(str(d+1)+': '+str(sums[d]))

#print(cases_listofdicts)
stage = chumodan.choosing
tk.messagebox.showinfo('Начните игру', 'Выберите свой чемодан')



root.protocol('WM_DELETE_WINDOW', doSomething)
root.mainloop()
