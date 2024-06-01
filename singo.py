
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
        time.sleep(1)

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

        time.sleep(1)


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
            time.sleep(0.5)

            button = singo_driver.find_element(By.ID, "btnNext")
            button.click()

            time.sleep(0.5)

            alert = singo_driver.switch_to.alert
            alert.accept()
            
        

        #제출 버튼 클릭
        time.sleep(1)

        try:
            button = singo_driver.find_element(By.ID, "btnCmptn")
        except Exception as e:
            is_next = input()
            print(e)
            return
        
        button.click()

        time.sleep(0.5)
        
        alert = singo_driver.switch_to.alert
        alert.accept()


        time.sleep(3)


        #전자납부번호
        try:
            payNo = singo_driver.find_element(By.ID, 'elpn').text
        except Exception as e:
            print(e)
            is_check = input()
        
        print("=====================")
        print("전자납부번호: ", payNo)
        print("=====================")

        #납부계좌 토글 클릭
        toggle_button = singo_driver.find_element(By.CLASS_NAME, 'toggle')
        time.sleep(0.5)
        singo_driver.execute_script("arguments[0].click();", toggle_button)
        time.sleep(0.5)

        # 납부계좌 테이블 행 추출
        rows = singo_driver.find_elements(By.CSS_SELECTOR, 'table[name="tblVrActnoList"] tbody tr')

        # 납부계좌 목록 문자열로 생성
        # 단, 전국공통(지방세입) 제외
        acct_list_string = ''
        for i in range(0, len(rows)):

            if i == 4:
                break

            row = rows[i]
            bank = row.find_elements(By.CSS_SELECTOR, 'td')[0].text

            if bank == '전국공통(지방세입)':
                continue
        
            account = row.find_elements(By.CSS_SELECTOR, 'td')[1].text
            
            acct_list_string += bank + " " + account + "\n"

        print("가상계좌목록:")
        print(acct_list_string)


        # 크롬 창 꺼지기 방지 
        is_ok = input()

        if is_ok == 1:
            singo_driver.quit()
        

        






