import flet as ft
import socket
import os
import time
import threading
import json

s = ""

def socket_logic(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (str(s), 10000)

    try:
        client_socket.connect(server_address)
        print('Отправляю', message)
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print('Получено', data.decode())
        return data.decode()
    finally:
        client_socket.close()

def keep_alive():
    while True:
        try:
            keep_alive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (str(s), 10000)
            keep_alive_socket.connect(server_address)
            keep_alive_socket.close()
            time.sleep(60)
        except ConnectionRefusedError:
            print("Сервер недоступен. Повторная попытка подключения через 5 секунд...")
            time.sleep(5)
        except ConnectionResetError:
            print("Сервер разорвал соединение. Повторная попытка подключения через 5 секунд...")
            time.sleep(5)

keep_alive_thread = threading.Thread(target=keep_alive)


host = socket.gethostbyname(socket.gethostname())
print(host)
host2 = os.name
print("===================")
print(host2)
msgs = ft.Column(controls=[])

def main(page: ft.Page):
    page.bgcolor = "#2C2F33"
    page.window_width = 350
    page.window_height = 600
    page.fonts = {"roboto": "https://drive.google.com/file/d/1pRdrvRxN46XaMY6ytMVoCTRtFQwJVWnZ/view?usp=drive_link"}
    page.dark_theme



    rail = ft.NavigationRail(
        bgcolor='#23272A',
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.Text("Scord", size=20),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.CHAT, label="Chat"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.MIC),
                label="Voice",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS,
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: rail_logic(e.control.selected_index),
    )
    

    tfsip = ft.TextField(label="server ip", hint_text="Введите IPv4 сервера")
    def reg(e):
        if tf.value != "" and tf1 != "":
            sd1 = socket_logic(f"/add_acc {tf.value} {tf1.value} {host}")
            com, ip, reg = sd1.split()
            if reg == "ok":            
            
                print(f"tf:{tf.value}| tf1:{tf1.value}")
                page.clean()
                page.add(ft.Row([ft.Icon(ft.icons.CHECK), ft.Text("Готово", size=36, expand=True)]))
                page.update()
                time.sleep(2)
                page.clean()
                page.window_width = 1920
                page.window_height = 1080
                page.add(
                ft.Row(
                    [
                        rail
                    ],
                    expand=True,
                    )
                )
        else:
            t = ft.Text("Нужно ввести данные!", size=30)
            page.add(t)
            page.update()
            time.sleep(3)
            page.remove(t)
    
    tf = ft.TextField(label="nickname", hint_text="Ваш никнейм, можно изменить")
    tf1 = ft.TextField(label="password", hint_text="Ваш пароль, можно изменить")
    tfb = ft.ElevatedButton(text="Зарегистрироваться", on_click=reg)
    
    def server_ip_change(e):
        if tf2.value == "":
            page.add(ft.Text("Нужно заполнить поле!"))
        else:
            global s 
            s = tf2.value
            keep_alive_thread.start()
            page.clean()
            sd = socket_logic(f"/check {host}")
            com, ip, check = sd.split()
            if check != "ok":
                page.clean()
                page.add(ft.Column([tf, tf1, tfb], expand=True, alignment="center"))
    
            else:
                page.window_width = 1920
                page.window_height = 1080
                page.add(
                    ft.Row(
                    [
                        rail
                    ],
                    expand=True,
                    )       
                )

    tf2 = ft.TextField(label="server ip", value="")
    btn_tf2 = ft.ElevatedButton("Готово", on_click=server_ip_change)
    page.add(ft.Column([ft.Text("Введите IP"), tf2, btn_tf2]))
    page.update()
       

    def add_msg_to_msgs(v):
        r = socket_logic(f"/text-=S=-{host}-=S=-{tf_ch.value}")
        if r.startswith("/text"):
            com, f_t = r.split("-=S=-")
            msgs.controls.append(ft.Text(f_t, size=20, font_family="roboto"))
            tf_ch.value = ""
        page.update()

    sd2 = socket_logic(f"/get_settings {host}")
    com, nick, desc = sd2.split(":")
    desc_card = ft.TextField(label="описание", value=desc)
    card = ft.Card(color="#23272A", content=ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.icons.ACCOUNT_BOX, scale=1.6), title=ft.Text(nick), subtitle=ft.Text(desc))], alignment=ft.MainAxisAlignment.CENTER)))
    tf_ch = ft.TextField(hint_text="Enter your messge: ", on_submit=add_msg_to_msgs)

    def settings_logic_btn(e):
        sd3 = socket_logic(f"/set:{host}:desc:{desc_card.value}")

        page.clean()
        page.controls.append(
            ft.Row([
                rail,
                ft.Column([
                    card,
                    ft.Divider(height=4, thickness=2),
                    desc_card,
                    ft.Row([ft.ElevatedButton("Применить", on_click=settings_logic_btn), ft.Text("Перезайдите в настройки")])
                ],
                expand=True, alignment="top_center", spacing=20)
            ], expand=True)
        )
        page.update()

    message_list = []

    def get_mesgs():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = "192.168.1.47"
        server_address = (str(s), 10000)
        client_socket.sendto(f"/getmsgs:{host}".encode(), server_address)
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode().rstrip('-=S=-')
            message_list.append(message)



    def rail_logic(index):
        if index == 0:
            #get_mesgs()
            #for i in message_list:
                #msgs.controls.append(ft.Text(str(i)))
                #print(i)
            r = socket_logic(f"/getmsgs:{host}")
            key = json.loads(r)
            for i in key:
                msgs.controls.append(ft.Text(i, size=20))
            page.clean()
            page.add(ft.Row([
                rail,
                ft.Column([ft.Column([msgs], expand=True, scroll=True, alignment=ft.MainAxisAlignment.END), tf_ch], expand=True, alignment="end"),                
                users_chat_ov
            ], expand=True))
            page.update()

        elif index == 1:
            page.clean()
            # ТУТ НАДА СДЕЛАТЬ ПОКАЗ ЛЮДЕЙ В ВОЙСЕ
            page.add(ft.Row([rail], expand=True))
            page.update()
            
        elif index == 2:
            page.update()
            page.clean()
            page.controls.append(
                ft.Row([
                    rail,
                    ft.Column([
                        card,
                        ft.Divider(height=4, thickness=2),
                        desc_card,
                        ft.ElevatedButton("Применить", on_click=settings_logic_btn)
                        #ТУТА НАДА СДЕЛАТЬ ПРАВИЛА, ГИТХАББ ВЕРСИЮ SCORD И СМЕНУ ПАРОЛЯ
                             
                    ],
                    expand=True, alignment="top_center", spacing=20)
                ], expand=True)
            )
            page.update()

    

    
    users_chat_ov = ft.NavigationRail(
        bgcolor='#23272A',
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.Text("members", size=20),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ACCOUNT_BOX),
                label="sapph1ren",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ACCOUNT_BOX),
                label="StasiKuz",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ACCOUNT_BOX),
                label="Адыгей",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ACCOUNT_BOX),
                label="nigrilla",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ACCOUNT_BOX),
                label="egorka hund",
            ),

        ],
    )
    while True:
        page.update()
        time.sleep(5)

ft.app(main)

