import flet as ft
import webbrowser

def main(page: ft.Page):
    page.title = "Калькулятор"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK  # По умолчанию темная тема
    page.bgcolor = ft.colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE
    page.padding = 20

    # Поле для отображения результата
    result = ft.TextField(
        value="0",
        text_align=ft.TextAlign.RIGHT,
        width=400,
        height=100,
        read_only=True,
        bgcolor=ft.colors.BLACK12 if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE24,
        color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK,
        border_radius=15,
        text_size=40,
    )

    # Функция для обработки нажатий на кнопки
    def button_click(e):
        current_value = result.value
        button_text = e.control.content.value  # Получаем текст из Text внутри Container

        if current_value == "0":
            result.value = button_text
        else:
            result.value += button_text

        page.update()

    # Функция для вычисления результата
    def calculate(e):
        try:
            result.value = str(eval(result.value))
        except Exception as ex:
            result.value = "Ошибка"
        page.update()

    # Функция для очистки поля
    def clear(e):
        result.value = "0"
        page.update()

    # Функция для удаления последнего символа
    def backspace(e):
        result.value = result.value[:-1] if result.value != "0" else "0"
        page.update()

    # Функция для смены темы
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.bgcolor = ft.colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE
        result.bgcolor = ft.colors.BLACK12 if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE24
        result.color = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK
        logo.color = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK
        theme_button.icon_color = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK
        page.update()

    # Функция для открытия ссылки на Telegram-канал
    def open_telegram(e):
        webbrowser.open("https://t.me/#")  # Ваш Telegram-канал

    # Функция для создания стилизованной кнопки
    def create_button(text, on_click, width=80, height=80, bgcolor=None, color=None):
        if bgcolor is None:
            bgcolor = ft.colors.BLUE_GREY if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLUE_GREY_200
        if color is None:
            color = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK

        return ft.Container(
            content=ft.Text(text, size=24, color=color),
            width=width,
            height=height,
            alignment=ft.alignment.center,
            bgcolor=bgcolor,
            border_radius=15,
            on_click=on_click,
            animate=ft.animation.Animation(300, "easeInOut"),
            on_hover=lambda e: setattr(e.control, "bgcolor", ft.colors.BLUE_GREY_700 if e.data == "true" else bgcolor),
            padding=ft.padding.all(10),
            margin=ft.margin.all(5),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=5,
                color=ft.colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY,
                offset=ft.Offset(2, 2),
            ),
        )

    # Создаем кнопки
    buttons = [
        ["C", "←", "/", "*"],
        ["7", "8", "9", "-"],
        ["4", "5", "6", "+"],
        ["1", "2", "3", "="],  # Кнопка "=" справа от "3"
        ["0", ".", "="],  # Убираем дублирующую кнопку "="
    ]

    # Добавляем кнопки на страницу
    for row in buttons:
        row_controls = []
        for button_text in row:
            if button_text == "C":
                button = create_button(button_text, clear, bgcolor=ft.colors.RED)
            elif button_text == "←":
                button = create_button(button_text, backspace, bgcolor=ft.colors.ORANGE)
            elif button_text == "=":
                if row.index(button_text) == 3:  # Кнопка "=" только в четвертом ряду
                    button = create_button(button_text, calculate, bgcolor=ft.colors.GREEN)
                else:
                    continue  # Пропускаем дублирующую кнопку "="
            elif button_text in ["/", "*", "-", "+"]:  # Кнопки операций
                button = create_button(button_text, button_click, bgcolor=ft.colors.BLUE)
            else:
                button = create_button(button_text, button_click)
            row_controls.append(button)
        page.add(ft.Row(controls=row_controls, alignment=ft.MainAxisAlignment.CENTER))

    # Логотип и название
    logo = ft.Text("Калькулятор", size=32, color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK)

    # Кнопка для смены темы
    theme_button = ft.IconButton(
        icon=ft.icons.BRIGHTNESS_4,
        on_click=toggle_theme,
        icon_color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK,
    )

    # Кнопка "О нас"
    about_button = ft.ElevatedButton(
        text="О нас",
        icon=ft.icons.INFO,
        on_click=open_telegram,
        bgcolor=ft.colors.RED,
        color=ft.colors.BLACK,
    )

    # Добавляем логотип, кнопку смены темы и кнопку "О нас"
    page.add(ft.Row(controls=[logo, theme_button, about_button], alignment=ft.MainAxisAlignment.CENTER))

    # Добавляем поле результата на страницу
    page.add(result)

# Запуск приложения
ft.app(target=main)