from django.shortcuts import render
from django.http import HttpResponse

components = [{'id': 1, 'title': 'Процессорный узел бортового компьютера Xiphos Q7S', 'shortDescription': 'Решение для управления и передачи данных.', 'description': 'Q7S, доступный через AAC SpaceQuest, является новейшим представителем семейства Xiphos Q-Card — недорогих встраиваемых узлов для управления, обработки данных и интерфейсов. Это решение для управления и обработки данных было разработано для поддержки коммерческих проектов с ограниченным бюджетом, которым требуются надёжные и качественные решения. Благодаря небольшому размеру, малой массе и энергопотреблению решения Q7 идеально подходят для аэрокосмической отрасли.', 'price': '2000000₽','imgSrc': 'http://127.0.0.1:9000/lab1/1.png'},
            {'id': 2, 'title': 'Аккумулятор CubeSat AAC Clyde Space OPTIMUS', 'shortDescription': 'Один из лучших аккумуляторов космических аппаратов.', 'description': 'Батареи CubeSat серии AAC Clyde Space OPTIMUS являются одними из самых часто используемых в космических аппаратах за всю историю. Тысячи таких батарей были отправлены в миссии по всему миру, и сотни из них находятся на орбите. Наша батарея обладает непревзойденными характеристиками на орбите. Наши батареи также оснащены встроенными функциями, такими как термостатируемые нагреватели и датчики. Сочетание параллельного подключения ячеек с электроникой защиты ячеек означает, что наши аккумуляторы CubeSat надёжны, устойчивы к внешним воздействиям и обладают внутренней избыточностью. Кроме того, использование защищённых параллельных цепочек позволяет нам легко и безопасно масштабировать аккумулятор в соответствии с различными требованиями к миссии.', 'price': '900000₽','imgSrc': 'http://127.0.0.1:9000/lab1/2.jpg'},
            {'id': 3, 'title': 'Блок управления и распределения мощности STARBUCK-NANO', 'shortDescription': 'Надёжная и безотказная система питания.', 'description': 'Благодаря своей универсальной конструкции и беспрецедентному опыту работы на орбите мы гордимся стабильным высоким качеством наших подсистем, в том числе CubeSat EPS (системы электропитания). Линейка STARBUCK была разработана с учётом обширных системных знаний и опыта, накопленного в ходе многих миссий, а это значит, что почти наверняка найдётся система, которая удовлетворит ваши потребности. Платы STARBUCK-PICO и STARBUCK-NANO CubeSat EPS специально разработаны для удовлетворения требований к объёму и мощности, которые обычно требуются для миссий CubeSat размером от 1U до 16U (хотя многие наши клиенты используют STARBUCK-NANO-PLUS и для более крупных малых спутников).', 'price': '400000₽','imgSrc': 'http://127.0.0.1:9000/lab1/3.jpg'},
            {'id': 4, 'title': 'Кольцевая антенна S-диапазона AC-2000', 'shortDescription': 'Наносателлитовая антенна с поляризацией.', 'description': 'Благодаря своей универсальной конструкции и беспрецедентному опыту работы на орбите мы гордимся стабильным высоким качеством наших подсистем, в том числе CubeSat EPS (системы электропитания). Линейка STARBUCK была разработана с учётом обширных системных знаний и опыта, накопленного в ходе многих миссий, а это значит, что почти наверняка найдётся система, которая удовлетворит ваши потребности. Платы STARBUCK-PICO и STARBUCK-NANO CubeSat EPS специально разработаны для удовлетворения требований к объёму и мощности, которые обычно требуются для миссий CubeSat размером от 1U до 16U (хотя многие наши клиенты используют STARBUCK-NANO-PLUS и для более крупных малых спутников).', 'price': '700000₽','imgSrc': 'http://127.0.0.1:9000/lab1/4.jpg'},
            {'id': 5, 'title': 'Солнечные батареи CubeSat PHOTON', 'shortDescription': 'Максимальная выработка энергии и простота интеграции.', 'description': 'Солнечные панели AAC Clyde Space PHOTON предназначены для максимальной выработки электроэнергии и простоты платформы интеграция. Панели используются в наших собственных миссиях. Солнечные панели PHOTON, доступные в различных конфигурациях, совместимы с конструкциями AAC Clyde Space ZAPHOD. Боковые солнечные панели предназначены для установки на боковые панели наших конструкций CubeSat, чтобы обеспечить оптимизированную выработку энергии с любой стороны спутника. Мы используем новейшие производственные технологии для создания высоконадёжных, малогабаритных, высокоплотных решений для выработки энергии, от солнечных панелей, устанавливаемых только на корпус, до тройных развёрнутых солнечных панелей. Они предназначены для установки в большинстве механизмов развёртывания CubeSat.', 'price': '1500000₽','imgSrc': 'http://127.0.0.1:9000/lab1/5.jpg'},
            {'id': 6, 'title': 'Оптический датчик IM200', 'shortDescription': 'Универсальный интеллектуальный оптический датчик.', 'description': 'Наш универсальный интеллектуальный оптический сканер IM200 имеет разрешение 4 мегапикселя, высокоскоростной интерфейс передачи данных и различные варианты объективов. Адаптивный видеодатчик IM200 основан на платформе ST200 Star Tracker. Благодаря выделенному высокоскоростному интерфейсу USB2.0 IM200 может снимать 5 кадров в секунду в полном разрешении.', 'price': '550000₽','imgSrc': 'http://127.0.0.1:9000/lab1/6.jpg'}\
]

assemblies = [
    {'id': 1, 'components': [{'id': 2, 'count': 1}, {'id': 3, 'count': 2}, {'id': 6, 'count': 3}], 'satelliteName': 'Markus I', 'flyDate': '2020-12-20'},
    {'id': 2, 'components': [{'id': 1, 'count': 3}, {'id': 4, 'count': 3}], 'satelliteName': 'Markus II', 'flyDate': '2020-12-20'},
    {'id': 3, 'components': [{'id': 5, 'count': 4}, {'id': 6, 'count': 3}], 'satelliteName': 'Markus III', 'flyDate': '2020-12-20'},
]

curAssemblyId = 1

def GetMain(request):
    input_down = request.GET.get('down', '')
    input_up = request.GET.get('up', '')
    if input_down == '':
        input_down = '0'
    if input_up == '':
        input_up = '999999999999'
    search_components = []
    for component in components:
        if int(input_down) <= int(component['price'][:-1:]) <= int(input_up):
            search_components.append(component)
    if input_down == '0':
        input_down = ''
    if input_up == '999999999999':
        input_up = ''
        
    print(assemblies[curAssemblyId - 1].get('components'))
    return render(request, 'main.html', {'data' : {
        'curAssemblyId': curAssemblyId,
        'components': search_components,
        'price_down': input_down,
        'price_up': input_up,
        'cart_counter': len(assemblies[curAssemblyId - 1].get('components'))
    }})    
    
def GetComponent(request, id):
    return render(request, 'component.html', {'data' : {
        'id': id,
        'title': components[id-1]['title'],
        'description': components[id-1]['description'],
        'price': components[id-1]['price'],
        'imgSrc': components[id-1]['imgSrc']
    }})
    
def GetAssembly(request, id):
    curAssembly = assemblies[id - 1]
    selectedComponents = []
    componentsCount = []
    
    for curComponent in curAssembly.get('components'):
        for component in components:
            if component['id'] == curComponent['id']:
                component['count'] = curComponent['count']
                selectedComponents.append(component)
    
    return render(request, 'assembly.html', {'data' : {
        'components': selectedComponents,
    }})