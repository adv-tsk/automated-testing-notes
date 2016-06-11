# automated-testing-notes

## Practices

### Worst practice

1. Частая инициализация вебдрайвера
2. Передача вебдрайвера каждому ПейджОбжекту в самый конструктор
3. Лишняя инициализация каждого виджета/элемента

### Best practice

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
