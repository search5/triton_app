def test_guest_comment_list(client):
    """게시물 댓글 목록 확인"""
    req_http = client.get('/board/107/comments')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_json()

    # 댓글 목록 응답 검사
    assert response_content['success'], '게시물 댓글 목록을 가져오는데 실패했습니다'
    
    # 댓글 목록 검사
    assert 'data' in response_content, '게시물 댓글 목록이 없습니다'

    # 댓글 목록을 반복하면서 내용 확인
    for item in response_content['data']:
        assert item['writer_name'], '작성자명이 없습니다'
        assert item['content'], '댓글 내용이 없습니다'
