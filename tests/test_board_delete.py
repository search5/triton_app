def test_board_delete(client, write_article):
    """게시물 삭제 기능 테스트"""
    article_id = write_article.get('article_id')

    req_http = client.delete(f'/board/{article_id}/delete', data={
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()


def test_board_login_delete(client_user, write_loggined):
    """로그인 중인 사용자의 게시물 삭제 기능 테스트"""
    article_id = write_loggined.get('article_id')

    req_http = client_user.delete(f'/board/{article_id}/delete')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()
