from bs4 import BeautifulSoup
import requests
import re

# 获取网页内容
url = "https://www.imgt.org/3Dstructure-DB/cgi/details.cgi?pdbcode=P00001"
response = requests.get(url)
html_content = response.text

# 解析HTML内容
soup = BeautifulSoup(html_content, "html.parser")

pattern = r"SeqIMGT\.cgi\?seq=(.*?)(?:&|$)"

# 使用search方法查找匹配项
match = re.search(pattern, html_content)

if match:
    # 如果找到匹配项，获取匹配的序列
    seq_value = match.group(1)
    print(seq_value)  # 输出匹配的序列
else:
    print("No sequence found.")


# domain_description_row = soup.find(
#     "td", class_="titre_h", string="IMGT domain description"
# )
# # 如果找到这一行，接着查找相邻的包含具体描述的td元素
# if domain_description_row:
#     # 由于在<tr>中，需要找到兄弟元素来获取描述
#     domain_description = domain_description_row.find_next_sibling("td", class_="data_h")
#     if domain_description:
#         # 提取并打印描述文本
#         print(domain_description.get_text(separator=" ", strip=True))
