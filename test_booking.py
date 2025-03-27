import datetime
from playwright.sync_api import (
    Playwright,
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
import os
import calendar


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            "--disable-gpu",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--headless",
        ],
        channel="chrome",
    )
    context = browser.new_context(
        geolocation={"latitude": 4.60971, "longitude": -74.08175},
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080},
        bypass_csp=True,
        permissions=["geolocation"],
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    )
    context.clear_cookies()
    page = context.new_page()
    page.route("**", lambda route: route.continue_())
    page.goto("https://www.easycancha.com/profile/countries")
    page.get_by_role("link", name="Colombia").click()
    page.get_by_role("button", name="Ok").click()
    page.goto("https://www.easycancha.com/login")
    page.get_by_role("textbox", name="Email").click()
    email = os.getenv("EMAIL", "")
    password = os.getenv("PASSWORD", "")
    page.get_by_role("textbox", name="Email").fill(email)
    page.get_by_role("textbox", name="Clave").click()
    page.get_by_role("textbox", name="Clave").fill(password)
    page.get_by_role("button", name="Ingresar").click()
    page.locator("#book-views div").filter(has_text="Deportes Clubes").locator(
        "div"
    ).nth(3).click()
    page.get_by_role("textbox", name="Buscar").click()
    page.get_by_role("textbox", name="Buscar").fill("bosque")
    page.locator("#club-497").get_by_text("RESERVA AQUI").click()
    date, weekday = get_date_and_weekday()
    page.get_by_text(f"{date} {weekday}.").click()
    page.get_by_text("60 min.").click()
    time = "9:"
    if weekday == "sáb" or weekday == "dom":
        time = "10:"
    custom_time = os.getenv("TIME")
    if custom_time is not None and int(custom_time) >= 6 and int(custom_time) <= 21:
        time = f"{custom_time}:"
    page.locator("div").filter(has_text=time).nth(3).click()
    page.get_by_role("link", name="Siguiente").click()
    try_to_find_court(page)
    page.get_by_role("button", name="Agregar / Quitar jugadores").click()
    page.get_by_text("Mariana Jaramillo").click()
    page.get_by_role("button", name="Seleccionar").click()
    page.get_by_role("button", name="Reservar").click()
    page.wait_for_url("**/summary/*")
    page.get_by_role("heading", name="¡ Juan Jacobo Tu reserva ya").click()
    # ---------------------
    context.close()
    browser.close()


def get_date_and_weekday():
    es_weekday_first_three_letters = [
        "lun",
        "mar",
        "mié",
        "jue",
        "vie",
        "sáb",
        "dom",
    ]
    date = datetime.datetime.now()
    days_in_month = calendar.monthrange(date.year, date.month)[1] + 1
    month_day_number = (date.day + 1) % days_in_month
    weekday_number = (date.weekday() + 1) % 7
    return month_day_number, es_weekday_first_three_letters[weekday_number]


def try_to_find_court(page):
    mappings = {
        1: 4,
        2: 1,
        3: 2,
        4: 3,
    }
    for i in range(1, 5):
        try:
            page.get_by_text(f"Cancha {mappings[i]}").click(timeout=1500)
            break
        except PlaywrightTimeoutError:
            continue


with sync_playwright() as playwright:
    run(playwright)
