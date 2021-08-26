def test_duckduckgo(driver):
    driver.get("https://duckduckgo.com")
    assert "DuckDuckGo" in driver.title


def test_mail(driver):
    driver.get("https://mail.ru")
    assert "Mail.ru" in driver.title
