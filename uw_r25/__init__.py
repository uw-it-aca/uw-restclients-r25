from uw_r25.dao import R25_DAO
from restclients_core.exceptions import DataFailureException
from lxml import etree


nsmap = {"r25": "http://www.collegenet.com/r25",
         "xhtml": "http://www.w3.org/1999/xhtml"}


def get_resource(url):
    """
    Issue a GET request to R25 with the given url
    and return a response as an etree element.
    """

    instance = R25_DAO().get_service_setting('INSTANCE')
    if instance is not None:
        url = "/r25ws/wrd/%s/run/%s" % (instance, url)
    else:
        url = "/r25ws/servlet/wrd/run/%s" % url

    response = R25_DAO().getURL(url, {"Accept": "text/xml"})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    tree = etree.fromstring(response.data.strip())

    # XHTML response is an error response
    xhtml = tree.xpath("//xhtml:html", namespaces=nsmap)
    if len(xhtml):
        raise DataFailureException(url, 500, response.data)

    return tree
