from bs4 import BeautifulSoup


def test_board_list_zero(client):
    """글 개수가 0개이거나 0개 이상이면 유효한 것으로 점검한다."""
    req_http = client.get('/board')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # HTTP 게시물 목록 응답(HTML)
    article_table = response_parser.select_one("table.table.board_list")
    
    article_list = article_table.select("tbody>tr")
    
    if article_list:
        assert len(article_list), '아직 게시물이 없습니다'
    else:
        # 글 개수가 0개면 성공, 0개 이상이면 실패
        assert not len(article_list), '게시물이 존재합니다'

    add_button = response_parser.select_one('.btn.add')
    assert bool(add_button), '게시물 추가 버튼이 없습니다'
    assert add_button['href'] == "/board/write", '정상적인 게시물 추가 링크가 아닙니다'


def test_board_list_many(client):
    req_http = client.get('/board')

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    response_content = req_http.get_data()

    response_parser = BeautifulSoup(response_content, 'lxml')

    # HTTP 게시물 목록 응답(HTML) 확인
    article_table = response_parser.select_one("table.table.board_list")
    
    article_list = article_table.select("tbody>tr")
    
    # 글 개수가 0개 이상이면 성공, 0개면 실패
    assert len(article_list) > 0

    # 게시물 목록이 모든 셀이 빠짐없이 채워졌는지 확인(하나라도 비어있으면 오류)
    all_rows = []
    for row in article_list:
        all_td = row.select("td")
        article_view_link = all_td[1].select_one("a")
        if not article_view_link:
            all_rows.append(False)
            continue
        else:
            if article_view_link['href'] != f'/board/{all_td[0].text}':
                all_rows.append(False)
                continue
        all_rows.append(all(map(lambda x: x.text, all_td)))
    
    assert [True] * len(article_list) == all_rows, '게시물 행의 모든 셀 및 게시물 제목에 링크가 걸려있어야 합니다.'

    # 게시물 목록 페이징 응답(HTML) 확인
    pagination_link = response_parser.select("ul.pagination>li>a")
    
    assert len(pagination_link) > 0, '페이징 기능이 구현되지 않았습니다'

    add_button = response_parser.select_one('.btn.add')
    assert bool(add_button), '게시물 추가 버튼이 없습니다'
    assert add_button['href'] == "/board/write", '정상적인 게시물 추가 링크가 아닙니다'
