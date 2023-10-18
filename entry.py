import time
import yaml
from pathlib import Path
from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.print_page_options import PrintOptions

import os
import base64
from ocr import translate_captcha
from headshot_resize import resize_image
from build_yaml_old import build_yaml
from whatsapp_yaml import build_whatsapp_yaml
from time_countdown import countdown_timer



def store_pdf(pdf_base, person, pdf_type):
    pdf_data = base64.b64decode(pdf_base)
    # Specify the directory where you want to save the PDF
    download_directory = str(Path.cwd() / "submitted_apps/")
    # Specify the desired filename for the PDF
    pdf_filename = f"{person['first_name']}_{person['last_name']}_{pdf_type}.pdf"
    # Combine the directory and filename to create the complete file path
    pdf_file_path = os.path.join(download_directory, pdf_filename)
    # Write the decoded PDF data to a file
    with open(pdf_file_path, "wb") as pdf_file:
        pdf_file.write(pdf_data)


def read_yaml(full_name):
    with open(f'data/yaml_forms/{full_name}.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def gen_driver():
    svc = webdriver.ChromeService(executable_path=binary_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=svc, options=options)
    url = 'https://dvprogram.state.gov/application.aspx'
    driver.get(url)
    return driver


def pass_captcha(driver):
    captcha_element = driver.find_element(By.ID, "c_application_contentplaceholder1_uccaptcha_CaptchaImage")
    captcha_image = captcha_element.screenshot_as_png
    with open('captcha.png', 'wb') as img_file:
        img_file.write(captcha_image)
    time.sleep(1)
    text = translate_captcha('captcha.png')
    print(f"captcha image with text of: {text['code']} was detected and passed")
    
    captcha_input = driver.find_element(By.ID, "ContentPlaceHolder1_txtCodeInput")
    captcha_input.clear()
    captcha_input.send_keys(text['code'])
    time.sleep(1)
    
    driver.find_element(By.ID, "ContentPlaceHolder1_btnSubmit").click()
    time.sleep(1)
    try:
        driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl0_txtLastName")
    except:
        time.sleep(5)
        pass_captcha(driver)
    

def input_personal_info(driver, person):
    last_name = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl0_txtLastName")
    first_name = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl0_txtFirstName")
    no_mid_name = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl0_cbxMiddleName")
    last_name.send_keys(person["last_name"])
    first_name.send_keys(person["first_name"])
    no_mid_name.click()
    select_gender(driver, person)
    bday_month = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl2_txtMonthOfBirth")
    bday_day = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl2_txtDayOfBirth")
    bday_year = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl2_txtYearOfBirth")
    bday_month.send_keys(person["bday_month"])
    bday_day.send_keys(person["bday_day"])
    bday_year.send_keys(person["bday_year"])
    city_born = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl3_txtBirthCity")
    city_born.send_keys(person["city_born"])
    country_born_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl4_drpBirthCountry"))
    country_born_dropdown.select_by_visible_text(person['country_born'])
    upload_pic(driver, person)
    time.sleep(2)
    address_1 = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl7_txtAddress1")
    address_city = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl7_txtCity")
    address_provice = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl7_txtDistrict")
    address_country_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl7_drpMailingCountry"))
    live_today_country_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl8_drpCountry"))
    phone_number = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl9_txtPhoneNumber")
    email_address = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl10_txtEmailAddress")
    confirm_email = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl10_txtConfEmailAddress")
    address_1.clear()
    address_1.send_keys(person['address_1'])
    address_city.clear()
    address_city.send_keys(person['address_city'])
    address_provice.clear()
    address_provice.send_keys(person['province'])
    check_zipcode(driver, person)
    address_country_dropdown.select_by_visible_text(person['country_mail_live'])
    live_today_country_dropdown.select_by_visible_text(person['country_mail_live'])
    phone_number.clear()
    phone_number.send_keys(person['phone'])
    email_address.clear()
    email_address.send_keys(person['email'])
    confirm_email.clear()
    confirm_email.send_keys(person['email'])
    select_highest_edu(driver, person)
    select_marital_status(driver, person)
    num_of_kids = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl13_txtNumChildren")
    num_of_kids.clear()
    num_of_kids.send_keys(person['num_kids'])
    time.sleep(1)
    driver.find_element(By.ID, "ContentPlaceHolder1_btnContinueP1").click()
    fill_out_spouce(driver, person)
    time.sleep(2)
    fill_kid_info(driver, person) #
    

def check_zipcode(driver, person):
    address_postal_code = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl7_txtZipCode")
    no_postal_check_box = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl7_cbxZipCode")
    if not person['no_zip_code']:
        address_postal_code.clear()
        address_postal_code.send_keys(person['zip_code'])
    else:
        no_postal_check_box.click()
    

def fill_out_spouce(driver, person):
    if person['marital_status'] not in  ["Unmarried", "Divorcecd"]:
        spouce_name = person['spouce_full_name'].lower()
        spouce_name = spouce_name.split(" ")
        
        spouce_file_name = f"{spouce_name[0]}_{spouce_name[1]}"
        
        try:
            spouce = build_yaml(spouce_file_name)
        except:
            spouce = build_whatsapp_yaml(spouce_file_name)
    
        driver.find_element(By.ID, 'ContentPlaceHolder1_formSpouse_qName_txtLastName').send_keys(spouce['last_name'])
        driver.find_element(By.ID, 'ContentPlaceHolder1_formSpouse_qName_txtFirstName').send_keys(spouce['first_name'])
        no_mid_name = driver.find_element(By.ID, "ContentPlaceHolder1_formSpouse_qName_cbxMiddleName")
        no_mid_name.click()
        
        # Find and fill out the Birth Date fields (Month, Day, Year)
        driver.find_element(By.ID, 'ContentPlaceHolder1_formSpouse_qBirthDate_txtMonthOfBirth').send_keys(spouce['bday_month'])
        driver.find_element(By.ID, 'ContentPlaceHolder1_formSpouse_qBirthDate_txtDayOfBirth').send_keys(spouce['bday_day'])
        driver.find_element(By.ID, 'ContentPlaceHolder1_formSpouse_qBirthDate_txtYearOfBirth').send_keys(spouce['bday_year'])
        
        
        select_spouce_gender(driver, spouce)
        # Find and fill out the City Where Spouse Was Born
        driver.find_element(By.ID, 'ContentPlaceHolder1_formSpouse_qBirthCity_txtBirthCity').send_keys(spouce['city_born'])
        country_spouce_born = Select(driver.find_element(By.ID, "ContentPlaceHolder1_formSpouse_qBirthCountry_drpBirthCountry"))
        country_spouce_born.select_by_visible_text("Iran")
        upload_pic(driver, spouce)
        time.sleep(2)
    else:
        pass


def upload_pic(driver, person):
    driver.implicitly_wait(1)  # Adjust the wait time as needed
    person_name = person['first_name'].capitalize()
    resize_image(person_name)
    headshot_path = Path.cwd() / f"data/imgs/{person_name}_.jpg"
    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input.send_keys(str(headshot_path))


def upload_kid_pic(driver, person):
    driver.implicitly_wait(1)  # Adjust the wait time as needed
    person_name = person['kid_first_name'].capitalize()
    resize_image(person_name)
    headshot_path = Path.cwd() / f"data/imgs/{person_name}_.jpg"
    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input.send_keys(str(headshot_path))
    
    
def select_gender(driver, person):
    if person["gender"]=="m":
        m_gender = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl1_rdoGenderM")
        m_gender.click()
    else:
        f_gender = driver.find_element(By.ID, "ContentPlaceHolder1_formApplicant__ctl1_rdoGenderF")
        f_gender.click()


def select_kid_gender(driver, person):
    if person["kid_gender"]=="m":
        m_gender = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qGender_rdoGenderM")
        m_gender.click()
    else:
        f_gender = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qGender_rdoGenderF")
        f_gender.click()
   
    
def select_spouce_gender(driver, person):
    if person["gender"]=="m":
        m_gender = driver.find_element(By.ID, "ContentPlaceHolder1_formSpouse_qGender_rdoGenderM")
        m_gender.click()
    else:
        f_gender = driver.find_element(By.ID, "ContentPlaceHolder1_formSpouse_qGender_rdoGenderF")
        f_gender.click()
    
    
def select_highest_edu(driver, person):
    radio_buttons = driver.find_elements(By.XPATH, "//table[@id='ContentPlaceHolder1_formApplicant__ctl11_rblEducation']//input[@type='radio']")
    for radio_button in radio_buttons:
        label_element = radio_button.find_element(By.XPATH, "./following-sibling::label")
        if label_element.text == person['education']:
            radio_button.click()
            break
    
    
    

def select_marital_status(driver, person):
    radio_buttons = driver.find_elements(By.XPATH, "//table[@id='_ctl0_ContentPlaceHolder1_formApplicant__ctl12_rblMarried']//input[@type='radio']")
    for radio_button in radio_buttons:
        label_element = radio_button.find_element(By.XPATH, "./following-sibling::label")
        if label_element.text == person['marital_status']:
            radio_button.click()
            break  # Exit the loop once a match is found


def review_app(driver, person):
    if person['marital_status'] not in ['Unmarried', 'Divorced'] or person['num_kids'] > 0: 
        time.sleep(2)
        driver.find_element(By.ID, "ContentPlaceHolder1_btnReview").click()
    else:
        pass
    print('!!!!!!!!!! REVIEW INFORMATION BEFORE BEING SUBMITTED!!!!!!!!!!!!')
    print_options = PrintOptions()
    print_options.page_ranges = ['1-3']
    base64code = driver.print_page(print_options)
    store_pdf(base64code, person, 'review_page')
    countdown_timer(60)
    print('Review Page Printed and Saved!!')
    
    
def submit_application(driver, person):
    print("Submitting Application")
    driver.find_element(By.ID, "ContentPlaceHolder1_btnContinueP2").click()
    time.sleep(2)
    print_options = PrintOptions()
    print_options.page_ranges = ['1-2']
    base64code = driver.print_page(print_options)
    store_pdf(base64code, person, 'submit' )
    print("Submission Page Printed and Saved!!")
    time.sleep(15)
    driver.quit()

    
def fill_kid_info(driver, person):
    if int(person['num_kids']) > 0:
        print("Filling out information regarding applicant's kid")
        last_name = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qName_txtLastName")
        first_name = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qName_txtFirstName")
        no_mid_name = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qName_cbxMiddleName")
        last_name.send_keys(person["kid_last_name"])
        first_name.send_keys(person["kid_first_name"])
        no_mid_name.click()
        select_kid_gender(driver, person)
        bday_month = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qBirthDate_txtMonthOfBirth")
        bday_day = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qBirthDate_txtDayOfBirth")
        bday_year = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qBirthDate_txtYearOfBirth")
        bday_month.send_keys(person["kid_month"])
        bday_day.send_keys(person["kid_day"])
        bday_year.send_keys(person["kid_year"])
        city_born = driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qBirthCity_txtBirthCity")
        city_born.send_keys(person["kid_city_born"])
        country_born_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_formChild01_qBirthCountry_drpBirthCountry"))
        country_born_dropdown.select_by_visible_text(person['country_born'])
        upload_kid_pic(driver, person)

 
    
import sys
if __name__=="__main__":
    person_name = sys.argv[1]
    try:
        person = build_yaml(person_name)
    except:
        person = build_whatsapp_yaml(person_name)
    driver = gen_driver()
    pass_captcha(driver)
    time.sleep(1)
    input_personal_info(driver, person)
    review_app(driver, person)
    submit_application(driver, person)
    driver.quit()
    