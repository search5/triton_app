from bs4 import BeautifulSoup


def test_guest_comment_delete_input(client, write_comment):
    """게시물 댓글 삭제 버튼이 있는지 확인"""
    article_id = write_comment.get("article_id")

    req_http = client.get(f'/board/{article_id}')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 댓글 삭제 버튼 확인
    comment_delete_btn = response_parser.select_one("btn.btn-danger.comment_delete")
    assert comment_delete_btn is not None, '코멘트 삭제 버튼이 없습니다'


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
