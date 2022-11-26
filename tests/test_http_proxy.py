from http_proxy import __version__


def test_version():
    assert __version__ == '0.1.0'

# TODO: Create unit test testing no URL Sent
# Empty query: "http://127.0.0.1:8000/v2/urlinfo/"
# Returns:
# detail	
# 0	
#     loc	
#         0	"query"
#         1	"resource_url_with_query_string"
#     msg	"field required"
#     type	"value_error.missing"

# TODO: Test the use of a response model by outputting more fields than responseModel

