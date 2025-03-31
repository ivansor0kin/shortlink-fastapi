from app.utils import generate_short_code
import string

def test_generate_short_code():
    code = generate_short_code()
    assert len(code) == 6
    assert all(c in string.ascii_letters + string.digits for c in code)