import requests
from bs4 import BeautifulSoup

# 定义POST请求的URL
url = "https://www.imgt.org/3Dstructure-DB/cgi/3Dquery.cgi"

# 定义要发送的数据
data = {
    "type-result": "ProteinOverview",
    "PDBCode": "",  # 空字符串表示没有提供值
    "Proteinname": "",
    "type-entry": "any",
    "species": "any",
    "ReceptorType": "IG",
    "DomType": "any",
    "LigandCat": "any",
    "PepLength": "any",
    "ReceptorDesc": "any",
    "ChainDesc": "any",
    "DomainDesc": "any",
    "groups": "any",
    "subgroups": "any",
    "genes": "IGHV1-69",
    "Allele": "",
    "CDR1length": "",
    "CDR2length": "",
    "CDR3length": "",
    "CDR1pattern": "",
    "CDR2pattern": "",
    "CDR3pattern": "",
    "submit": "Search",
    "release_date": "any",
    "resol": "any",
    "experiment": "any",
    "type-ref": "PUBMED",
    "pmid": "any",
    "author": "",
    "journal": "",
    "title": "",
    "year": "any",
    "AA": "",
    "PosAA": "",
    "SS": "any",
    "PosSS": "",
    "Phi": "",
    "PosPhi": "",
    "Psi": "",
    "PosPsi": "",
    "ASA": "",
    "PosASA": "",
    "ContType": "any",
    "PosCont1": "",
    "PosCont2": "",
    "Query": "",
    "ANDOR": "AND",
    "numres": 10,
    "sequence": "",
}

# 发送POST请求
response = requests.post(url, data=data)
html_content = response.text
# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, "html.parser")

# 找到所有的<a>标签，它们包含了IMGT entry ID
a_tags = soup.find_all("a")

# 初始化一个列表来存储IMGT entry ID
imgt_entry_ids = []

# 遍历所有的<a>标签
for tag in a_tags:
    # 检查<a>标签的href属性中是否包含'details.cgi?pdbcode='字符串
    if "details.cgi?pdbcode=" in tag.get("href", ""):
        # 提取pdbcode的值，并添加到列表中
        pdbcode = tag.get("href").split("pdbcode=")[1]
        imgt_entry_ids.append(pdbcode)

# 打印所有的IMGT entry ID
# for entry_id in imgt_entry_ids:
#     print(entry_id)

print(len(imgt_entry_ids))
