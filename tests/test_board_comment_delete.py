def test_guest_comment_delete(client, write_comment):
    """손님 상태에서 게시물 댓글 삭제 기능 확인"""
    article_id = write_comment.get("article_id")
    comment_id = write_comment.get("comment_id")

    req_http = client.delete(
        f'/board/{article_id}/comments/{comment_id}',
        json={
            "password": "1234"
        }
    )

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()


def test_logined_comment_delete(client_user, write_comment_loggined):
    """로그인 상태에서 게시물 댓글 삭제 기능 확인"""
    article_id = write_comment_loggined.get("article_id")
    comment_id = write_comment_loggined.get("comment_id")

    req_http = client_user.delete(f'/board/{article_id}/comments/{comment_id}')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()
