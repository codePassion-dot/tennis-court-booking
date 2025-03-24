import datetime
from playwright.sync_api import (
    Playwright,
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
import os


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        headless=True,
    )
    context = browser.new_context(
        geolocation={"latitude": 4.60971, "longitude": -74.08175},
        permissions=["geolocation"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )
    page = context.new_page()
    page.goto("https://www.easycancha.com/profile/countries")
    page.get_by_role("link", name="Colombia").click()
    page.get_by_role("button", name="Ok").click()
    page.goto("https://www.easycancha.com/login")
    page.get_by_role("textbox", name="Email").click()
    email = os.getenv("EMAIL", "")
    password = os.getenv("PASSWORD", "")
    print(f"Email: {email}, Password: {password}")
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
    page.get_by_role("heading", name="¡ Juan Jacobo Tu reserva ya").click()
    # ---------------------
    context.close()
    browser.close()


def get_date_and_weekday():
    es_weekday_first_three_letters = {
        0: "lun",
        1: "mar",
        2: "mié",
        3: "jue",
        4: "vie",
        5: "sáb",
        6: "dom",
    }
    month_day_number = (datetime.datetime.now().day + 1) % 31
    weekday_number = (datetime.datetime.now().weekday() + 1) % 7
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
