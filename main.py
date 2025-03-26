from playwright.sync_api import sync_playwright
import time

def auto_cet(id_number, password):
    """四六级考试报名自动操作"""
    with sync_playwright() as p:
        # 使用Edge浏览器
        browser = p.chromium.launch(
            channel="msedge",
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--no-sandbox',
                '--start-maximized'
            ]
        )
        
        # 创建上下文
        context = browser.new_context(
            # viewport={'width': 2000, 'height': 1380},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
        )
        
        # 创建新页面
        page = context.new_page()
        
        try:
            print("正在访问登录页面...")
            page.goto('https://passport.neea.edu.cn/CETLogin?ReturnUrl=https://cet-bm.neea.edu.cn/Home/VerifyPassport/?LoginType=0&Safe=1', 
                     wait_until='networkidle',
                     timeout=30000)
            
            # time.sleep(1)  # 等待页面稳定
            
            print("选择省份...")
            page.select_option('#selectProvince', value='63')
            
            print("填写身份证号...")
            page.fill('#txtName', id_number)
            
            print("填写密码...")
            page.fill('#txtPassword', password)
            
            print("\n请在5秒内输入验证码...")
            time.sleep(5)
            
            print("点击登录按钮...")
            page.click('#btnLogin')
            
            print("等待页面跳转...")
            time.sleep(1)
            
            print("点击同意按钮...")
            page.click('#btnToAgreement')
            time.sleep(1)

            print("勾选同意协议...")
            #page.click("label[for='chkAssure']")
            page.evaluate("document.querySelector('#chkAssure').checked = true")

            is_checked = page.is_checked("#chkAssure")
            print(f"复选框是否被选中: {is_checked}")
            # time.sleep(1)

            if is_checked:
                print("复选框已被选中")
            
                print("再次确认同意...")
                page.evaluate("document.querySelector('#btnAgree').click()")
                time.sleep(1)
                
                print("点击搜索...")
                page.click('#btnSearch')
                time.sleep(2)
                page.evaluate("document.querySelector('#chkAssure').checked = true")
                time.sleep(1)
                page.evaluate("document.querySelector('#btnAgree').click()")

                time.sleep(1)
                page.click('.l-btn-left')

                time.sleep(1)
                page.click('.l-btn-left')

                print("\n自动操作已完成！按Ctrl+C退出程序")
                # 保持浏览器开启
                while True:
                    time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n程序已退出")
        except Exception as e:
            print(f"发生错误: {e}")
            try:
                page.screenshot(path="error.png")
                print("已保存错误截图到 error.png")
            except:
                pass
        finally:
            browser.close()

if __name__ == "__main__":
    # 配置信息
    id_number = ""  # 身份证号
    password = ""  # 密码
    
    # 开始执行
    auto_cet(id_number, password)