# -*- coding: utf-8 -*-
import logging
import re
import time

from selenium import webdriver

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)
# 设置chromedriver的存放位置
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
driver.get(r'http://sxnxs.21tb.com')

# 防止有人的网络特别慢，每步的间隔均设置 5 秒，以便稳定，如果某步报错了可适当增加延时
time.sleep(3)

##这里改成你的用户名，一般为身份证号
driver.find_element_by_xpath('//*[@id="loginName"]').send_keys('18082516201')
##这里改成你的密码，一般为身份证号
driver.find_element_by_xpath('//*[@id="password1"]').send_keys('18082516201')
driver.find_element_by_class_name("login_Btn").click()

time.sleep(3)

# 如果提示异常登陆时自动点击确认，不需要手动点击
try:

    btn_primary = driver.find_element_by_class_name("btn-primary").click()

    #if btn_primary:
        #btn_primary.click()
    #driver.find_element_by_xpath('//*[@id="dialog-content"]/div/input[1]').click()
    time.sleep(5)
except:
    pass

try:
    print(f"{time.strftime('%Y-%m-%d %T')} 直接进入学习地图")
    driver.get('http://sxnxs.21tb.com/els/html/index.parser.do?id=0007')
    time.sleep(2)
    print(f"{time.strftime('%Y-%m-%d %T')} 进入课程列表")
    driver.find_element_by_xpath('//*[@id="trackList"]/ul/li[1]/div[2]/div[3]/a').click()
    time.sleep(2)
except:
    pass
##查找未学的课程的 id 保存至变量 corses 列表中
regex = re.compile('<a href="#" id="(.*)" title="(.*)" class="innercan goCourseByStudy"')
corses = re.findall(regex, driver.page_source)
toltal_count = len(corses)
learn_num = 4
while learn_num < toltal_count:
    # print("直接进入学习地图")
    # driver.get('http://e-learning.jsnx.net/els/html/index.parser.do?id=0007')
    # time.sleep(5)
    # print("进入课程列表")
    # driver.find_element_by_xpath('//*[@id="trackList"]/ul/li[1]/div[2]/div[3]/a').click()
    # time.sleep(5)
    # ##查找未学的课程的 id 保存至变量 corses 列表中
    # regex = re.compile('<a href="#" id="(.*)" title=.*class="innercan goCourseByStudy"')
    # corses = re.findall(regex,driver.page_source)
    # if corses == []:  break ##说明没有待学的课程，已全部学完，直接退出循环

    print(f"{time.strftime('%Y-%m-%d %T')} 将学习的课程ID为: {corses[learn_num][0]},课程名称: {corses[learn_num][1]}")
    xpath = f'//*[@id="{corses[learn_num][0]}"]'
    learn_num += 1

    ##循环点击待学习的课程
    ##注意第一次播放时需要启用一下 Flash player,根据浏览器提示右键点击一下即可启用，只需要处理一次即可。
    try:
        driver.find_element_by_xpath(xpath).click()
    except:
        pass
    print("开始播放")
    handles = driver.window_handles

    time.sleep(1)
    ##切换浏览器标签页
    for handle in handles:
        if driver.current_window_handle != handle:
            driver.switch_to.window(handle)
            break

    ##最低观看60s 后检查是否可以进行课程评估
    time.sleep(60)

    # regex_count_item = re.compile('<div class="cl-catalog-item-sub">')

    regex_count_item = re.compile(
        '<a href="javascript:;" data-id=".*" title="(.*)" class="scormItem-no cl-catalog-link cl-catalog-link-sub')
    vedios = re.findall(regex_count_item, driver.page_source)
    print(vedios)
    count = len(vedios)
    if count > 0:
        print(f"{time.strftime('%Y-%m-%d %T')} 当前页面的视频个数为 {count},正在播放 {vedios[0]}...")
        # 判断上一个是否完成
        # 如果完成就点击下一个
        # 如果有正在播放的就等待
        i = 2
        while i <= count:
            while True:
                regex_count_item = re.compile('item-no cl-catalog-playing"')
                playings = re.findall(regex_count_item, driver.page_source)
                if len(playings) > 0:
                    time.sleep(30)
                else:
                    print(f"{time.strftime('%Y-%m-%d %T')} 播放完成。")
                    break
            ##判断已经学过了多少
            time.sleep(1)
            regex_done = re.compile('item-done cl-catalog-link-done"')
            dones = re.findall(regex_done, driver.page_source)
            i = len(dones) + 1
            if i > count:
                break
            vedio_xpath = f'//*[@id="courseItemId"]/ol/li/div[{i}]/a'
            try:
                driver.find_element_by_xpath(vedio_xpath).click()
            except:
                pass
            print(f"{time.strftime('%Y-%m-%d %T')} 正在播放{vedios[i-1]}")
            time.sleep(10)

    print(f"{time.strftime('%Y-%m-%d %T')} 开始检查是否可以进行课程评估")

    tmp_count = 0
    while True:
        # 循环判断是否出现[进入下一步】按钮，如有说明视频已经看完，可以进行课程评估
        if tmp_count >= 50:  ##如果超过 20 分钟，则跳出循环，防止死循环
            break
        try:
            driver.find_element_by_xpath('//*[@id="goNextStep"]/a').click()
            time.sleep(5)
            break
        except:
            pass
        time.sleep(30)
        tmp_count += 1

    try:
        ##开始进行课程评估
        print(f"{time.strftime('%Y-%m-%d %T')} 开始进行课程评估")
        time.sleep(2)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='★'])[3]/following::input[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='B'])[1]/following::span[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='B'])[2]/following::span[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='B'])[3]/following::span[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='B'])[4]/following::span[1]").click()
        time.sleep(2)
        driver.find_element_by_id("courseEvaluateSubmit").click()
        time.sleep(2)
        driver.find_element_by_link_text(u"确定").click()
        time.sleep(2)
        driver.find_element_by_link_text(u"查看结果").click()
        time.sleep(2)
        print(f"{time.strftime('%Y-%m-%d %T')} 已提交课程评估")
    except:
        pass

    ##切换浏览器标签页
    for handle in handles:
        if driver.current_window_handle != handle:
            driver.switch_to.window(handle)
            break
    time.sleep(2)
    # 刷新下，看看已经学了多少

    try:
        print(f"{time.strftime('%Y-%m-%d %T')} 直接进入学习地图")
        driver.get(r'http://sxnxs.21tb.com/els/html/index.parser.do?id=0007')
        time.sleep(2)
        print(f"{time.strftime('%Y-%m-%d %T')} 进入课程列表")
        driver.find_element_by_xpath('//*[@id="trackList"]/ul/li[1]/div[2]/div[3]/a').click()
        time.sleep(2)
    except:
        pass
# 退出浏览器
driver.quit()
