from selenium import webdriver
import csv

# 歌单第一页URL
url = 'http://music.163.com/#/discover/playlist/' \
    '?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0'
# http://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0

# 用PhantomJS接口创建一个Selenium的WebDriver
service_args=[]
service_args.append('--load-images=no')  ##关闭图片加载
#service_args.append('--disk-cache=yes')  ##开启缓存
#service_args.append('--ignore-ssl-errors=true') ##忽略https错误

driver = webdriver.PhantomJS(service_args=service_args)

# 准备好CSV文件
csv_file = open('playlist.csv', 'w', newline='', encoding='utf8')
writer = csv.writer(csv_file)
writer.writerow(['标题', '播放数', '链接'])

# 解析结束条件：下一页为空
while url != 'javascript:void(0)':
    # 用WebDriver加载页面
    driver.get(url)
    # 切换到名为'contentFrame'的iframe
    driver.switch_to.frame('contentFrame')
    # 定位歌单标签
    data = driver.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')

    # 解析每一个歌单
    for data_i in data:
        nb = data_i.find_element_by_class_name('nb').text
        if '万' in nb and int(nb.split('万')[0]) > 500:
            # 获取播放数大于500万的歌单的封面
            msk = data_i.find_element_by_css_selector('a.msk')
            # 将标题/播放数/链接写入CSV文件
            writer.writerow([msk.get_attribute('title'), nb, msk.get_attribute('href')])
            print("{}\t：{}".format(nb, msk.get_attribute('title')))
    # 取得下一页的URL
    url = driver.find_element_by_css_selector('a.zbtn.znxt').get_attribute('href')

    offset_start = url.find('offset=')
    if offset_start != -1:
        offset = url[offset_start + 7 : len(url)]
    print("\t第{}页".format(int(int(offset) / 35)))

csv_file.close()