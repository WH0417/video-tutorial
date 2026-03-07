import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

# -------------------------- 配置项 --------------------------
COLLECT_FORM_URL = "https://docs.qq.com/form/page/DVWdnRmFtWWpNd0N6"
TARGET_TIME = "18:58:00"
FORM_DATA = {
    "姓名": "测试1",
    "班级": "大数据2402",
    "学号": "202410128",
}
DEBUG_PORT = 9222
WAIT_TIMEOUT = 5

# --------------------------------------------------------------------------------
def fill_tencent_form():
    # 仅保留远程调试必要配置（删除无效选项）
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 已连接到Chrome！")

        driver.get(COLLECT_FORM_URL)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始填写表单...")

        # 填写表单逻辑
        for label, value in FORM_DATA.items():
            try:
                input_element = WebDriverWait(driver, WAIT_TIMEOUT).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f"//input[@placeholder='{label}'] | //textarea[@placeholder='{label}'] | "
                         f"//label[contains(text(), '{label}')]/following-sibling::input")
                    )
                )
                input_element.clear()
                input_element.send_keys(value)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 已填写：{label} = {value}")
            except TimeoutException:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 未找到字段「{label}」")

        # 提交表单
        try:
            submit_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '提交')]"))
            )
            submit_button.click()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 表单已提交！")
        except TimeoutException:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 未找到提交按钮")

    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 执行出错：{str(e)}")
    finally:
        if driver:
            driver.quit()

def main():
    print(f"程序已启动，将在 {TARGET_TIME} 填写收集表...")
    schedule.every().day.at(TARGET_TIME).do(fill_tencent_form)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()