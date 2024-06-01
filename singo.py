
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class CorpSingo:


    def __init__(self, singo_input_data: dict):
        
        self.ht_tin         = singo_input_data.get("HT_TIN"         , "") if singo_input_data.get("HT_TIN")         != None else ""
        self.htx_reg_no     = singo_input_data.get("HTX_REG_NO"     , "") if singo_input_data.get("HTX_REG_NO")     != None else ""
        self.tot_htax_amt   = singo_input_data.get("TOT_HTAX_AMT"   , "") if singo_input_data.get("TOT_HTAX_AMT")   != None else ""
        self.corp_no        = singo_input_data.get("CORP_NO"        , "") if singo_input_data.get("CORP_NO")        != None else ""
        self.corp_nm        = singo_input_data.get("CORP_NM"        , "") if singo_input_data.get("CORP_NM")        != None else ""
        self.user_nm        = singo_input_data.get("USER_NM"        , "") if singo_input_data.get("USER_NM")        != None else ""
        self.hp_no          = singo_input_data.get("HP_NO"          , "") if singo_input_data.get("HP_NO")          != None else ""
        self.corp_addr      = singo_input_data.get("CORP_ADDR"      , "") if singo_input_data.get("CORP_ADDR")      != None else ""
        self.corp_lb_addr   = singo_input_data.get("CORP_LB_ADDR"   , "") if singo_input_data.get("CORP_LB_ADDR")   != None else ""


    def singo(self):

        singo_driver = webdriver.Chrome()
        singo_driver.get("https://www.wetax.go.kr/main/?cmd=LPEPBN3R0&TAX_SEQ=" + self.htx_reg_no)
        time.sleep(0.8)

        ########## 1page
        # 신고인 구분
        element = singo_driver.find_element(By.ID, 'dclrGbn')
        select = Select(element)
        select.select_by_index(1) #select index value


        # 징수의무자 식별번호구분
        element = singo_driver.find_element(By.ID, 'dscmNoClCd')
        select = Select(element)
        select.select_by_index(2) #select index value


        # 징수의무자 식별번호
        textbox = singo_driver.find_element(By.ID, "dscmNo")
        textbox.send_keys(self.corp_no)


        # 확인 버튼 클릭
        button = singo_driver.find_element(By.ID, "btnOk")
        button.click()

        time.sleep(0.5)


        ########## 1page > 2page
        button = singo_driver.find_element(By.ID, "btnOk")
        button.click()


        ########## 2page
        ## 사업장 번호 조회 버튼 클릭
        button = singo_driver.find_element(By.ID, "btnBrnoInfoList")
        button.click()

        # 조회되는 사업장의 개수
        find_corp_cnt = int(singo_driver.find_element(By.ID, 'spnTotCnt').text)

        if find_corp_cnt > 1:
            print("========== 사업장 2개 이상 존재 ==========")
            return

        # 라벨 클릭
        element = singo_driver.find_element(By.XPATH, '//*[@id="tbl_brnoInfoList"]/tbody/tr/td[1]/span/label')
        element.click()

        # 선택 버튼 클릭
        button = singo_driver.find_element(By.ID, "btn_confirm")
        button.click()

        ## 휴대폰 번호 입력
        textbox = singo_driver.find_element(By.ID, "dclrRlpMblTelno")
        textbox.send_keys(self.hp_no)

        textbox = singo_driver.find_element(By.ID, "txpMblTelno")
        textbox.send_keys(self.hp_no)


        ########## 2page > 3page > 4page > 5page
        # 다음 버튼 클릭 후, 브라우저 알림창 확인처리
        for move in range(4):
            time.sleep(0.3)

            button = singo_driver.find_element(By.ID, "btnNext")
            button.click()

            time.sleep(0.2)

            alert = singo_driver.switch_to.alert
            alert.accept()
        

        # 크롬 창 꺼지기 방지 
        is_ok = input()

        if is_ok == 1:
            singo_driver.quit()

        






