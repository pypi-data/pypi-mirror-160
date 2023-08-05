# -*- coding: utf-8 -*-

import med_data_science_helper.helper_siagie_kpi as hsk
import med_data_science_helper.helper_terceros_kpi as htk
import med_data_science_helper.helper_acces_db as hadb


se2018 = hadb.get_shock_economico(2018,cache=True)


df_siagie = hadb.get_siagie_por_anio(2022,id_nivel="B0",id_grado=8 , columns_n= ['ID_PERSONA'])


df_siagie_ = hsk.generar_kpis_p_deser_by_dist(df_siagie,anio_df=2020 , anio_h = 2019 ,t_anios=4  ,cache=True)
df_siagie_2 = hsk.generar_kpis_p_deser_by_codmod(df_siagie,anio_df=2020 , anio_h = 2019 ,t_anios=4  ,decimals=4,cache=True)

df_p_deser = hsk.get_p_desercion_by_distrito(anio=2019,macro_region="Peru",cache=True)


df_siagie.SITUACION_FINAL.value_counts()


df_siagie[df_siagie.DESERCION_2020_2021==1].SITUACION_FINAL.value_counts()




df_siagie.columns


df_siagie_ = hsk.generar_kpis_p_deser_by_dist(df_siagie,anio_df=2021 ,cache=True)

df_siagie_2 = hsk.generar_kpis_p_deser_by_codmod(df_siagie,anio_df=2021 ,cache=True)


df_siagie_2.P_DESERCION_COD_MOD_T_MENOS_1.value_counts()

df_p_deser = hsk.get_p_desercion_by_codmod(anio=2021,macro_region="norte",cache=False)


df_siagie2 = htk.agregar_nexus(df_siagie,anio_df=2021,anio_h=2020, cache=False )
df_siagie3 = htk.agregar_pivot_juntos(df_siagie,anio_df=2021,anio_h=2021,t_anios=3,delete_juntos_t_vcc=True, cache=False )

print(df_siagie3.columns)


print(df_siagie3.JUNTOS_T.value_counts())
print(df_siagie3.JUNTOS_T.isna().value_counts())

print(df_siagie3.JUNTOS_T_MENOS_1.isna().value_counts())
print(df_siagie3.JUNTOS_T_MENOS_1.value_counts())

print(df_siagie3.JUNTOS_T_MENOS_2.value_counts())
print(df_siagie3.JUNTOS_T_MENOS_2.isna().value_counts())
