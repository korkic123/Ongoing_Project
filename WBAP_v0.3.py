# Whale Browser Artifact Parser / Ver 0.3
# Created By Korkic

# Version 0.3 :
# 1. Scan all drives for artifacts

# Version 0.2 :
# 1. Convert Chrome Time to KST
# 2. Add Columns of Browser, Action and Search Keyword

# Version 0.1 :
# 1. It's NOT Complete Parser Yet. Only mapping and exporting the 'History' DB are possible...



import os
import win32api
import sqlite3
import datetime

def search_users(dir) :
# This function is to search the Whale Browser folder in the path
# 
    gwf_list = []
    files = os.listdir(dir)

    # Whether there is 'Whale Browser' folder in 'dir' path's folders or not.
    # if there is it, return this User's path.
    for file in files:
        if os.path.isdir(os.path.join(dir, file)) :
            if os.path.exists(os.path.join(dir, file, "AppData\\Local\\Naver\\Naver Whale\\User Data\\Default")) :
                gwf_list.append(os.path.join(dir, file))

    return gwf_list


def convert_ct_2_kst(timestamp):
# This function is to convert Google Chrome Time to KST(Korean Standard Time; GMT+9)

    epoch_time = datetime.datetime(1601,1,1)
    passing_time = datetime.timedelta(microseconds=int(timestamp))
    kst = datetime.timedelta(hours=9)

    # return to convert to KST
    return epoch_time + passing_time + kst


def analyze_db(lt) :
# This function is to make CSV file
# Export path : %USERPROFILE%\Desktop\<username>_WBAP_Result.csv

    user = lt.replace(lt[:9],"")

    print(user + "의 History 파일을 분석합니다.")

    # Add column's names.
    temp = "연 번,마지막 방문시간,브라우저,행 위,검색어,URL,제 목,방문 횟수\n"
    count = 0

    # Whether there is History DB.
    if os.path.exists(lt + "\\AppData\\Local\\Naver\\Naver Whale\\User Data\\Default\\History") :
        db = lt + "\\AppData\\Local\\Naver\\Naver Whale\\User Data\\Default\\History"

        # connect to DB
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur2 = conn.cursor()

        # DB data allocates to each column.
        # execute 'urls' Table.
        for row in cur.execute("select id, last_visit_time, url, title, visit_count from urls order by last_visit_time asc") :
        
            # count = 연번
            count += 1
            temp += str(count) + ","
            data_flag = 0

            for m in range(1, 5) :
                if m == 1 :
                    temp += str(convert_ct_2_kst(row[m])) + ","
                    temp += "Naver Whale Browser,"

                    # execute 'keyword_search_terms' Table.
                    # this table include searching data.
                    for row2 in cur2.execute("select url_id, term from keyword_search_terms") :
                        if row[0] == row2[0] :
                            temp += "검색," + row2[1] + ","
                            data_flag = 1
                    if data_flag == 0 :
                        temp += ",,"
                else :
                    temp += str(row[m]) + ","
            temp += "\n"

        cur.close()
        cur2.close()

    f = open(os.environ["USERPROFILE"] + "\\Desktop\\" + user + "_WBAP_Result.csv", "w")
    f.write(temp)
    f.close

os.system("cls")

print("Naver Whale Browser Artifact Parser")
print("Version 0.3")
print("Created By Korkic")
print()
print()

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
wf_list=[]

for i in range(0, len(drives)) :
    if os.path.isdir(drives[i] + "Users\\") :
        wf_list += search_users(drives[i] + "Users\\")

if len(wf_list) != 0 :
    print("다음 폴더에서 Naver Whale Browser Artifact가 확인되었습니다.")
    for a in range(0, len(wf_list)) :
        print(wf_list[a])

    print()
    print("진행사항 :")
    for a in range(0, len(wf_list)) :
        analyze_db(wf_list[a])

    print()
    print("분석이 완료되었습니다.")

else :
    print("Naver Whale Browser Artifact가 확인되지 않습니다.")
