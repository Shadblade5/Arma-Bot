from bot.cocparser import PrepareCoCPost


def test_cocfile_load(coc_test_data):
    assert 'header' in coc_test_data.__dict__.keys()
    assert 'sections' in coc_test_data.__dict__.keys()


def test_coc_prepare_post(coc_test_data):
    prepared_posts = PrepareCoCPost(coc_test_data)

    assert 'preamble' in prepared_posts.keys()
    assert 'sections' in prepared_posts.keys()

    assert prepared_posts['preamble']['title'] == 'PREAMBLE'
    assert len(prepared_posts['preamble']['headerposts']) == 3

    assert len(prepared_posts['sections']) == 1
