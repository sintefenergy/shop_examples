import pandas as pd
import numpy as np

def build_model(shop):
    starttime = pd.Timestamp('2018-01-23 00:00:00')
    endtime = pd.Timestamp('2018-01-26')
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit="hour", timeresolution=pd.Series(index=[starttime],data=[1]))
    
    rsv1 = shop.model.reservoir.add_object('Reservoir1')
    rsv1.max_vol.set(39)
    rsv1.lrl.set(860)
    rsv1.hrl.set(905)
    rsv1.vol_head.set(pd.Series([860, 906, 907], index=[0, 39, 41.66], name=0))    

    rsv2 = shop.model.reservoir.add_object('Reservoir2')
    rsv2.max_vol.set(97.5)   
    rsv2.lrl.set(650)   
    rsv2.hrl.set(679)    
    rsv2.vol_head.set(pd.Series([650, 679, 680], index=[0, 97.5, 104.15], name=0))
    
    plant1 = shop.model.plant.add_object('Plant1')
    plant1.outlet_line.set(672)
    plant1.main_loss.set([0])
    plant1.penstock_loss.set([0.001])
    plant1.mip_flag.set(1)
    for gen_no in range(2):
        gen=shop.model.generator.add_object(f"{plant1.get_name()}_G{str(gen_no+1)}")
        gen.connect_to(plant1)
        gen.penstock.set(1)
        gen.p_min.set(60)
        gen.p_max.set(120)
        gen.p_nom.set(120)
        gen.startcost.set(300)
        gen.gen_eff_curve.set(pd.Series([100, 100], index=[60, 120]))
        gen.turb_eff_curves.set([pd.Series([85.8733, 87.0319, 88.0879, 89.0544, 89.9446, 90.7717, 91.5488, 92.2643, 92.8213, 93.1090, 93.2170, 93.0390, 92.6570, 92.1746],
                                    index=[28.12, 30.45, 32.78, 35.11, 37.45, 39.78, 42.11, 44.44, 46.77, 49.10, 51.43, 53.76, 56.10, 58.83],
                                    name=170),
                          pd.Series([86.7321, 87.9022, 88.9688, 89.9450, 90.8441, 91.6794, 92.4643, 93.1870, 93.7495, 94.0401, 94.1492, 93.9694, 93.5836, 93.0964],
                                    index=[28.12, 30.45, 32.78, 35.11, 37.45, 39.78, 42.11, 44.44, 46.77, 49.10, 51.43, 53.76, 56.10, 58.83],
                                    name=200),
                          pd.Series([87.5908, 88.7725, 89.8497, 90.8355, 91.7435, 92.5871, 93.3798, 94.1096, 94.6777, 94.9712, 95.0813, 94.8998, 94.5101, 94.0181],
                                    index=[28.12, 30.45, 32.78, 35.11, 37.45, 39.78, 42.11, 44.44, 46.77, 49.10, 51.43, 53.76, 56.10, 58.83],
                                    name=230)])

    plant2 = shop.model.plant.add_object('Plant2')
    plant2.outlet_line.set(586)
    plant2.main_loss.set([0])
    plant2.penstock_loss.set([0.0001,0.0002])
    plant2.mip_flag.set(1)
    for gen_no in range(4):
        gen=shop.model.generator.add_object(f"{plant2.get_name()}_G{str(gen_no+1)}")
        gen.connect_to(plant2)
        if gen_no == 0:
            gen.penstock.set(1)
            gen.p_min.set(100)
            gen.p_max.set(180)
            gen.p_nom.set(180)
            gen.startcost.set(300)
            gen.gen_eff_curve.set(pd.Series([100, 100], index=[100, 180]))
            gen.turb_eff_curves.set([pd.Series([92.7201, 93.2583, 93.7305, 94.1368, 94.4785, 94.7525, 94.9606, 95.1028, 95.1790, 95.1892, 95.1335, 95.0118, 94.8232, 94.5191],
                                        index=[126.54, 137.03, 147.51, 158.00, 168.53, 179.01, 189.50, 199.98, 210.47, 220.95, 231.44, 241.92, 252.45, 264.74],
                                        name=60)])
        else:
            gen.penstock.set(2)
            gen.p_min.set(30)
            gen.p_max.set(55)
            gen.p_nom.set(55)
            gen.startcost.set(300)
            gen.gen_eff_curve.set(pd.Series([100, 100], index=[30, 55]))
            gen.turb_eff_curves.set([pd.Series([83.8700, 85.1937, 86.3825, 87.4362, 88.3587, 89.1419, 89.7901, 90.3033, 90.6815, 90.9248, 91.0331, 91.0063, 90.8436, 90.4817],
                                        index=[40.82, 44.20, 47.58, 50.97, 54.36, 57.75, 61.13, 64.51, 67.89, 71.27, 74.66, 78.04, 81.44, 85.40],
                                        name=60)])
    
    rsv1.connect_to(plant1)
    plant1.connect_to(rsv2)
    rsv2.connect_to(plant2)
    
    rsv1.start_head.set(900)
    rsv2.start_head.set(670)    
    
    rsv1.inflow.set(pd.Series([80], [starttime]))
    rsv2.inflow.set(pd.Series([60], [starttime]))
    
    da = shop.model.market.add_object('Day_ahead')
    da.sale_price.set(pd.DataFrame([32.992,31.122,29.312,28.072,30.012,33.362,42.682,74.822,77.732,62.332,55.892,46.962,42.582,40.942,39.212,39.142,41.672,46.922,37.102,32.992,31.272,29.752,28.782,28.082,27.242,26.622,25.732,25.392,25.992,27.402,28.942,32.182,33.082,32.342,30.912,30.162,30.062,29.562,29.462,29.512,29.672,30.072,29.552,28.862,28.412,28.072,27.162,25.502,26.192,25.222,24.052,23.892,23.682,26.092,28.202,30.902,31.572,31.462,31.172,30.912,30.572,30.602,30.632,31.062,32.082,36.262,34.472,32.182,31.492,30.732,29.712,28.982], 
                               index=[starttime + pd.Timedelta(hours=i) for i in range(0,72)]))
    da.max_sale.set(pd.Series([9999], [starttime]))
    da.buy_price.set(da.sale_price.get()+0.002)
    da.max_buy.set(pd.Series([9999], [starttime]))

    settings = shop.model.global_settings.global_settings
    settings.mipgap_rel.set(0)
    settings.mipgap_abs.set(0)

