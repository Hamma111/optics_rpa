import json


def mutate_optical_pia_order(order):
    order.material_type = order.material_type.lower()

    order.sphere_r = "+" + order.sphere_r if order.sphere_r[0] != "-" and order.sphere_r != "0" else order.sphere_r
    order.sphere_l = "+" + order.sphere_l if order.sphere_l[0] != "-" and order.sphere_l != "0" else order.sphere_l

    order.cylinder_r = "+" + order.cylinder_r if order.cylinder_r[
                                                     0] != "-" and order.cylinder_r != "0" else order.cylinder_r
    order.cylinder_l = "+" + order.cylinder_l if order.cylinder_l[
                                                     0] != "-" and order.cylinder_l != "0" else order.cylinder_l

    order.sphere_r = order.sphere_r.ljust(2, ".") if order.sphere_r == "0" else order.sphere_r.ljust(3, ".")
    order.sphere_l = order.sphere_l.ljust(2, ".") if order.sphere_l == "0" else order.sphere_l.ljust(3, ".")

    order.cylinder_r = order.cylinder_r.ljust(2, ".") if order.cylinder_r == "0" else order.cylinder_r.ljust(3, ".")
    order.cylinder_l = order.cylinder_l.ljust(2, ".") if order.cylinder_l == "0" else order.cylinder_l.ljust(3, ".")

    order.sphere_r = order.sphere_r.ljust(5, "0")
    order.sphere_l = order.sphere_l.ljust(5, "0")

    order.cylinder_r = order.cylinder_r.ljust(5, "0")
    order.cylinder_l = order.cylinder_l.ljust(5, "0")

    return order


def send_cdp_command(driver, cmd, params):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')
