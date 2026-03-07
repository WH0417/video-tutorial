import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from dotenv import load_dotenv

# 加载环境变量（建议敏感信息放.env文件，避免硬编码）
load_dotenv()


# -------------------------- 配置项 --------------------------
# 腾讯文档收集表网址
COLLECT_FORM_URL = os.getenv("COLLECT_FORM_URL", "https://docs.qq.com/form/page/DVWdnRmFtWWpNd0N6")
# 定时执行时间（24小时制，格式："HH:MM:SS"）
TARGET_TIME = os.getenv("TARGET_TIME", "19:20:00")

# 要填写的表单信息（key=输入框标签/占位符，value=要填写的内容）
FORM_DATA = {
    "姓名": "测试1",
    "班级": "大数据2402",
    "学号": "202410128"
    # 可根据实际表单字段继续添加
}
# ChromeDriver 路径（如果已配置环境变量，可设为 None,未配置环境变量,ChromeDriver的绝对路径）
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH",None)

# 等待元素加载的超时时间（秒）
WAIT_TIMEOUT = 1



# --------------------------------------------------------------------------------
def fill_tencent_form():
    """自动填写腾讯文档收集表"""
    # 初始化Chrome浏览器
    chrome_options = webdriver.ChromeOptions()
    # 可选：禁用图片加载，提升速度
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 可选：取消浏览器自动化提示
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        # 启动浏览器
        if CHROME_DRIVER_PATH:
            driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)

        # 最大化窗口（避免元素被遮挡）
        driver.maximize_window()

        # 访问收集表网址
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在打开收集表...")
        driver.get(COLLECT_FORM_URL)

        # 遍历表单数据，自动填写
        for label, value in FORM_DATA.items():
            try:
                # 定位输入框（优先通过placeholder/label文本定位，可根据实际调整）
                # 常见定位方式：name、id、xpath、css_selector，需根据实际表单结构调整
                input_element = WebDriverWait(driver, WAIT_TIMEOUT).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f"//input[@placeholder='{label}'] | //textarea[@placeholder='{label}'] | //label[text()='{label}']/following-sibling::input")
                    )
                )
                # 清空输入框（防止有默认值）
                input_element.clear()
                # 输入内容
                input_element.send_keys(value)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 已填写：{label} = {value}")
            except TimeoutException:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 未找到字段「{label}」，请检查定位方式")
            except NoSuchElementException:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 字段「{label}」不存在，请核对表单字段")

        # 定位提交按钮并点击（需根据实际按钮文本调整，如"提交"、"确认"、"保存"）
        try:
            submit_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '提交')]"))
            )
            submit_button.click()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 表单已提交！")
        except TimeoutException:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 未找到提交按钮，请检查按钮文本")


    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 执行出错：{str(e)}")
    finally:
        # 可选：是否关闭浏览器（如需验证结果，可注释此行）
        # driver.quit()
        pass


def main():
    """主函数：配置定时任务"""
    print(f"程序已启动，将在 {TARGET_TIME} 自动填写收集表...")
    print(f"目标网址：{COLLECT_FORM_URL}")

    # 添加定时任务
    schedule.every().day.at(TARGET_TIME).do(fill_tencent_form)

    # 循环检测定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)  # 每秒检测一次，减少资源占用


if __name__ == "__main__":
    main()