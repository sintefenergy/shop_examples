import pandas as pd

def build_model(shop):
    starttime=pd.Timestamp("2018-02-27 00:00:00")
    endtime=pd.Timestamp("2018-02-27 06:00:00")
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit="hour")

    rsv1=shop.model.reservoir.add_object("Reservoir1")
    rsv1.hrl.set(100)
    rsv1.lrl.set(90)
    rsv1.max_vol.set(5)
    rsv1.vol_head.set(pd.Series([90,100,101],index=[0,5,6]))
    rsv1.flow_descr.set(pd.Series([0, 1000], index=[100, 101]))

    rsv2=shop.model.reservoir.add_object("Reservoir2")
    rsv2.hrl.set(100)
    rsv2.lrl.set(90)
    rsv2.max_vol.set(5)
    rsv2.vol_head.set(pd.Series([90,100,101],index=[0,5,6]))
    rsv2.flow_descr.set(pd.Series([0, 1000], index=[100, 101]))

    rsv3=shop.model.reservoir.add_object("Reservoir3")
    rsv3.hrl.set(100)
    rsv3.lrl.set(90)
    rsv3.max_vol.set(5)
    rsv3.vol_head.set(pd.Series([90,100,101],index=[0,5,6]))
    rsv3.flow_descr.set(pd.Series([0, 1000], index=[100, 101]))

    plant1=shop.model.plant.add_object("Plant1")
    plant1.main_loss.set([0.0002])
    plant1.penstock_loss.set([0.0001])

    p1g1=shop.model.generator.add_object("P1G1")
    p1g1.connect_to(plant1)
    p1g1.penstock.set(1)
    p1g1.p_min.set(0.1)
    p1g1.p_nom.set(100)
    p1g1.p_max.set(100)
    p1g1.gen_eff_curve.set(pd.Series([95,98], index=[0,100]))
    p1g1.turb_eff_curves.set([pd.Series([80,95,90],index=[1,90,100],name=90),pd.Series([82,98,92],index=[1,90,100],name=100)])

    tunnel1=shop.model.tunnel.add_object("Tunnel1")
    tunnel1.loss_factor.set(0.00016)
    tunnel1.start_height.set(90)
    tunnel1.end_height.set(90)
    tunnel1.diameter.set(3)
    tunnel1.length.set(2022)
    
    tunnel2=shop.model.tunnel.add_object("Tunnel2")
    tunnel2.loss_factor.set(0.00015)
    tunnel2.start_height.set(90)
    tunnel2.end_height.set(90)
    tunnel2.diameter.set(3)
    tunnel2.length.set(2022)

    tunnel3=shop.model.tunnel.add_object("Tunnel3")
    tunnel3.loss_factor.set(0.00030)
    tunnel3.start_height.set(90)
    tunnel3.end_height.set(90)
    tunnel3.diameter.set(3)
    tunnel3.length.set(2022)

    rsv1.connect_to(tunnel1)
    tunnel1.connect_to(rsv2)
    rsv2.connect_to(tunnel2)
    tunnel2.connect_to(rsv3)
    rsv3.connect_to(tunnel3)
    tunnel3.connect_to(plant1)

    rsv1.start_head.set(93)
    rsv2.start_head.set(93)
    rsv3.start_head.set(97)

    rsv3.inflow.set(200)

    rsv1.energy_value_input.set(pd.Series([31.7],index=[0]))
    rsv2.energy_value_input.set(pd.Series([31.7],index=[0]))
    rsv3.energy_value_input.set(pd.Series([31.7],index=[0]))

    da=shop.model.market.add_object('1')
    da.sale_price.set(39.99)
    da.buy_price.set(40.01)
    da.max_sale.set(9999)
    da.max_buy.set(9999)
    
def add_gate(shop):
    tunnel2=shop.model.tunnel["Tunnel2"]
    tunnel2.gate_opening_curve.set(pd.Series([0,1],index=[0,1]))
    tunnel2.continuous_gate.set(1)
    
def run_model(shop):
    shop.start_sim([],['3'])
    shop.set_code(['inc'],[])
    shop.start_sim([],['3'])