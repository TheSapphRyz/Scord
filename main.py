import flet as ft
import socket
import os
import time
import threading
import json

s = "10.2.0.2"

def socket_logic(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (str(s), 10000)

    try:
        client_socket.connect(server_address)
        print('Отправляю', message)
        client_socket.sendall(message.encode('UTF-8'))
        data = client_socket.recv(1024)
        print('Получено', data.decode('UTF-8'))
        return data.decode()
    finally:
        client_socket.close()

host = socket.gethostbyname(socket.gethostname())
print(host)
host2 = os.name
host3 = socket.gethostname()
print("===================")
print(host3)
print("===================")
print(host2)
msgs = ft.Column(controls=[])
client_name = "sapph1ren"
client_password = "1201"


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
    # ТУТ ДОБАВЛЯЕТСЯ НА ЭКРАН ГЛАВНАЯ СТРАНИЦА ТО ЕСТЬ ПЕРЕД ЭТИМ НАДА СДЕЛАТЬ sing up/in И ВЫБОР СЕРВЕРА
    page.add(ft.Row([rail], expand=True))

    def add_msg(e):
        r = socket_logic(f"/text-=S=-{client_name}-=S=-{tf.value}")

        msgs.controls.append(ft.Text(f"{client_name}: {tf.value}", size=20, font_family="roboto"))
        tf.value = ""
        page.update()

    tf = ft.TextField(label="enter your message", on_submit=add_msg)
    
    def rail_logic(index):

        if index == 0:
            print(index)
            r = socket_logic(f"/getmsgs:{client_name}")
            key = json.loads(r)
            for i in key:
                print(i)
                msgs.controls.append(ft.Text(i, size=20))
            page.clean()
            page.add(ft.Row([
                rail,
                ft.Column([ft.Column([msgs], expand=True, scroll=True, alignment=ft.MainAxisAlignment.START), tf], expand=True, alignment=ft.MainAxisAlignment.END),                
            ], expand=True))
            page.update()

        elif index == 1:
            page.clean()
            # ТУТ НАДА СДЕЛАТЬ ПОКАЗ ЛЮДЕЙ В ВОЙСЕ
            page.add(ft.Row([
                rail

            ], expand=True))
            page.update()
            
        elif index == 2:

            sd2 = socket_logic(f"/get_settings-=S=-{client_name}")
            com, nick, desc = sd2.split("-=S=-")
            desc_card = ft.TextField(label="описание", value=desc, expand=False)
            card = ft.Card(color="#23272A", content=ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.icons.ACCOUNT_BOX, scale=1.6), title=ft.Text(nick), subtitle=ft.Text(desc))], expand=False, alignment=ft.MainAxisAlignment.CENTER)))
            page.update()
            page.clean()
            page.controls.append(
                ft.Row([
                    rail,
                    ft.Column([
                        card,
                        ft.Divider(height=4, thickness=2),
                        desc_card,
                        ft.ElevatedButton("Применить", on_click=lambda e: rail_logic(2))
                        #ТУТА НАДА СДЕЛАТЬ ПРАВИЛА, ГИТХАББ ВЕРСИЮ SCORD И СМЕНУ ПАРОЛЯ
                             
                    ], alignment="top_center", spacing=20)
                ], expand=True)
            )
            page.update()

ft.app(main)
