import datetime
from playwright.sync_api import (
    Playwright,
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
import os


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        executable_path="/usr/bin/chromium",
        args=["--disable-gpu", "--headless", "--no-sandbox"],
        headless=True,
        channel="chrome",
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080},
        geolocation={"latitude": 4.60971, "longitude": -74.08175},
        permissions=["geolocation"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        bypass_csp=True,
    )
    page = context.new_page()
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
    page.locator("div").filter(has_text="9:").nth(3).click()
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
    month_day_number = datetime.datetime.now().day + 1
    weekday_number = datetime.datetime.now().weekday() + 1
    return month_day_number, es_weekday_first_three_letters[weekday_number]


def try_to_find_court(page, retries=4):
    try:
        page.get_by_text(f"Cancha {retries}").click(timeout=1500)
    except PlaywrightTimeoutError:
        if retries > 1:
            try_to_find_court(page, retries - 1)
        else:
            raise Exception("Court not found")


with sync_playwright() as playwright:
    run(playwright)
