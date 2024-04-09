import dbwork
import json
import IPO

#print("기업 개요입니다.\n")
#dbwork.get_comp_list(8)
#pprint.pprint(dbwork.companies)
#with open("data.json", "w", encoding="utf-8") as json_file:
#    json.dump(dbwork.companies, json_file, ensure_ascii=False, indent=4)
#print("json 파일이 생성되었습니다.")

print("공모 정보입니다.")
IPO.get_comp_list(1)
#IPO.get_detail_info(2044)