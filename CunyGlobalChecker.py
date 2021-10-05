from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import os
import gmail

import CunyFirstEnroller


class CunyGlobalChecker:

    global_search_page = "https://globalsearch.cuny.edu/CFGlobalSearchTool/_search.jsp"
    term_box_id = "t_pd"
    next_buttom_name = "next_btn"
    subject_id = "subject_ld"
    career_id = "courseCareerId"
    open_class_id = "open_classId"
    additional_criteria_id = "imageDivLink"
    instructor_box_id = "instructorId"
    instructor_name_input_box_id = "instructorNameId"
    search_buttom_id = "btnGetAjax"
    result_expand_id = "imageDivLink_inst0"
    status_id = "SSR_CLS_DTL_WRK_SSR_DESCRSHORT"

    loading_icon_id = "WAIT_win0"
    global_search_page_new = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/GUEST/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fGUEST%2fHRMS%2fc%2fCOMMUNITY_ACCESS.CLASS_SEARCH.GBL&PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fGUEST%2fHRMS%2fc%2fCOMMUNITY_ACCESS.CLASS_SEARCH.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Class%20Search&PortalRegistryName=GUEST&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode=ENTP&NoCrumbs=yes"
    institution_box_id = "CLASS_SRCH_WRK2_INSTITUTION$31$"
    term_box_id_new = "CLASS_SRCH_WRK2_STRM$35$"
    subject_box_id = "SSR_CLSRCH_WRK_SUBJECT_SRCH$0"
    open_class_only_id = "SSR_CLSRCH_WRK_SSR_OPEN_ONLY$5"
    class_nbr_box_id = "SSR_CLSRCH_WRK_CLASS_NBR$10"
    class_search_button_id = "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"
    clear_button_id = "CLASS_SRCH_WRK2_SSR_PB_CLEAR"
    first_result_id = "MTG_CLASS_NBR$0"
    status_id_new = "win0divSSR_CLS_DTL_WRK_SSR_STATUS_LONG"
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

    def check_class(self, io, to, so, career, ln, cls_num, delay):
        try:
            self.browser.get(self.global_search_page)

            institution_check_box = self.browser.find_element_by_id(io)
            self.browser.execute_script("arguments[0].click();", institution_check_box)

            term_select = Select(self.browser.find_element_by_id(self.term_box_id))
            term_select.select_by_visible_text(to)

            next_buttom = self.browser.find_element_by_name(self.next_buttom_name)
            self.browser.execute_script("arguments[0].click();", next_buttom)

            subject_select = Select(self.browser.find_element_by_id(self.subject_id))
            subject_select.select_by_visible_text(so)

            career_select = Select(self.browser.find_element_by_id(self.career_id))
            career_select.select_by_visible_text(career)

            open_class_buttom = self.browser.find_element_by_id(self.open_class_id)
            self.browser.execute_script("arguments[0].click();", open_class_buttom)

            additional_criteria = self.browser.find_element_by_id(self.additional_criteria_id)
            self.browser.execute_script("arguments[0].click();", additional_criteria)

            instructor_select = Select(self.browser.find_element_by_id(self.instructor_box_id))
            instructor_select.select_by_visible_text("contains")

            instructor_name_input = self.browser.find_element_by_id(self.instructor_name_input_box_id)
            instructor_name_input.send_keys(ln)

            search_buttom = self.browser.find_element_by_id(self.search_buttom_id)
            self.browser.execute_script("arguments[0].click();", search_buttom)

            result_classes = self.browser.find_elements_by_xpath("//*[contains(@id, 'imageDivLink')]")
            for i in range(len(result_classes)):
                self.browser.execute_script("arguments[0].click();", result_classes[i])

            target_class = self.browser.find_element_by_link_text(cls_num)
            self.browser.execute_script("arguments[0].click();", target_class)

            while (1):
                status_ele = self.browser.find_element_by_id(self.status_id)
                status = status_ele.text

                if "Closed" in status:
                    print(time.asctime(time.localtime(time.time())) + "  (" + cls_num + ") --- Closed")
                    time.sleep(delay)

                    self.browser.refresh()
                elif "Open" in status:
                    print(time.asctime(time.localtime(time.time())) + "  (" + cls_num + ") --- Open")
                    return True
        except:
            return False

    def check_class_new(self, io, to, so, cls_num, delay):
        try:
            self.browser.get(self.global_search_page_new)

            school_select = Select(self.browser.find_element_by_id(self.institution_box_id))
            school_select.select_by_visible_text("Hostos CC")
            self.loading()
            school_select = Select(self.browser.find_element_by_id(self.institution_box_id))
            school_select.select_by_visible_text(io)
            self.loading()
            school_select = Select(self.browser.find_element_by_id(self.institution_box_id))
            school_select.select_by_visible_text(io)
            self.loading()

            term_select = Select(self.browser.find_element_by_id(self.term_box_id_new))
            term_select.select_by_visible_text(to)
            self.loading()

            clear_button = self.browser.find_element_by_id(self.clear_button_id)
            self.browser.execute_script("arguments[0].click();", clear_button)


            subject_select = Select(self.browser.find_element_by_id(self.subject_box_id))
            subject_select.select_by_visible_text(so)
            self.loading()

            # settings for Search Criteria
            if self.browser.find_element_by_id(self.open_class_only_id).is_selected():
                self.browser.find_element_by_id(self.open_class_only_id).click()
                class_nbr_input = self.browser.find_element_by_id(self.class_nbr_box_id)
                class_nbr_input.send_keys(cls_num)


            # click on the search button
            search_button = self.browser.find_element_by_id(self.class_search_button_id)
            self.browser.execute_script("arguments[0].click();", search_button)
            self.loading()

            # click on the first result
            first_result = self.browser.find_element_by_id(self.first_result_id)
            self.browser.execute_script("arguments[0].click();", first_result)
            self.loading()

            while (1):
                # get status Closed or Open
                status_ele = self.browser.find_element_by_xpath("//div[@id='{}']/div/img".format(self.status_id_new))
                status = status_ele.get_attribute("alt")
                self.loading()

                if "Closed" in status:

                    print(time.asctime(time.localtime(time.time())) + "  (" + str(cls_num) + ") --- Closed")
                    time.sleep(delay)

                    view_results_button = self.browser.find_element_by_id(self.view_search_result_button_id)
                    self.browser.execute_script("arguments[0].click();", view_results_button)
                    self.loading()

                    # click on the first result again
                    first_result = self.browser.find_element_by_id(self.first_result_id)
                    self.browser.execute_script("arguments[0].click();", first_result)
                    self.loading()

                elif "Open" in status:
                    print(time.asctime(time.localtime(time.time())) + "  (" + str(cls_num) + ") --- Open")
                    return True

        except:
            return False

