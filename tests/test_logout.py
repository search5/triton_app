def test_logout_proc(client_user):
    """로그아웃 URL 테스트"""
    req_http = client_user.get('/board/logout')

    # HTTP 응답 상태 확인
    assert req_http.status == '302 FOUND', 'URL이 구현되지 않았습니다'
