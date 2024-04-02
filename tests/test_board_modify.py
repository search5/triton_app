from bs4 import BeautifulSoup


def test_board_modify_view(client):
    req_http = client.get('/board/107/modify')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 폼 가져오기
    form_elem = response_parser.select_one('form')
    assert form_elem != None, 'form 태그가 없습니다'
    assert form_elem.has_attr('method'), 'method 속성이 없습니다'
    assert form_elem['method'].lower() == 'post', 'method 속성의 값이 post가 아닙니다'

    # 제목
    input_subject = form_elem.select_one("input[type=text][name=subject]")
    assert input_subject != None, '제목 입력란이 없습니다'
    assert input_subject.has_attr('value'), 'value 속성이 없습니다'
    assert input_subject['value'].strip() != '', '제목 입력란에 내용이 없습니다'

    # 비밀번호
    input_password = form_elem.select_one("input[type=password][name=password]")
    assert input_password != None, '비밀번호 입력란이 없습니다'
    assert input_password['value'].strip() == '', '비밀번호은 입력되어 있으면 안됩니다'

    # 내용
    text_content = form_elem.select_one("textarea[name=content]")
    assert text_content != None, '내용 입력란이 없습니다'
    assert ''.join(text_content.contents) != '', '내용 입력안에 내용이 없습니다'

    # 게시물 저장 버튼 여부 확인
    save_button = form_elem.select_one('.btn.save')
    assert save_button != None, '게시물 저장 버튼이 없습니다.'


def test_board_modify_save(client):
    """게시물 저장 기능 테스트"""

    req_http = client.post('/board/107/modify', data={
        "subject": "게시물 제목 수정",
        "content": "게시물 내용 수정",
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()


def test_board_modify_login_save(client_user):
    """로그인 중인 사용자의 게시물 저장 기능 테스트"""

    # 로그인한 사용자로 게시물 추가
    req_http = client_user.post('/board/write', data={
        "subject": "로그인한 사용자가 작성한 게시물 제목",
        "content": "로그인한 사용자가 작성한 게시물 내용"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'
    
    req_json = req_http.get_json()

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_json

    article_id = req_json.get('article_id')

    req_http = client_user.post(f'/board/{article_id}/modify', data={
        "subject": "게시물 제목 수정",
        "content": "게시물 내용 수정"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()
