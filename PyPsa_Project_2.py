import pandas as pd
import pypsa


time_index = pd.date_range("2026-06-01", periods=24, freq="h")

## Varying wind capacity factor (0 to 1) across 24 hours
wind_profile = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.5, 
                0.3, 0.2, 0.2, 0.3, 0.4, 0.3, 0.2, 0.3,
                0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.4]



##this is a container of rules and inputs basically 
network = pypsa.Network()


##this basically gives a glimpse into each time frame so in this case its 24 hours 
##so we just only get 1 snapshot per hour
network.set_snapshots(time_index)


##Now we add our connection points which is our Buses,these points baiscally help 
##us connect the generator to the load
network.add("Bus","main_electrical_node")


##we now add the consumer or the costs of the node i.e. a load
##this will be connected via our bus
##here the cost we are bearing is a 100 MegaWatts(p_set)
network.add("Load","City_load",bus="main_electrical_node",p_set = 30)


##Now we add our generators
network.add("Generator","Wind_Turbine_1",bus="main_electrical_node",
            p_nom = 100,marginal_cost = 5)
network.add("Generator","Wind_Turbine_2",bus="main_electrical_node",
            p_nom = 100,marginal_cost = 5)


##this part of the code basically helps us get the total power of generation by 
##the wind which the generator is giving 
network.generators_t.p_max_pu['Wind_Turbine_1'] = wind_profile
network.generators_t.p_max_pu['Wind_Turbine_2'] = wind_profile  


##we "sanitize"; more so we just validate the connections to show that they
##are consistant 
network.sanitize()


##we then use an optimization equation here to find out the max profit we can obtian if
##our generators meet the 100 unit limit
network.optimize(solver_name="highs")


##we will see our results via our time series function (generator_t)
##with our active power output (p)
print(network.generators_t.p)

