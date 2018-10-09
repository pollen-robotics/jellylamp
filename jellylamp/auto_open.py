from pypot.dynamixel import Dxl320IO, get_available_ports


def find_port_for_ids(ports, ids):
    for p in ports:
        with Dxl320IO(port=p) as io:
            if set(ids) == set(io.scan(ids)):
                return p

    raise IOError('Could not find a port for {}!'.format(ids))


def auto_open_ios(ids_groups):
    available_ports = get_available_ports()

    ios = {}
    for ids in ids_groups:
        port = find_port_for_ids(available_ports, ids)
        print('Found port {} for {}.'.format(port, ids))

        io = Dxl320IO(port=port)
        ios[tuple(ids)] = io

        available_ports.remove(port)

    return ios
