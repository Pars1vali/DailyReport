class GroupTopic:
    def __init__(self, topics: list):
        self.topics = topics


class PlanFactValue:
    def __init__(self, plan, fact):
        self.plan = plan
        self.fact = fact


class CreditValue:
    def __init__(self, loan_apply, approved, issued):
        self.loan_apply = loan_apply
        self.approved = approved
        self.issued = issued


class TopicValue:
    def __init__(self, number=0, plan_fact: PlanFactValue = None, credit: CreditValue = None):
        self.number = number
        self.plan_fact = plan_fact
        self.credit = credit


class Topic:
    def __init__(self, text: str, unit, is_credit: bool = False, have_plan: bool = False,
                 value: TopicValue = TopicValue):
        self.text = text
        self.unit = unit
        self.is_credit = is_credit
        self.have_plan = have_plan
        self.value = value


group_topics = list([
    GroupTopic([
        Topic("Сим Мегафон+Yota, шт", 0),
        Topic("Мегасемья", 0)
    ]),
    GroupTopic([
        Topic("Абонементы мегафон +ета", 0, have_plan=True),
        Topic("Доля абонементов от сим", 0.0)
    ]),
    GroupTopic([
        Topic("РК REALME(модели по акции)", 0),
        Topic("РК HONOR(модели по акции)", 0),
        Topic("Первая цена", 0),
        Topic("Хуавей", 0),
        Topic("Apple", 0)
    ]),
    GroupTopic([
        Topic("Аксесуары", 0.0),
        Topic("Акция 1+1", 0.0)
    ]),
    GroupTopic([
        Topic("ФУ", 0.0),
        Topic("Плотер", 0),
        Topic("Страховки", 0.0),
    ]),
    GroupTopic([
        Topic("КД шт", 0, is_credit=True),
        Topic("БК шт", 0, is_credit=True)
    ]),
    GroupTopic([
        Topic("Адаптер", 0)
    ]),
    GroupTopic([
        Topic("NPS 9/10 факт за день", 0)
    ])
])

opio_list = list([
    "Став 189",
    "Став 141",
    "Став/Веш",
    "Лента",
    "Оз",
    "Мачуги",
    "Игнатова",
    "Сормовская",
    "Тюляева",
    "Новомих",
    "Гулькевичи",
    "Туапсе Маркса",
    "Туапсе Жукова",
    "Кропоткин 226",
    "Кропоткин 72",
    "Усть-Лабинск Ленина",
    "Усть-Лабинск Ободовского"
])
