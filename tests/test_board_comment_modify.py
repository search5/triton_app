from bs4 import BeautifulSoup


def test_guest_comment_modify_input(client):
    """손님 상태에서 게시물 댓글 수정 창 확인"""
    req_http = client.get('/board/107')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 폼 가져오기
    form_elem = response_parser.select_one('form.modify_form_comment')
    assert form_elem != None, 'form 태그가 없습니다'

    # 작성자
    input_writer = form_elem.select_one("input[type=text][name=writer]")
    assert input_writer != None, '작성자 입력란이 없습니다'
    if input_writer.has_attr('value'):
        assert input_writer['value'] == '', '작성자 입력안에 내용이 있으면 안됩니다'

    # 비밀번호
    input_password = form_elem.select_one("input[type=password][name=password]")
    assert input_password != None, '비밀번호 입력란이 없습니다'
    if input_password.has_attr('value'):
        assert input_password['value'] == '', '비밀번호 입력안에 내용이 있으면 안됩니다'

    # 내용
    text_content = form_elem.select_one("textarea[name=content]")
    assert text_content != None, '내용 입력란이 없습니다'
    assert ''.join(text_content.contents) == '', '내용 입력안에 내용이 있으면 안됩니다'
    
    is_save_button = form_elem.select('.btn.save')

    # 버튼 표시 및 게시물 수정 링크 확인
    assert len(is_save_button) == 1, '댓글 저장 버튼이 없습니다'


def test_logined_comment_modify_input(client_user):
    """로그인 상태에서 게시물 댓글 수정 창 확인"""
    req_http = client_user.get('/board/107')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 폼 가져오기
    form_elem = response_parser.select_one('form.modify_form_comment')
    assert form_elem != None, 'form 태그가 없습니다'

    # 내용
    text_content = form_elem.select_one("textarea[name=content]")
    assert text_content != None, '내용 입력란이 없습니다'
    assert ''.join(text_content.contents) == '', '내용 입력안에 내용이 있으면 안됩니다'
    
    is_save_button = form_elem.select('.btn.save')

    # 버튼 표시 및 게시물 수정 링크 확인
    assert len(is_save_button) == 1, '댓글 저장 버튼이 없습니다'


def test_guest_comment_modify(client):
    """손님 상태에서 댓글 편집 후 저장 기능 테스트"""

    req_http = client.put('/board/107/comments/5', json={
        "content": "손님 상태에서 댓글 내용 수정",
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'


def test_logined_comment_modify(client_user):
    """로그인된 상태에서 댓글 편집 후 저장 기능 테스트"""

    req_http = client_user.put('/board/107/comments/6', json={
        "content": "로그인 상태에서 댓글 내용 수정"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'