# school = "City College"
# term = "2019 Fall Term"
# subject = "EE - Electrical Engineering"
# cls_number = 21852
# email = "your_email@gmail.com"
# delay = 15
# counter = 20
# while(counter > 0):
#     counter -= 1
#
#     checker = CunyGlobalChecker("headles")
#     availability = checker.check_class_new(school, term, subject, cls_number, delay)
#
#     if availability:
#         gmail.send_email(email, "Class '{}' is available for register.".format(cls_number))
#
#         enroller = CunyFirstEnroller.CunyFirstEnroller()
#         enroller.login("dasha.melville54", "Damelv@3832")
#         enroller.enroll_cart(term)
#         enroller.quit()
#         checker.quit()
#         break
#     else:
#         gmail.send_email('reincara@gmail.com', "Something Went Wrong With Your Program!     " + str(cls_number))
#         checker.quit()

school = "CTY01"
term = "2020 Fall Term"
subject = "Mathematics"
career = "Undergraduate"
email = "your_email@gmail.com"
last_name = ""
class_number = "36715"
delay = 15
counter = 20
while(counter > 0):
    counter -= 1
    checker = CunyGlobalChecker("headless")
    availability = checker.check_class(school, term, subject, career, last_name, class_number, delay)

    if availability:

        gmail.send_email(email, "Class '{}' is available for register.".format(class_number))
        enroller = CunyFirstEnroller.CunyFirstEnroller()
        enroller.login("cunyfirst_username", "cunyfirst_password")
        enroller.enroll_cart(term)
        enroller.quit()
        checker.quit()

        break

    else:
        gmail.send_email('your_email@gmail.com', "Something Went Wrong With Your Program!     " + class_number + " " + str(counter))
        print("Something Went Wrong With Your Program!     " + class_number + " " + str(counter))
        checker.quit()