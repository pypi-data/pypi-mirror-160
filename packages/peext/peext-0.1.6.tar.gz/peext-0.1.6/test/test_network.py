from peext.scenario.network import create_small_test_multinet, create_super_district_coupled_network
import peext.network as network

import pandapipes

def test_from_pandapipes():
    # GIVEN
    test_network = create_small_test_multinet()

    # WHEN
    me_network = network.from_panda_multinet(test_network)

    # THEN
    assert len(me_network.nodes) == 11
    assert len(me_network.edges) == 9
    assert len(me_network.nodes[9].edges) == 3
    assert me_network.nodes[9].edges['power'][0][1] == 'to'
    assert me_network.nodes[9].edges['power'][0][0]._id == 1
    assert me_network.nodes[9].edges['gas'][0][1] == 'to'
    assert me_network.nodes[9].edges['gas'][0][0]._id == 1
    assert me_network.nodes[9].edges['heat'][0][1] == 'from'
    assert me_network.nodes[9].edges['heat'][0][0]._id == 0
    

def test_write_net():
    test_network = create_super_district_coupled_network(0.8)
    pandapipes.to_pickle(test_network, "coupled_district_network_with_p2h.p")


def test_load_net():
    mn = pandapipes.from_pickle("coupled_district_network_with_p2h.p")
    _ = network.from_panda_multinet(mn)
