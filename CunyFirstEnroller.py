from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
import gmail
import random


class CunyFirstEnroller:
    home_page = "https://home.cunyfirst.cuny.edu"
    student_center = "https://cssa.cunyfirst.cuny.edu/psc/cnycsprd/EMPLOYEE/CAMP/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fcssa.cunyfirst.cuny.edu%2fpsc%2fcnycsprd%2fEMPLOYEE%2fCAMP%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentURL=https%3a%2f%2fcssa.cunyfirst.cuny.edu%2fpsc%2fcnycsprd%2fEMPLOYEE%2fCAMP%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider=CAMP&PortalCRefLabel=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"
    class_search_page = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL"
    class_search_page_id = "ACE_DERIVED_CLSRCH_GROUP2"
    close_button_name = "closebtn"
    username_id = "CUNYfirstUsernameH"
    password_id = "CUNYfirstPassword"
    shopping_cart_id = "DERIVED_SSS_SCL_SSS_ENRL_CART"
    select_term_id = "SSR_DUMMY_RECV1$scroll$0"
    select_term_continue_button_id = "DERIVED_SSS_SCT_SSR_PB_GO"
    class_select_box_id = "win0divP_SELECT$"
    cart_enroll_button_id = "DERIVED_REGFRM1_LINK_ADD_ENRL$"
    enroll_submit_button_id = "win0divDERIVED_REGFRM1_SSR_PB_SUBMIT"
    enroll_result_msg_id = "trSSR_SS_ERD_ER$0_row"
    loading_icon_id = "WAIT_win0"


    institution_box_id = "CLASS_SRCH_WRK2_INSTITUTION$31$"
    term_box_id = "CLASS_SRCH_WRK2_STRM$35$"
    subject_box_id = "SSR_CLSRCH_WRK_SUBJECT_SRCH$0"
    open_class_only_id = "SSR_CLSRCH_WRK_SSR_OPEN_ONLY$5"
    class_nbr_box_id = "SSR_CLSRCH_WRK_CLASS_NBR$10"
    class_search_button_id = "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"
    status_id = "win0divSSR_CLS_DTL_WRK_SSR_STATUS_LONG"
    view_search_result_button_id = "CLASS_SRCH_WRK2_SSR_PB_BACK"

    def __init__(self, head=None):
        chromedriver_path = os.getcwd() + r"\chrome\chromedriver.exe"
        if head == "headless":
            options = Options()
            options.binary_location = os.getcwd() + r'\chrome\chrome.exe'
            options.add_argument('--headless')
            self.browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
        else:
            self.browser = webdriver.Chrome(chromedriver_path)

    def login(self, login_id, login_pw):
        self.browser.get(self.home_page)
        # self.browser.find_element_by_name(self.close_button_name).click()
        self.browser.find_element_by_id(self.username_id).send_keys(login_id)
        self.browser.find_element_by_id(self.password_id).send_keys(login_pw)
        self.browser.find_element_by_name('submit').click()
        if self.home_page in self.browser.current_url:
            return True
        elif "portaldown" in self.browser.current_url:
            print("CUNYfirst System Unavailable")
            return False
        else:
            print("Login Failed")
            return False

    def quit(self):
        self.browser.quit()

    def loading(self):
        try:
            WebDriverWait(self.browser, 600).until(
                ec.invisibility_of_element_located((By.ID, self.loading_icon_id))
            )
            return True
        except TimeoutException:
            print("[!]TimeoutException")
            return False

    def enroll_cart(self, term=None, delay=60, enroll_all=False):
        self.browser.get(self.student_center)
        self.browser.find_element_by_id("win0divDERIVED_SSS_SCL_SSS_ENRL_CART$276$").click()
        self.loading()

        all_success = False
        while all_success is False:
            print(time.asctime(time.localtime(time.time())))
            text = 'Select a term then select Continue.'
            if text in self.browser.page_source:
                if term is None:
                    print("Need to specify term")
                    return False
                else:
                    print("ha")
                    self.browser.find_element_by_xpath("//*[contains(text(), '{}')]"
                                                       "/parent::*/parent::*/preceding-sibling::*"
                                                       .format(term)).click()
                    self.browser.find_element_by_id("{}".format(self.select_term_continue_button_id)).click()
                    self.loading()

                    classes = self.browser.find_elements_by_xpath(
                        "//div[starts-with(@id, '{}')]".format(self.class_select_box_id))
                    for k in range(len(classes)):
                        classes[k].click()

                    warning_text = 'valid'
                    while True:
                        self.browser.find_element_by_xpath(
                            "//*[starts-with(@id, '{}')]".format(self.cart_enroll_button_id)).click()
                        self.loading()
                        if warning_text in self.browser.page_source:
                            time.sleep(delay)
                        else:
                            break

                    self.browser.find_element_by_id('{}'.format(self.enroll_submit_button_id)).click()
                    self.loading()
                    message_elm = self.browser.find_elements_by_xpath(
                        "//*[starts-with(@id, '{}')]".format(self.enroll_result_msg_id))

                    subject = 'CunyFirst Enroller'
                    message = ''
                    for k in range(len(message_elm)):
                        message = message + message_elm[k].text + '<br/><br/>'
                    self.loading()

                    if 'full' not in message:
                        all_success = True

                    if enroll_all is True:
                        self.browser.get(self.shopping_cart_page)
                        if 'Success' in message:
                            gmail.send_email('your_email@gmail.com', message)
                    else:
                        gmail.send_email('your_email@gmail.com', message)
                        break

    def check_class(self, io, to, so, nbr, delay=180, times=20):
        try:
            self.browser.find_element_by_id(self.class_search_page_id)
        except (StaleElementReferenceException, NoSuchElementException):
            self.browser.get(self.class_search_page)

        institution_select = Select(self.browser.find_element_by_id(self.institution_box_id))
        institution_select.select_by_visible_text(io)
        self.loading()
        term_select = Select(self.browser.find_element_by_id(self.term_box_id))
        term_select.select_by_visible_text(to)
        self.loading()
        subject_select = Select(self.browser.find_element_by_id(self.subject_box_id))
        subject_select.select_by_value(so)
        self.loading()

        # settings for Search Criteria
        if self.browser.find_element_by_id(self.open_class_only_id).is_selected():
            self.browser.find_element_by_id(self.open_class_only_id).click()
            class_nbr_input = self.browser.find_element_by_id(self.class_nbr_box_id)
            class_nbr_input.send_keys(nbr)

        # click on the search button
        search_button = self.browser.find_element_by_id(self.class_search_button_id)
        self.browser.execute_script("arguments[0].click();", search_button)
        self.loading()

        if "no results" in self.browser.page_source:
            print("The search returns no results that match the criteria specified.")
            return False

        while(times > 0):
            # click the first class to view its details
            try:
                first_class = self.browser.find_element_by_id("MTG_CLASS_NBR$0")
            except (StaleElementReferenceException, NoSuchElementException):
                return False

            self.browser.execute_script("arguments[0].click();", first_class)
            self.loading()

            # get status
            status_ele = self.browser.find_element_by_xpath("//div[@id='{}']/div/img".format(self.status_id))
            status = status_ele.get_attribute("alt")

            if "Closed" in status:
                print(time.asctime(time.localtime(time.time())) + " --- Closed" + " " + str(times))
                time.sleep(random.randint(80, delay))

                # click on View Search Results button
                view_results_button = self.browser.find_element_by_id(self.view_search_result_button_id)
                self.browser.execute_script("arguments[0].click();", view_results_button)
                self.loading()

                if times == 0:
                    return False
                else:
                    times = times - 1

            elif "Open" in status:
                print(time.asctime(time.localtime(time.time())) + " --- Open")
                return True

