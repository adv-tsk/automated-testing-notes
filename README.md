# automated-testing-notes

PageObject'ы используют
* и чтобы прятать локаторы: давать им красивые имена и нормальную поддержу рефакторинга
* и чтобы инкапсулировать логику работы с этими элементами
* а также чтобы упростить совместную работы команды


## Practices

### Worst practice

1. Частая инициализация вебдрайвера
2. Передача вебдрайвера каждому ПейджОбжекту в самый конструктор
3. Лишняя инициализация каждого виджета/элемента

### Best practice

1. PageObject отвечает только за действия над страницей, которую он описывает. Т.е. на странице нового пользователя, есть методы FillForm и Save, но не вкоем случае не (CreateUser()). В некоторых ситуациях, Педжобжект может взаимодействовать с другими Пейджобжектами и с Бизнес-шагами. Но, делается это на уровне абстракций и API. Пейджобжекты не взаимодействуют с базой данных или веб-элементами других страниц напрямую.
2. Вебдрайвер и ожидания не должны быть в PO.
3. Все методы касающиеся элементов должны находиться в своем классе.
4. Все методы по ожиданиям должны находится в своем классе.
5. Инициализацию драйвера надо делать исключительно за пределами тестов и объектов страниц или компонентов, но при этом делать это так, чтобы этот самый драйвер можно было использовать не только в PO, но и в других классах.

## Логирование

Пример того, как можно автоматически логировать вызываемые методы <sup>[1](#fn1)</sup>.

```python
import logging
from functools import wraps

def method_decorator(func):
    @wraps(func)
    def wrapper(self, *argv, **kwargv):
        logging.basicConfig(filename='myapp.log', 
            level=logging.INFO, format='%(message)s')
        logging.info("\t- %s" % func.__doc__)
        return func(self, *argv, **kwargv)
    return wrapper
 
def class_decorator(cls):
    for name, method in cls.__dict__.iteritems():
        if not name.startswith('_'):
            setattr(cls, name, method_decorator(method))
    return cls
```

## Скриншоты при падении тестов

### Первый вариант

```python
def pytest_exception_interact(node, call, report):
    driver = node.instance.driver
    # ...
    allure.attach(
        name='Скриншот',
        contents=driver.get_screenshot_as_png(),
        type=allure.constants.AttachmentType.PNG,
    )
    # ...
```

### Второй вариант

```python
import unittest
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener

class ScreenshotListener(AbstractEventListener):
    def on_exception(self, exception, driver):
        screenshot_name = "exception.png"
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)

class TestDemo(unittest.TestCase):
    def test_demo(self):

        pjsdriver = webdriver.PhantomJS("phantomjs")
        d = EventFiringWebDriver(pjsdriver, ScreenshotListener())

        d.get("http://www.google.com")
        d.find_element_by_css_selector("div.that-does-not-exist")
```

<a name="fn1">1</a>: [Логирование и декораторы в python](http://poliarush.com/working/development/logging-and-decorators-in-python.html)
