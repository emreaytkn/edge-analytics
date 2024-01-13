

import pandas as pd
from sklearn import preprocessing
import avro.schema
import joblib
from datasource.avro_sink import AvroSink

INPUT_TOPIC = 'cmapss-in'

# Read cmapss test dataset into pandas dataframe
cmapss_data = pd.read_csv("../data/cmapss_test_data.csv")
cmapss_label = pd.read_csv("../data/cmapss_test_labels.csv")

scaler = joblib.load("../model/cmapss_scaler.save") 

cmapss_data = pd.DataFrame(scaler.transform(cmapss_data))

cmapss = AvroSink(
    boostrap_servers="localhost:9092", topic=INPUT_TOPIC, 
    data_scheme_filename='../schema/data_schema.avsc', label_scheme_filename='../schema/label_schema.avsc',
    deployment_id=1)

for i in range (0, cmapss_data.shape[0]):
    data = { 
        "cycle": cmapss_data.loc[i][0], 
        "lpc_outlet_temp": cmapss_data.loc[i][1], 
        "hpc_outlet_temp": cmapss_data.loc[i][2], 
        "lpt_outlet_temp": cmapss_data.loc[i][3],
        "bypass_duct_pressure": cmapss_data.loc[i][4], 
        "hpc_outlet_pressure": cmapss_data.loc[i][5], 
        "physical_fan_speed": cmapss_data.loc[i][6],
        "physical_core_speed": cmapss_data.loc[i][7], 
        "hpc_outlet_static_pressure": cmapss_data.loc[i][8],
        "ratio_of_fuel_flow": cmapss_data.loc[i][9],
        "corrected_fan_speed": cmapss_data.loc[i][10],
        "bypass_ratio": cmapss_data.loc[i][11],
        "bleed_enthalpy": cmapss_data.loc[i][12],
        "hpt_cool_air_flow": cmapss_data.loc[i][13],
        "lpt_cool_air_flow": cmapss_data.loc[i][14]
    }
    label = { "RUL": int(cmapss_label.loc[i][0]) }
    
    cmapss.send_avro(data, label)

cmapss.close()
