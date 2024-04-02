from bs4 import BeautifulSoup


def test_guest_comment_delete_input(client):
    """게시물 댓글 삭제 버튼이 있는지 확인"""
    req_http = client.get('/board/107')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 댓글 삭제 버튼 확인
    comment_delete_btn = response_parser.select_one("btn.btn-danger.comment_delete")
    assert comment_delete_btn != None, '코멘트 삭제 버튼이 없습니다'


def test_guest_comment_delete(client):
    """손님 상태에서 게시물 댓글 삭제 기능 확인"""
    req_http = client.post('/board/107/comments', data={
        "content": "손님 상태에서 댓글 작성",
        "writer_name": "코멘트 작성자",
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '302 FOUND', 'URL이 구현되지 않았습니다'

    comment_id = req_http.headers.get('x-comment_id')

    req_http = client.delete(f'/board/107/commnents/{comment_id}', data={
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()


def test_logined_comment_delete(client_user):
    """로그인 상태에서 게시물 댓글 삭제 기능 확인"""
    # 로그인한 사용자로 댓글 추가
    req_http = client_user.post('/board/107/comments', data={
        "content": "로그인한 사용자로 댓글 추가"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '302 FOUND', 'URL이 구현되지 않았습니다'

    comment_id = req_http.headers.get('x-comment_id')

    req_http = client_user.delete(f'/board/107/comments/{comment_id}')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()