def run_model(shop):
    shop.start_sim([], ['5'])
    shop.set_code(['incremental'], [])
    shop.start_sim([], ['3'])


def read_cuts():
    
    with open("rhs_file.txt","r") as f:
        lines = [l for l in f]
    
    rhs = []
    for l in lines:
        l = l.split(",")
        rhs.append(float(l[0]))
        
    with open("wv_file.txt","r") as f:
        lines = [l for l in f]
    
    cut_coeffs = {}
    v_ref = []
    wv = []
    name = ""
    for l in lines:
        l = l.split(",")
        
        if len(l) < 3:
            
            if len(v_ref) > 0 and len(wv) > 0:
                cut_coeffs[name] = v_ref,wv
                v_ref = []
                wv = []
                
            name = l[0]
            continue
        
        v_ref.append(float(l[0]))        
        wv.append(float(l[1]))    

    cut_coeffs[name] = v_ref,wv

        
    return rhs, cut_coeffs    
    
    
def get_minimal_cut_surface(rhs,cut_coeffs,v1,v2):

    v_ref1,wv1 = cut_coeffs["Reservoir1"]
    v_ref2,wv2 = cut_coeffs["Reservoir2"]

    v_mesh1,v_mesh2 = np.meshgrid(v1,v2)

    cuts = []

    for k in range(len(rhs)):        
        c = rhs[k] + wv1[k]*(v_mesh1-v_ref1[k]) + wv2[k]*(v_mesh2-v_ref2[k])
        cuts.append(c)
        

    minimal_surface = np.zeros(cuts[0].shape)

    binding_cuts = set()

    for i in range(len(v1)):
        for j in range(len(v2)):
            minimal_surface[j][i] = np.amin([c[j][i] for c in cuts])
            
            binding_cuts.add(np.argmin([c[j][i] for c in cuts]))      
            
    return binding_cuts,minimal_surface
    