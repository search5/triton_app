from bs4 import BeautifulSoup


def test_board_view(client):
    """게시물 상세 조회 시 모든 정보가 정상적으로 보이는지 확인한다
    점검 대상 정보: 게시물 제목, 게시물 작성자명, 게시물 작성일, 게시물 내용, 게시물 조회 수
        - 게시물 수정 버튼
        - 게시물 삭제 버튼
    """
    req_http = client.get('/board/107')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # 게시물 제목
    article_subject = response_parser.select_one("td.subject")
    assert article_subject.text != '', '게시물 제목이 없습니다'

    # 게시물 작성자명
    article_writer_name = response_parser.select_one("td.writer_name")
    assert article_writer_name.text != '', '게시물 작성자명이 없습니다'
    
    # 게시물 작성일
    article_write_date = response_parser.select_one("td.write_date")
    assert article_write_date.text != '', '게시물 작성일이 없습니다'

    # 게시물 내용
    article_content = response_parser.select_one("td.content")
    assert article_content.text != '', '게시물 내용이 없습니다'

    # 게시물 조회 수
    article_hit = response_parser.select_one("td.hit")
    assert article_hit.text != '', '게시물 조회 수가 없습니다'
    assert article_hit.text.isdigit() == True, '게시물 조회 수는 숫자여야 합니다'
    
    is_modify_button = response_parser.select('.btn.modify')
    is_delete_button = response_parser.select('.btn.delete')

    # 버튼 표시 및 게시물 수정 링크 확인
    assert len(is_modify_button) == 1, '게시물 수정 버튼이 없습니다'
    assert len(is_delete_button) == 1, '게시물 삭제 버튼이 없습니다'
    assert is_modify_button[0]['href'] == '/board/107/modify', '게시물 수정 링크가 올바르지 않습니다'


def test_not_found_view(client):
    """잘못된 게시물 번호를 호출해서 404 응답이 오는지 확인한다"""
    req_http = client.get('/board/88888')
    
    assert req_http.status == '404 NOT FOUND', '게시물이 존재합니다.'
