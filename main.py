import flet as ft
from assistant import ChatGPT 

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class chatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True, width=500),
                ],
                tight=True,
                spacing=5 
            )
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()
    
    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER, ft.colors.BLUE, ft.colors.BLUE_100, ft.colors.BLACK,
            ft.colors.GREEN_100, ft.colors.GREEN_700, ft.colors.PINK_200,
            ft.colors.PINK_800, ft.colors.GREY, ft.colors.RED_300,
            ft.colors.RED_700, ft.colors.BROWN, ft.colors.PURPLE
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def main(page: ft.Page):
    page.title = "ChatGPT AI"
    page.theme_mode = "light"
    page.fonts = {
        "organical": "fonts/organical.ttf"
    }

    # Initialize ChatGPT
    Chatgpt = ChatGPT()

    def join_chat_click(e):
        if not join_user_name.value: 
            join_user_name.error_text = "Let us first know your name!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False 
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat!", message_type="login_message"))
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            user_message = new_message.value
            page.pubsub.send_all(Message(page.session.get("user_name"), user_message, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

            # Send message to ChatGPT and get response
            try:
                ai_response = Chatgpt.ChatGPTResponse(user_text=user_message)
                page.pubsub.send_all(Message("ChatGPT", ai_response, message_type="chat_message"))
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                page.pubsub.send_all(Message("System", error_message, message_type="chat_message"))
            finally:
                page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = chatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)

        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    join_user_name = ft.TextField(
        label="Tell us your Name: ",
        autofocus=True,
        on_submit=join_chat_click
    )

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join Chat", on_click=join_chat_click)]
    )

    # chat messages 
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    # new user message 
    new_message = ft.TextField(
        hint_text="Message",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=10,
        filled=True,
        expand=True, 
        border_radius=20,
        on_submit=send_message_click,
        border_color=ft.colors.BLACK
    )

    page.add(
        ft.Row([ft.Text("ChatGPT AI", font_family="organical", style="headLineLarge", color='black')], alignment="center"),
        ft.Container(
            content=chat, 
            border=ft.border.all(2, ft.colors.BLACK),
            border_radius=20,
            padding=10,
            expand=True 
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="send message",
                    on_click=send_message_click,
                    icon_color=ft.colors.BLACK,
                )
            ]
        )
    )

ft.app(target=main, assets_dir="assets")
