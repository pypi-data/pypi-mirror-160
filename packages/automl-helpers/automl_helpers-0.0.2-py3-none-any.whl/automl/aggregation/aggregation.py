import pandas as pd
import numpy as np
import warnings

#pass in the data and either a file path or DataFrame specifying the aggregation approach
def aggregate_data(data,method_file="Aggregation_Method.csv"):
    #get the method file into a dataframe
    if type(method_file)==str:
        method=pd.read_csv(method_file)
    else:
        method=method_file
        
    new_df=data.copy()  
    
    #get list of all by groups
    by_groups=method[method["Type"]=="by_group"]["Feature"].unique()
    
    #always count the observations - this should sort by by_groups
    temp_df=new_df[list(by_groups)].groupby(list(by_groups)).size().reset_index(name="#obs_count")

    #For each row the the method file perform the action
    for ii in range(len(method)):
        this_var=method['Feature'].iloc[ii]

        if type(method['Method'].iloc[ii])!=str:
            continue
        #loop over the different actions to take: E.g. sum, mean , std, min, max
        for func in [func.strip() for func in method['Method'].iloc[ii].split(',')]:
            #levels methods
            if method['Type'].iloc[ii]=="level":
                temp_df[this_var+'_'+func]=new_df[list(by_groups)+[this_var]].groupby(list(by_groups))[this_var].agg(func).reset_index(drop=True) 
                if func in 'sum':
                    warnings.warn("Warning: Taking a sum of a numerical level")                   
            #flows methods        
            if method['Type'].iloc[ii]=="flow":
                temp_df[this_var+'_'+func]=new_df[list(by_groups)+[this_var]].groupby(list(by_groups))[this_var].agg(func).reset_index(drop=True) 

            #categorical data methods
            if method['Type'].iloc[ii]=="categorical":
                if func=="unique":
                    temp_df[this_var+'_#unique'] = new_df[list(by_groups)+[this_var]].groupby(list(by_groups))[this_var].apply(lambda x: len(np.unique(np.hstack(x)))).reset_index(drop=True)
                    temp_df[this_var+'_unique'] = new_df[list(by_groups)+[this_var]].groupby(list(by_groups))[this_var].apply(lambda x: np.unique(np.hstack(x))).reset_index(drop=True)
                    #to remove excess nan values
                    temp_df[this_var+'_unique'] = temp_df[this_var+'_unique'].astype(str).str.replace("nan[^0-9a-zA-Z\]']+","") 
                #method the calculates a by category value sum
                if '_' in func:
                    sub_func, this_ele=func.split('_')
                    cat_list=new_df[this_var].unique()
                    for cat_val in cat_list:
                        new_df["temp"]=np.nan
                        new_df.loc[new_df[this_var]==cat_val,"temp"]=new_df.loc[new_df[this_var]==cat_val][this_ele] 
                        temp_df[this_ele+"_("+this_var+"="+str(cat_val)+")"] = new_df[list(by_groups)+["temp"]].groupby(list(by_groups))["temp"].agg(sub_func).reset_index(drop=True)

            #string variable methods. Can use numerical aggregation features and will all be applied to counts
            if method['Type'].iloc[ii]=="text":
                new_df[this_var]=new_df[this_var].astype(str)
                #replace 'nan' with empty value
                new_df[this_var]=new_df[this_var].mask(new_df[this_var]=='nan','')

                if func=="concat":
                    temp_df[this_var] = new_df[list(by_groups)+[this_var]].groupby(list(by_groups))[this_var].apply(lambda x: ' | '.join(x)).reset_index(drop=True)
                else:
                    new_df["temp"]=[len(sss.split()) for sss in new_df[this_var]]
                    temp_df[this_var+'_'+func] = new_df[list(by_groups)+["temp"]].groupby(list(by_groups))["temp"].agg(func).reset_index(drop=True)

    new_df=temp_df
        
    return new_df