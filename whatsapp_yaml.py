
import yaml


def read_yaml(full_name):
    with open(f'data/yaml_forms/{full_name}.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


def build_whatsapp_yaml(person):
    
    try:
        person_file = read_yaml(person)
    except FileNotFoundError:
        with open(f'data/forms/{person}.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        
        
        # Split the text into lines
        lines = text.strip().split('\n')
        # Initialize a dictionary to store key-value pairs
        data = {}
        # Iterate through lines and extract key-value pairs
        for line in lines:
            parts = line.split(' : ')
            if len(parts) == 2:
                key, value = parts
                data[key.strip()] = value.strip()
        
        

        # Convert data to the desired format
        yaml_data = {
            'address_1': data['آدرس محل زندگی به انگلیسی'],
            'address_city': data['شهر محل زندگی به انگلیسی'],
            'bday_day': int(data['روز تولد میلادی به انگلیسی']),
            'bday_month': int(data['ماه تولد میلادی'][-2:]),
            'bday_year': int(data['سال تولد به انگلیسی ۴ رقم']),
            'city_born': data['شهر تولد به انگلیسی'],
            'country_born': data['کشور تولد به انگلیسی'].title(),
            'country_mail_live': data['کشور محل زندگی به انگلیسی'].title(),
            'education': data['تحصیلات (حداقل دیپلم لازم میباشد)'],
            'email': data['آدرس ایمیل معتبر'],
            'first_name': data['نام به انگلیسی'],
            'gender': data['جنسیت'],
            'last_name': data['فامیل به انگلیسی'],
            'no_zip_code': False,  # Assuming no zip code is provided
            'num_kids': int(data['تعداد فرزند زیر ۱۸ سال (اگر ندارید 0)']),
            'phone': data['تلفن همراه (با کد ایران شروع شود) به انگلیسی'],
            'province': data['استان محل زندگی به انگلیسی'],
            
            'zip_code': data['کد پستی محل زندگی به انگلیسی']
        }
        
        
        if data['وضعیت تاهل'] == 'مجرد':
            m_stat = 'Unmarried'
        elif data['وضعیت تاهل'] == 'متاهل':
            m_stat = "Married and my spouse is NOT a U.S.citizen or U.S. Lawful Permanent Resident (LPR)"
            yaml_data['spouce_full_name'] = data['نام و فامیل همسر به انگلیسی(اگر ندارید خالی)']
        else:
            m_stat = "Divorced"
            
        yaml_data['marital_status'] = m_stat
        
        
        if yaml_data['num_kids'] == 1:
            yaml_data["kid_first_name"] = data["نام فرزند به اینگلیسی"]
            yaml_data["kid_last_name"] = data["فامیل فرزند به اینگلیسی"]
            yaml_data["kid_day"] = data["روز تولد میلادی فرزند به اینگلیسی"]
            yaml_data["kid_month"] =int(data["ماه تولد میلادی  فرزند"][-2:])
            yaml_data["kid_year"] = data["سال تولد میلادی فرزند به اینگلیسی"]
            yaml_data["kid_gender"] = data["جنسیت فرزند"]
            yaml_data["kid_city_born"] = data["شهر تولد فرزند به انگلیسی"]
        elif yaml_data['num_kids'] > 1:
            print("Applicant has more than one kid")

        # Write the YAML data to a file
        full_name = data['نام به انگلیسی'].lower() + "_" + data['فامیل به انگلیسی'].lower()
        with open(f'data/yaml_forms/{full_name}.yaml', 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=True, allow_unicode=True)
        person_file = read_yaml(full_name)
            
    return person_file


if __name__=="__main__":
    import sys
    build_whatsapp_yaml(sys.argv[1])