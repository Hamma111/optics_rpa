def mutate_optical_pia_order(order):
    order.material_type = order.material_type.lower()

    order.sphere_r = "+" + order.sphere_r if order.sphere_r[0] != "-" and order.sphere_r != "0" else order.sphere_r
    order.sphere_l = "+" + order.sphere_l if order.sphere_l[0] != "-" and order.sphere_l != "0" else order.sphere_l

    order.cylinder_r = "+" + order.cylinder_r if order.cylinder_r[0] != "-" and order.cylinder_r != "0" else order.cylinder_r
    order.cylinder_l = "+" + order.cylinder_l if order.cylinder_l[0] != "-" and order.cylinder_l != "0" else order.cylinder_l

    order.sphere_r = order.sphere_r.ljust(2, ".") if order.sphere_r == "0" else order.sphere_r.ljust(3, ".")
    order.sphere_l = order.sphere_l.ljust(2, ".") if order.sphere_l == "0" else order.sphere_l.ljust(3, ".")

    order.cylinder_r = order.cylinder_r.ljust(2, ".") if order.cylinder_r == "0" else order.cylinder_r.ljust(3, ".")
    order.cylinder_l = order.cylinder_l.ljust(2, ".") if order.cylinder_l == "0" else order.cylinder_l.ljust(3, ".")

    order.sphere_r = order.sphere_r.ljust(5, "0")
    order.sphere_l = order.sphere_l.ljust(5, "0")

    order.cylinder_r = order.cylinder_r.ljust(5, "0")
    order.cylinder_l = order.cylinder_l.ljust(5, "0")

    return order
