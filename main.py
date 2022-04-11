import datetime as dt


class Record:
    # Рекомендую использовать нотацию типов. docs https://docs.python.org/3/library/typing.html
    #  рекомендация для всех методов классов.
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Само условие лучше прописывать явно, длиннее, но читаемость будет выше
        #  if number == some_data:
        #     ....
        #  else:
        #    ....
        #
        self.date = (
            dt.datetime.now().date() if not date
            # используемый формат лучше вынести в отдельную переменную/константу, если ожидается только один формат
            else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Нейминг переменный в python используется с нижнего регистра.
        #  docs https://peps.python.org/pep-0008/#naming-conventions
        #  Важным моментом здесь является наличие у тебя класса Record в файле- использование того же нейминга
        #   зачастую приводит к конфликтам в коде, это правило касается также встроенных переменных в Python.
        for Record in self.records:
            # текущую дату dt.datetime.now().date() лучше вынести до цикла, поместить в отдельную переменную -
            #  ее нет необходимости вычислять каждый раз заново по каждой записи record
            if Record.date == dt.datetime.now().date():
                # здесь можно использовать синтаксический сахар today_stats += record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # повторяющееся today - record.date вынести в отдульную перменную, обозначающее действие.
            #  повторение в коде загромождает сам код, кроме того одно и то же вычисление отнимает вычислительные
            #  ресурсы. само условие if лучше прописывать в одну строку, чтобы было легко читать

            if (
                    (today - record.date).days < 7 and
                    (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Описание к функциям пишется в докстрингах. Комментарии загромождают код.
    #  docs https://peps.python.org/pep-0257/#what-is-a-docstring
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Переменные необходимо называть кратко и емко, избегать однобуквенных названий, чтобы было понятно,
        #  что в себе содержит эта переменна по названию.
        x = self.limit - self.get_today_stats()
        if x > 0:
            # f-строки прописываются только на строке, где нужно вставлять аргументы. В первой строке это не нужно
            #  делать. Не рекомендуется использовать слеши для переноса. длинные строки можно заключать в ()
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # здесь лишнее использование скобок
            return ('Хватит есть!')


class CashCalculator(Calculator):
    # нет необходимости переводить целое число в число с плавающей точкой. наглядней будет сразу прописать число
    #  в нужно формате 60.00
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # аргументы класса вызываются через точечную нотацию self.USD_RATE, не нужно их передавать в метод класса
    #  они уже определены в экземпляре класса.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()

        # if можно заменить на более удобный способ хранения данных- словарь, например, чтобы видеть структуру
        #  данных и не раздувать elif в случае появления новой валюты.
        #  не учтен случай, если передается валюта, которой нет в калькуляторе.
        if currency == 'usd':
            # имеет место повторяемый код с делением. Весь повторяемый код стоит вынести в функцию/метод класса
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Все константы по валютам хранятся в классе, хорошим моментом будет положить рубли также в
            #  переменную класса
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # f- string не должны содержать вычислений. Стоит вынести вычисления отдельно
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # по переносу с бекслешами комментарий дал выше. Лучше заключать все в ()
            #  стоит использовать однотипные решения в коде- или f- строки или format
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Если родительский метод не нужно переопределять, его не нужно прописывать в дочернем классе, он
    #  уже будет иметь родительское поведение
    def get_week_stats(self):
        super().get_week_stats()
