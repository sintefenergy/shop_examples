import pandas as pd

def build_model(shop):
    starttime=pd.Timestamp("2018-02-27 00:00:00")
    endtime=pd.Timestamp("2018-02-28 00:00:00")
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit="hour")

    rsv1=shop.model.reservoir.add_object("Reservoir1")
    rsv1.hrl.set(100)
    rsv1.lrl.set(90)
    rsv1.max_vol.set(12)
    rsv1.vol_head.set(pd.Series([90,100,101],index=[0,12,14]))
    rsv1.flow_descr.set(pd.Series([0, 1000], index=[100, 101]))

    plant1=shop.model.plant.add_object("Plant1")
    plant1.main_loss.set([0.0002])
    plant1.penstock_loss.set([0.0001])
    plant1.outlet_line.set(40)

    p1g1=shop.model.generator.add_object("P1G1")
    p1g1.connect_to(plant1)
    p1g1.penstock.set(1)
    p1g1.p_min.set(25)
    p1g1.p_nom.set(100)
    p1g1.p_max.set(100)
    p1g1.startcost.set(500)
    p1g1.gen_eff_curve.set(pd.Series([95,98], index=[0,100]))
    p1g1.turb_eff_curves.set([pd.Series([80,95,90],index=[25,90,100],name=90),pd.Series([82,98,92],index=[25,90,100],name=100)])

    rsv2=shop.model.reservoir.add_object("Reservoir2")
    rsv2.hrl.set(50)
    rsv2.lrl.set(40)
    rsv2.max_vol.set(5)
    rsv2.vol_head.set(pd.Series([40,50,51],index=[0,5,6]))
    rsv2.flow_descr.set(pd.Series([0, 1000], index=[50, 51]))

    rsv1.connect_to(plant1)
    plant1.connect_to(rsv2)
   
    rsv1.start_head.set(92)
    rsv2.start_head.set(43)

    rsv1.inflow.set(10)
    rsv2.inflow.set(0)

    rsv1.energy_value_input.set(pd.Series([39.7],index=[0]))
    rsv2.energy_value_input.set(pd.Series([0],index=[0]))

    da=shop.model.market.add_object('Day_Ahead')
    da.sale_price.set(pd.Series([19.99,39.99],index=[starttime,starttime+pd.Timedelta(hours=6)]))
    da.buy_price.set(pd.Series([20.01,40.01],index=[starttime,starttime+pd.Timedelta(hours=6)]))
    da.max_sale.set(9999)
    da.max_buy.set(9999)
    
    
def run_model(shop):
    shop.start_sim([],['3'])
    shop.set_code(['inc'],[])
    shop.start_sim([],['3'])