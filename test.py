from flask import request
from flask import Flask

app = Flask(__name__)

@app.post('/login')
def login():
    username = request.form.get('account')  # 获取POST请求中的username参数
    password = request.form.get('password')  # 获取POST请求中的password参数
    identityFlag =  request.form.get('identityFlag')
    print(username,password,identityFlag,type(identityFlag))

    # 进行身份验证逻辑，比如验证用户名密码是否匹配数据库中的记录
    if identityFlag == "True":
        if username == 'student' and password == '111111':
            return 'True'
        else:
            return 'False'
    else:
        if username == 'admin' and password == '111111':
            return 'True'
        else:
            return 'False'

if __name__ == '__main__':
    pass