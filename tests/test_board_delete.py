def test_board_delete(client):
    """게시물 삭제 기능 테스트"""

    req_http = client.delete('/board/3/delete', data={
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()


def test_board_login_delete(client_user):
    """로그인 중인 사용자의 게시물 삭제 기능 테스트"""

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

    req_http = client_user.delete(f'/board/{article_id}/delete')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()
