import openpyxl
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select




driver = webdriver.Chrome()

htx_reg_no = "30820242503882850557"
driver.get("https://www.wetax.go.kr/main/?cmd=LPEPBN3R0&TAX_SEQ=" + htx_reg_no)

time.sleep(0.5)


########## 1page
# 신고인 구분
element = driver.find_element(By.ID, 'dclrGbn')
select = Select(element)
select.select_by_index(1) #select index value


# 징수의무자 식별번호구분
element = driver.find_element(By.ID, 'dscmNoClCd')
select = Select(element)
select.select_by_index(2) #select index value


# 징수의무자 식별번호
corp_no = "3080526331"
textbox = driver.find_element(By.ID, "dscmNo")
textbox.send_keys(corp_no)


# 확인 버튼 클릭
button = driver.find_element(By.ID, "btnOk")
button.click()

time.sleep(0.5)


########## 1page > 2page
button = driver.find_element(By.ID, "btnOk")
button.click()




########## 2page
## 사업장 번호 조회 버튼 클릭
button = driver.find_element(By.ID, "btnBrnoInfoList")
button.click()

# 조회되는 사업장의 개수
find_corp_cnt = int(driver.find_element(By.ID, 'spnTotCnt').text)

if find_corp_cnt != 1:
    print("========== 사업장 2개 이상 존재 ==========")
    #중단! 예외처리

# 라벨 클릭
element = driver.find_element(By.XPATH, '//*[@id="tbl_brnoInfoList"]/tbody/tr/td[1]/span/label')
element.click()

# 선택 버튼 클릭
button = driver.find_element(By.ID, "btn_confirm")
button.click()

## 휴대폰 번호 입력
hp_no = "010-5516-5336"

textbox = driver.find_element(By.ID, "dclrRlpMblTelno")
textbox.send_keys(hp_no)

textbox = driver.find_element(By.ID, "txpMblTelno")
textbox.send_keys(hp_no)

#다음 버튼 클릭
button = driver.find_element(By.ID, "btnNext")
button.click()



is_ok = input()

if is_ok == 1:
    driver.quit()






