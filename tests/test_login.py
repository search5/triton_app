from bs4 import BeautifulSoup


def test_login_view(client):
    """로그인 화면 테스트"""
    req_http = client.get('/board/login')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 로그인 form
    form = response_parser.select_one("form[method=post]")
    assert form != '', '로그인 FORM이 없습니다'

    # 로그인 ID
    input_id = form.select_one("input[name=login_id][type=text]")
    assert input_id != '', '로그인 ID 입력 칸이 없습니다'

    # 로그인 비밀번호
    input_passwd = form.select_one("input[name=login_pass][type=password]")
    assert input_passwd != '', '로그인 비밀번호 입력 칸이 없습니다'

    # 로그인 버튼
    btn_login = form.select_one("button.btn.btn-primary[type=submit]")
    assert btn_login != '', '로그인 버튼이 없습니다'


def test_login_proc(client):
    """로그인 기능 테스트"""
    with client:
        req_http = client.post('/board/login', data={
            'login_id': 'admin',
            'login_pass': '1234'
        })
        assert req_http.status == '302 FOUND', '로그인에 실패했습니다'
