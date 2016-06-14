# automated-testing-notes

> Все используют пэдж обжекты, чтобы прятать локаторы. А на самом деле задача пэдж обжектов - инкапсулировать не нахождение элементов, а логику работы с этими элементами.

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

<a name="fn1">1</a>: [Логирование и декораторы в python](http://poliarush.com/working/development/logging-and-decorators-in-python.html)
