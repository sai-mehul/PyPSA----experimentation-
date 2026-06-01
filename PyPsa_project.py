import pypsa
import pandas as pd

##we now start with the Network initialization
##the network is the part of the database that holds all the variables
##i.e. the buses,generators and the lines
##it just contins the rules and inputs(More so like the data) 
network = pypsa.Network()


##we invovle this as time is a random variable it changes frequently
##we are using this to simulate it in a single 1 hr window 
time_index = pd.date_range("2026-06-01 12:00",periods = 1,frequency = "H")


##we then open a viewpoint to the current state of the simulation +
network.set_snapshot(time_index)


##here we then add a electrical node i.e Bus
##this is basically a transfer point (in brief)
network.add("Bus","main_electrical_node")


##we now add the consumer or the costs of the node i.e. a load
##this will be connected via our bus
##here the cost we are bearing is a 100 MegaWatts(p_set)
network.add("Load","City_load",bus="main_electrical_node",p_set = 100)


##now we add our source of energy i.e. a generator
##which will be connected via our bus i.e. the main electrical node
##this will have a max limit of 60 mega watts with a marginal cost of 5 units
##so in a literall sense our generator is generating a unit of power at 5 untis of money
##with a max limit of 60 units of energy (i.e. it would need 300 units of money)
network.add("Generator","Wind_Turbine",
            bus = "main_electrical_node",p_nom = 60 ,marginal_cost=5)


##here we add another generator into the mix which is a expensive generator
network.add("Generator","Gas_Turbine",
            bus = "main_electrical_node",p_nom = 80 ,marginal_cost=50)


##we "sanitize"; more so we just validate the connections to show that they
##are consistant 
network.sanitize()


##we then use an optimization equation here to find out the max profit we can obtian if
##our generators meet the 100 unit limit
network.optimize(solver_name="highs")


##we will see our results via our time series function (generator_t)

##the output we get is wind:60 and gas be 40 which directly reffers to the contribution
##of each element 
##with our active power output (p)
print(network.generator_t.p)
