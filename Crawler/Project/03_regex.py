import re


# 读取网页内容
def read_html(page):
    page = str(page)
    with open('./Web/链家-第' + page + '页.html', 'rt') as f:
        content = f.read()
    return content


# 获取城区
def find_urban(content):
    L = []
    connect = ''
    urbans = re.findall(r"""<a target="_blank" href="/zufang/.+</a>-""", content)
    for urban in urbans:
        word = re.findall(r"[\u4e00-\u9fa5]", urban)
        s = connect.join(word)
        L.append(s)
    return L


# 查找站点
def find_busstation(content):
    L = []
    connect = ''
    busstations = re.findall(r"""-<a href="/zufang/.+</a>""", content)
    for busstation in busstations:
        word = re.findall(r"[\u4e00-\u9fa5]", busstation)
        s = connect.join(word)
        L.append(s)
    return L


# 获取房屋面积
def find_area(content):
    L = []
    connect = ''
    areas = re.findall(r"""</i>\n\s*.+㎡\n\s*<i>""", content)
    for area in areas:
        word = re.findall(r"[0-9]", area)
        s = connect.join(word)
        L.append(s)
    return L


# 查找房屋朝向
def find_orientations(content):
    L = []
    connect = ''
    orientations = re.findall(r"""<i>/</i>.+<i>/</i>""", content)
    for orientation in orientations:
        word = re.findall(r"[\u4e00-\u9fa5]", orientation)
        s = connect.join(word)
        L.append(s)
    return L


# 查找房屋户型
def find_layouts(content):
    L = []
    connect = ''
    layouts = re.findall(r""".室.厅.卫""", content)
    for layout in layouts:
        L.append(layout)
    return L


# 查找房屋层数
def find_piles(content):
    L = []
    connect = ''
    piles = re.findall(r""".楼层\s*（.+）""", content)
    for pile in piles:
        word = re.sub(r"\s*", '', pile)
        s = connect.join(word)
        L.append(s)
    return L


# 循环取房产信息
def get_house(L1, L2, L3, L4, L5, L6):
    L = []
    for _ in range(23):
        info = L1[_] + "," + L2[_] + "," + L3[_] + "," + L4[_] + ',' + L5[_] + ',' + L6[_]
        L.append(info)
    return L


# 循环取网页信息
def get_html(page):
    List = {}
    for _ in range(page):
        content = read_html(page)
        L1 = find_urban(content)
        L2 = find_busstation(content)
        L3 = find_area(content)
        L4 = find_orientations(content)
        L5 = find_layouts(content)
        L6 = find_piles(content)
        L = get_house(L1, L2, L3, L4, L5, L6)
        List[_] = L
    return List


List = get_html(2)
print(List)
