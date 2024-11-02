import flet as ft
import socket
import os
import time
import threading
import json

def socket_logic(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (str(s), 10000)

    try:
        client_socket.connect(server_address)
        print('Отправляю', message)
        client_socket.sendall(message.encode('UTF-8'))
        data = client_socket.recv(1024)
        print('Получено', data.decode('UTF-8'))
        return data.decode('UTF-8')
    finally:
        client_socket.close()

host = socket.gethostbyname(socket.gethostname())
print(host)
host3 = socket.gethostname()
print("===================")
print(host3)
msgs = ft.Column(controls=[])
s = "0.0.0.0"
client_name = f"{host3}"
client_password = f"{s}"
release = "alfa 0.1"

async def main(page: ft.Page):
    page.bgcolor = "#2C2F33"
    page.window_width = 1920
    page.window_height = 1080
    page.fonts = {"roboto": "https://drive.google.com/file/d/1pRdrvRxN46XaMY6ytMVoCTRtFQwJVWnZ/view?usp=drive_link"}
    page.dark_theme

    rail = ft.NavigationRail(
        bgcolor='#23272A',
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.Text("Scord", size=20, font_family='roboto'),
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
    # ТУТ ДОБАВЛЯЕТСЯ НА ЭКРАН ГЛАВНАЯ СТРАНИЦА ТО ЕСТЬ ПЕРЕД ЭТИМ НАДА СДЕЛАТЬ sing up/in И ВЫБОР СЕРВЕРА
    def server_connect(e):
        print("server_connect")
        if tf_server.value == "":
            pass
        else:
            global s
            s = tf_server.value
            r = socket_logic("/c")
            if r == "ok":
                page.clean()
                page.add(ft.ProgressRing())
                time.sleep(0.8)
                page.clean()
                r = socket_logic(f"/acc_log_or_reg-=S=-{host3}")
                if r == "ok":
                    page.add(ft.Column([
                        ft.Text("login", size=25, font_family="roboto"),
                        tf_login_name,
                        tf_login_password,
                        btn_login
                    ]))
                    page.update()
                    tf_login_name.focus()
                else:
                    page.add(ft.Column([
                        ft.Text("register", size=25, font_family="roboto"),
                        tf_login_name,
                        tf_login_password,
                        btn_register
                    ]))
                    page.update()
                    tf_login_name.focus()

    def login_acc(e):
        r = socket_logic(f"/check-=S=-{tf_login_name.value}-=S=-{tf_login_password.value}-=S=-{host3}")
        if r == "ok":
            page.clean()
            page.window_width = 1920
            page.window_height = 1080
            page.add(ft.Row([rail], expand=True))
            page.update()
            global client_name 
            global client_password
            client_name = tf_login_name.value
            client_password = tf_login_password.value
        else:
            ft_neverno = ft.Text("Неверно")
            page.add(ft_neverno)
            time.sleep(3)
            page.remove(ft_neverno)

    def register_acc(e):
        r = socket_logic(f"/add_acc-=S=-{tf_login_name.value}-=S=-{tf_login_password.value}-=S=-{host}-=S=-{host3}")
        if r == "ok":
            page.clean()
            page.window_width = 1920
            page.window_height = 1080
            page.add(ft.Row([rail], expand=True))
            page.update()
            global client_name 
            global client_password
            client_name = tf_login_name.value
            client_password = tf_login_password.value
        else:
            ft_oshibka = ft.Text("Ошибка")
            page.add(ft_oshibka)
            time.sleep(3)
            page.remove(ft_oshibka)

    tf_login_name = ft.TextField(label="your username")
    tf_login_password = ft.TextField(label="your password")
    btn_login = ft.ElevatedButton("login", on_click=login_acc)
    btn_register = ft.ElevatedButton("register", on_click=register_acc)

    tf_server = ft.TextField(label="Введите IPv4 сервера", on_submit=server_connect)
    btn_server = ft.ElevatedButton("Подключиться", on_click=server_connect)
    
    page.window_width = 350
    page.window_height = 600
    page.add(ft.Column([
        ft.Text("official servers", size=20, font_family="roboto"),
        ft.Card(color="#23272A", content=ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.icons.NETWORK_WIFI_1_BAR, scale=1.6), title=ft.Text("Sanya's server", font_family="roboto"), subtitle=ft.Text("В разработке"))]))),
        ft.Text("community servers", size=20, font_family="roboto"),
        tf_server,
        btn_server
    ]))
    tf_server.focus()

    def add_msg(e):
        r = socket_logic(f"/text-=S=-{client_name}-=S=-{tf.value}")

        msgs.controls.append(ft.Text(f"{client_name}: {tf.value}", size=20, font_family="roboto"))
        tf.value = ""
        page.update()
        tf.focus()

    tf = ft.TextField(label="enter your message", on_submit=add_msg)

    def rail_logic(index):
        card = ft.Card(color="#23272A", content=ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.icons.ACCOUNT_BOX, scale=1.6), title=ft.Text(client_name), subtitle=ft.Text("Scord user"), title_alignment="center")], alignment=ft.MainAxisAlignment.CENTER)))
        page.update()
        if index == 0:
            print(index)
            r = socket_logic(f"/getmsgs:{client_name}")
            print(r)
            key = json.loads(r)
            for i in key:
                print(i)
                msgs.controls.append(ft.Text(i, size=20))
            page.clean()
            page.add(ft.Row([
                rail,
                ft.Column([ft.Column([msgs], expand=True, scroll=True, alignment=ft.MainAxisAlignment.START), tf], expand=True, alignment=ft.MainAxisAlignment.END),                
            ], expand=True))
            tf.focus()
            page.update()

        elif index == 1:
            page.clean()
            # ТУТ НАДА СДЕЛАТЬ ПОКАЗ ЛЮДЕЙ В ВОЙСЕ
            page.add(ft.Row([
                rail

            ], expand=True))
            page.update()
            
        elif index == 2:
            page.update()
            page.clean()
            page.controls.append(
                ft.Row([
                    rail,
                    ft.Column([
                        card,
                        ft.Divider(color="#23272A"),
                        ft.Row([ft.Text("Github проекта:", font_family="roboto"), ft.IconButton(icon=ft.icons.SOURCE, url="https://github.com/TheSapphRyz/Scord", selected_icon_color='#7289da')]),
                        ft.Row([ft.Text("Community сервер на Github:", font_family="roboto"), ft.IconButton(icon=ft.icons.SOURCE, url="https://github.com/TheSapphRyz/Scord_server", selected_icon_color='#7289da')])
                        #ТУТА НАДА СДЕЛАТЬ ПРАВИЛА, ГИТХАББ ВЕРСИЮ SCORD И СМЕНУ ПАРОЛЯ

                             
                    ], expand=True, alignment="top_center", spacing=20)
                ], expand=True)
            )
            page.update()
    


ft.app(main)
