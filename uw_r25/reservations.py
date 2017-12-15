from uw_r25.models import Reservation
from uw_r25 import nsmap, get_resource
from uw_r25.spaces import space_reservation_from_xml
try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode


def get_reservation_by_id(reservation_id):
    url = "reservation.xml?rsrv_id=%s" % reservation_id
    return reservations_from_xml(get_resource(url))[0]


def get_reservations(**kwargs):
    """
    Return a list of reservations matching the passed filter.
    Supported kwargs are listed at
    http://knowledge25.collegenet.com/display/WSW/reservations.xml
    """
    kwargs["scope"] = "extended"
    url = "reservations.xml"
    if len(kwargs):
        url += "?%s" % urlencode(kwargs)

    return reservations_from_xml(get_resource(url))


def reservations_from_xml(tree):
    try:
        profile_name = tree.xpath("r25:profile_name", namespaces=nsmap)[0].text
    except:
        profile_name = None

    reservations = []
    for node in tree.xpath("r25:reservation", namespaces=nsmap):
        reservation = Reservation()
        reservation.reservation_id = node.xpath("r25:reservation_id",
                                                namespaces=nsmap)[0].text
        reservation.start_datetime = node.xpath("r25:reservation_start_dt",
                                                namespaces=nsmap)[0].text
        reservation.end_datetime = node.xpath("r25:reservation_end_dt",
                                              namespaces=nsmap)[0].text
        reservation.state = node.xpath("r25:reservation_state",
                                       namespaces=nsmap)[0].text
        if profile_name:
            reservation.profile_name = profile_name
        else:
            reservation.profile_name = node.xpath("r25:profile_name",
                                                  namespaces=nsmap)[0].text

        try:
            pnode = node.xpath("r25:space_reservation", namespaces=nsmap)[0]
            reservation.space_reservation = space_reservation_from_xml(pnode)
        except IndexError:
            reservation.space_reservation = None

        try:
            enode = node.xpath("r25:event", namespaces=nsmap)[0]
            reservation.event_id = enode.xpath("r25:event_id",
                                               namespaces=nsmap)[0].text
            reservation.event_name = enode.xpath("r25:event_name",
                                                 namespaces=nsmap)[0].text

            rnode = enode.xpath("r25:role", namespaces=nsmap)[0]
            cnode = rnode.xpath("r25:contact", namespaces=nsmap)[0]
            reservation.contact_name = cnode.xpath("r25:contact_name",
                                                   namespaces=nsmap)[0].text
            try:
                anode = cnode.xpath("r25:address", namespaces=nsmap)[0]
                reservation.contact_email = anode.xpath(
                    "r25:email", namespaces=nsmap)[0].text
            except IndexError:
                reservation.contact_email = None

        except IndexError:
            enode = tree.getparent()
            reservation.event_id = enode.xpath("r25:event_id",
                                               namespaces=nsmap)[0].text
            reservation.event_name = enode.xpath("r25:event_name",
                                                 namespaces=nsmap)[0].text

        reservations.append(reservation)

    return reservations
