from bs4 import BeautifulSoup


def test_guest_comment_write_input(client, write_article):
    """손님 상태에서 게시물 댓글 입력 창 확인"""
    article_id = write_article.get("article_id")

    req_http = client.get(f'/board/{article_id}')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 폼 가져오기
    form_elem = response_parser.select_one('form#form_comment')
    assert form_elem is not None, 'form 태그가 없습니다'
    assert form_elem.has_attr('method'), 'method 속성이 없습니다'

    # 작성자
    input_writer = form_elem.select_one("input[type=text][name=writer_name]")
    assert input_writer is not None, '작성자 입력란이 없습니다'
    if input_writer.has_attr('value'):
        assert input_writer['value'] == '', '작성자 입력안에 내용이 있으면 안됩니다'

    # 비밀번호
    input_password = form_elem.select_one("input[type=password][name=password]")
    assert input_password is not None, '비밀번호 입력란이 없습니다'
    if input_password.has_attr('value'):
        assert input_password['value'] == '', '비밀번호 입력안에 내용이 있으면 안됩니다'

    # 내용
    text_content = form_elem.select_one("textarea[name=content]")
    assert text_content is not None, '내용 입력란이 없습니다'
    assert ''.join(text_content.contents) == '', '내용 입력안에 내용이 있으면 안됩니다'
    
    is_save_button = form_elem.select('.btn.save')

    # 버튼 표시 및 게시물 수정 링크 확인
    assert len(is_save_button) == 1, '댓글 저장 버튼이 없습니다'


def test_logined_comment_write_input(client_user, write_article):
    """로그인 상태에서 게시물 댓글 입력 창 확인"""
    article_id = write_article.get("article_id")

    req_http = client_user.get(f'/board/{article_id}')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 폼 가져오기
    form_elem = response_parser.select_one('form#form_comment')
    assert form_elem is not None, 'form 태그가 없습니다'
    assert form_elem.has_attr('method'), 'method 속성이 없습니다'
    assert form_elem['method'].lower() == 'post', 'method 속성의 값이 post가 아닙니다'

    # 내용
    text_content = form_elem.select_one("textarea[name=content]")
    assert text_content is not None, '내용 입력란이 없습니다'
    assert ''.join(text_content.contents) == '', '내용 입력안에 내용이 있으면 안됩니다'
    
    is_save_button = form_elem.select('.btn.save')

    # 버튼 표시 및 게시물 수정 링크 확인
    assert len(is_save_button) == 1, '댓글 저장 버튼이 없습니다'


def test_guest_comment_write(client, write_article):
    """손님 상태에서 댓글 저장 기능 테스트"""
    article_id = write_article.get("article_id")

    req_http = client.post(f'/board/{article_id}/comments', data={
        "content": "손님 상태에서 댓글 내용",
        "writer_name": "코멘트 작성자",
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '302 FOUND', 'URL이 구현되지 않았습니다'


def test_logined_comment_write(client_user, write_article):
    """로그인된 상태에서 댓글 저장 기능 테스트"""
    article_id = write_article.get("article_id")

    req_http = client_user.post(
        f'/board/{article_id}/comments', data={
            "content": "로그인 상태에서 댓글 내용"
        }
    )

    # HTTP 응답 상태 확인
    assert req_http.status == '302 FOUND', 'URL이 구현되지 않았습니다'
