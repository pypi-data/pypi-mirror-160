
from cgi import test
import pandapipes.multinet.control as ppmc

import peext.scenario.network as ps

def test_convergence_coupled_district_network():
    multinet = ps.create_super_district_coupled_network(0.7)

    #pandapipes error makes this test impossible right now
    #ppmc.run_control_multinet.run_control(multinet, max_iter = 30, mode='all')


if __name__ == '__main__':
    test_convergence_coupled_district_network()