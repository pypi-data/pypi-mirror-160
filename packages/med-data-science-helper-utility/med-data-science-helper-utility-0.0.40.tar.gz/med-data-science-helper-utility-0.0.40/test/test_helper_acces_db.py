
import pandas as pd
import numpy as np
import med_data_science_helper.helper_acces_db as hadb
import collections as c



df_siagie_ = hadb.get_siagie_por_anio(2018,  columns_n= ['ID_PERSONA'])
print(" 2018  : ",df_siagie_.shape)



df_serv = hadb.get_df_servicios(anio=2020,macro_region="lima_metro_callao",full=True)
print(df_serv.columns)







anio = 2020
df_siagie = hadb.get_siagie_por_anio(anio,macro_region="lima_metro_callao" ,desercion=True,  modalidad="EBR" , id_grado_list= [6,7,8] ,columns_n= ['ID_PERSONA','COD_MOD','ANEXO'])

df_siagie_ = hadb.get_siagie_por_anio(2022, modalidad="EBE", columns_n= ['ID_PERSONA','COD_MOD','ANEXO','ID_GRADO','ID_NIVEL'])



df_siagie = hadb.get_siagie_por_anio(2022,macro_region="Peru",ser_anio_menos_1 =True,modalidad="EBE", columns_n= ['ID_PERSONA','COD_MOD','ANEXO','ID_GRADO','ID_NIVEL'])




url_out ="E:\\PROYECTOS\\med-student-dropout-prediction\\src\\_04_Modeling\\modelos\\23062022\\03.data_output\\nacional_11072022_233916.dta"
df_out= pd.read_stata(url_out)  

df_siagie_out = pd.merge(df_siagie,df_out,left_on="ID_PERSONA",right_on="ID_PERSONA",how="inner")
df_siagie_out['RISK_SCORE_ROUND'] = df_siagie_out['RISK_SCORE'].round(decimals = 2)


df_siagie_out.RISK_SCORE_ROUND.value_counts()
df_siagie_out.columns



muestra = df_siagie_out[df_siagie_out.RISK_SCORE_ROUND==0.50].copy()
muestra.ID_GRADO.value_counts()

df_siagie_out.RISK_SCORE.max()




anios_str=str(anio)+"_"+str(anio+1)
original_col = "DESERCION_"+anios_str
df_siagie_ct =  pd.crosstab(index=df_siagie['D_DIST'], columns=df_siagie[original_col], normalize='index')
df_siagie_ct.rename({1: 'P_DESERCION_D_DIST', 0: 'P_SIN_DESERCION'}, axis=1, inplace=True)
df_siagie_ct.reset_index(drop=False,inplace=True)
df_siagie_ct.drop(['P_SIN_DESERCION'], axis = 1, inplace=True)


df_siagie_2020 = hadb.get_siagie_por_anio(2020,macro_region="lima_metro_callao", modalidad="EBR" , id_grado_list= [6,7,8] ,columns_n= ['ID_PERSONA','COD_MOD','ANEXO'])
df_siagie_2020 = pd.merge(df_siagie_2020, df_siagie_ct ,left_on="D_DIST",  right_on="D_DIST", how='left')











df_serv = hadb.get_df_servicios(anio=2020,macro_region="lima_metro_callao",full=True)

df_serv.columns

macro_region = "peru"
if macro_region in ["peru","perú","total","todo","general"]:
    print(True)

print(hadb.get_path_BD())



df_servicios = pd.concat([hadb.get_df_servicios(anio=2022) , hadb.get_df_servicios(anio=2021) ])
df_servicios.drop_duplicates(subset=['COD_MOD', 'ANEXO'], keep='first',inplace=True)



df_servicios = hadb.get_df_servicios(anio=2022)  
df_servicios = hadb.get_df_servicios(anio=2021)  


df = pd.merge(df_ebe,df_servicios, left_on=["COD_MOD","ANEXO"], right_on = ["COD_MOD","ANEXO"] ,how="inner")


print(df_ebe.shape)

path_file = hadb.get_path_BD_siagie_procesado()
url_trasl = path_file+'\\Siagie_Traslados_{}.csv'.format(2018)
sep = "|"
encoding = 'latin-1'
cols_tras = ['ID_PERSONA','TIPO_TRASLADO']
df_trasl = pd.read_csv(url_trasl ,encoding=encoding,usecols=cols_tras,  sep=sep,dtype={'ID_PERSONA':int})
df_merge = pd.merge(df_ebe,df_trasl,left_on = "ID_PERSONA",right_on="ID_PERSONA",how="inner")



dataSet_t = hadb.get_desertores_por_anio(2014)


dataSet_t = hadb.get_siagie_por_anio(2020,id_grado=1,id_nivel="A1",modalidad="EBR",  columns_n= ['ID_PERSONA'])
dataSet_t_menos_1 = hadb.get_siagie_por_anio(2019,modalidad_list=["EBR","EBE"],columns_n= ['ID_PERSONA'], id_persona_df=dataSet_t)    

df = hadb.get_desertores_por_anio(2019,modalidad="EBE")

df = hadb.get_nexus(anio=2015,cache=True,subtipo_trabajador=None)

df = hadb.get_ECE_2P()
df = hadb.get_ECE_4P()
df = hadb.get_ECE_2S()
df = hadb.get_ECE()

df = hadb.get_Censo_Educativo(anio=2019)

df = hadb.get_traslados_por_anio(2019)
df = hadb.get_traslados_a_publico(2019)

df = hadb.get_df_notas(2019)




df_se = hadb.get_shock_economico(2020,cache=False)

df_siagie_ebr = hadb.get_siagie_por_anio(2020,modalidad="EBR",id_nivel="A0", columns_n= ['ID_PERSONA'])  


df_siagie_ebe_ = hadb.get_siagie_por_anio(2021,modalidad_list=["EBE"],id_nivel="E2",columns_n= ['ID_PERSONA'],id_persona_df=df_siagie_ebr)  




df_siagie_ebr_ = hadb.get_siagie_por_anio(2020,modalidad_list=["EBR"],columns_n= ['ID_PERSONA'])  

df_siagie_ebe = hadb.get_siagie_por_anio(2020,modalidad="EBE",columns_n= ['ID_PERSONA'])  
df_siagie_ebe_ = hadb.get_siagie_por_anio(2020,modalidad_list=["EBE"],columns_n= ['ID_PERSONA'])  

df_siagie_total = hadb.get_siagie_por_anio(2020,modalidad_list=["EBR","EBE"],columns_n= ['ID_PERSONA'])  



df_siagie_ebr = hadb.get_siagie_por_anio(2020,modalidad="EBR",columns_n= ['ID_PERSONA','ID_NIVEL','COD_MOD','ANEXO'])  




df_siagie_ebe = hadb.get_siagie_por_anio(2020,modalidad="EBE",columns_n= ['ID_PERSONA','ID_NIVEL','COD_MOD','ANEXO'])  

df_siagie = pd.concat([df_siagie_ebr, df_siagie_ebe])  
print(df_siagie.shape)

df_serv = hadb.get_df_servicios(anio=2020,columns=["COD_MOD","ANEXO","CODGEO"])



df_merge = pd.merge(df_siagie, df_serv, left_on=["COD_MOD","ANEXO"], right_on=["COD_MOD","ANEXO"],  how='inner') 
print(df_merge.shape)

8106218-8106187

df = hadb.get_sisfoh()

df = hadb.get_distancia_prim_sec()
df = hadb.get_distancia_ini_prim()

df = hadb.get_siagie_por_anio(2020,id_nivel="A0")
