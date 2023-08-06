#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import altair as alt
import pathlib
import cv2
import imutils
from PIL import Image
from html2image import Html2Image 
import pkg_resources

# pip install html2image # allows html to png conversion
# pip install pyarrow # this is a backend for parquet files
# pip install fastparquet # this is a backend for parquet files
# pip install opencv-python # this allows import cv2
# pip install imutils # this allows import imutils
# pip install pandas
# pip install numpy


# In[2]:


def generate_ed_age_department_acuity_graph(data,
                                            person_id,
                                            department_1,
                                            department_2,
                                            compare='yes',
                                            configuration=None, 
                                            config_dept=None):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Generates the graph of each provider with the facility-wide comparison 
    graph. 
    
    The provider graph represents actual volumes at both facilities, and the 
    facility wide comparison represents the median provider. At a given age, 
    the median is computed by dropping providers with zero volume and then 
    computing the median at the. The exception to this is if a facility has 
    zero volume at the given age; if this occurs, then we set the median to be
    zero so the row is not eliminated in the final graph. It is possible to 
    use an example data set, or an actual data set. Accessing the example data 
    set is described below.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    data
        This parameter is required. This parameter is the dataframe 
        containing data on every single provider. This parameter will also 
        except the string value 'example'. If this string is given, then 
        an example file will be generated from a fake data set.

        IF A DATAFRAME IS PASSED IN, IT MUST HAVE THE FOLLOWING COLUMN
        STRUCTURE:
            AGE_AT_ADMISSION : int
            DEPARTMENT_NAME : str
            ACUITY_LEVEL : str : 'ESI 1', 'ESI 2', ...
            PROV_NAME : str
            PROV_ID : int
            NUM_PAT : int 
            FIRST_DATE : str : 'mm/dd/yyyy'
            LAST_DATE : str : 'mm/dd/yyyy'

    person_id
        This parameter is required. This parameter controls a particular 
        provider's graph. Each provider is given a unique integer ID 
        value, so you pass that value in and the function will filter for
        that particular provider. If this value is not an integer, or 
        cannot be converted to an integer, then an error will be thrown. 
        Values like 123.0, '123.0', and 123 will pass the assert 
        statements, but things like 123.1 and '123.1' will not pass the 
        assert statements. This parameter will also accept the value None. 
        Passing None will eliminate the comparison graph if a data is 
        passed an actual dataframe. If data is passed 'example', person_id 
        will automatically be defaulted to 123456789, and a comparison 
        graph will be included. 

    department_1
        This parameter is required. The value represents the name of the 
        first department you want to compare. If data is set to 'example', 
        this department name will be overidden and it will be reassigned 
        to 'Department 1'.

    department_2
        This parameter is required. The value represents the name of the 
        second department you want to compare. If data=='example', this 
        department name will be overidden and it will be reassigned to 
        'Department 2'.

    compare
        This parameter is optional. This value indicates whether to 
        include the comparison graph or not. 'yes' includes the comparison 
        graph while 'no' excludes the comparison graph. Setting this value to 
        'generic' will only produce the comparison provider, and will override 
        the variable configuration. Default value is 'yes'.

    configuration
        This parameter is optional. This value sets the rule for grouping 
        charts. If None or 'separate', both of the department graphs will be 
        grouped together and the both the comparison departments will be 
        grouped together. If this is set to 'together', then the graph with 
        pair each department graph with its' respective comparison graph, 
        where the department 1 chart is on the left and the department 2 chart 
        is on the right (i.e.,
        
        (dept 1 graph | dept 1 comparison) | (dept 2 graph | dept 2 comparison)

        Default is None.     
        
    config_dept
        This parameter is optional. This value controls the department used in
        the comparison when 
            compare=='no',
            configuration='together'
        By default, config_dept==None, which auto-selects the value from the
        variable department_1. Alternatively, you can specify 'department_1'
        or 'department_2', respectively. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function does not return anything, but it does save a png figure
    using the person_id in the name of the file. This function generates the 
    png file via an HTML file, and then eliminates the HTML file.
            
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Special Cases
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    One special case in the code I stumbled on during testing was a specific 
    combination of the parameters:
        compare = 'no'
        configuration='together'.
    This code, as intended, was designed to handle two distinct departments, 
    no more, no less. But the code can be tricked into handling any number of 
    departments and any number of provider IDs. Pseudo code below.
        for id in prov_ids:
            for dept_name in dept_names:
                generate_ed_age_department_acuity_graph(data=df,
                                                        person_id=id,
                                                        department_1=dept_name,
                                                        department_2=dept_name,
                                                        compare='no',
                                                        configuration='together', 
                                                        config_dept='department_1')
        
    '''
    
    # resources
    # https://altair-viz.github.io/gallery/us_population_pyramid_over_time.html
    # https://altair-viz.github.io/user_guide/configuration.html
    # https://learnui.design/tools/data-color-picker.html#palette
    # https://altair-viz.github.io/gallery/stacked_bar_chart.html
    # https://personal.sron.nl/~pault/
    # https://stackoverflow.com/questions/60328943/how-to-display-two-different-legends-in-hconcat-chart-using-altair
    # https://stackoverflow.com/questions/68624885/position-altair-legend-top-center
    
    alt.renderers.enable('default') # for rendering in jupyter when connected to the web
    # alt.renderers.enable('mimetype') # for rendering in jupyter when not connected to the web
    
    # Do an initial check on the inputs.
    assert compare in ['yes','no','generic'], 'your input for compare is not valid'
    assert configuration in [None,'separate','together'], 'your input for configuration is not valid'
    assert config_dept in [None,'department_1','department_2'], 'your input for config_dept is not valid'
    
    if compare=='generic':
        configuration='separate'
    
    if isinstance(data,str):
        assert data=='example', 'data was not a dataframe and was not marked as \'example\''
        stream = pkg_resources.resource_stream(__name__, 'examples/age_acuity_department_example.parq')
        data=pd.read_parquet(stream)
        person_id=123456789
        department_1='DEPARTMENT 1'
        department_2='DEPARTMENT 2'
    
    elif isinstance(data,pd.DataFrame) is True:
        data=data.copy(deep=True)
        data.columns=['PROV_ID' if 'PROV_ID' in col else col.upper() for col in data.columns]
        data.columns=['PROV_NAME' if 'PROV_NAME' in col else col.upper() for col in data.columns]
        data_columns=list(data.columns)
        assert ('PROV_ID' in data_columns) is True, 'a provider ID column was not in the columns of the dataframe'   
        assert ('AGE_AT_ADMISSION' in data_columns) is True, 'AGE_AT_ADMISSION was not in the columns of the dataframe'
        assert ('DEPARTMENT_NAME' in data_columns) is True, 'DEPARTMENT_NAME was not in the columns of the dataframe'
        assert ('AGE_AT_ADMISSION' in data_columns) is True, 'AGE_AT_ADMISSION was not in the columns of the dataframe'
        assert ('ACUITY_LEVEL' in data_columns) is True, 'ACUITY_LEVEL was not in the columns of the dataframe'
        assert ('NUM_PAT' in data_columns) is True, 'NUM_PAT was not in the columns of the dataframe'
        assert ('FIRST_DATE' in data_columns) is True, 'FIRST_DATE was not in the columns of the dataframe'
        assert ('LAST_DATE' in data_columns) is True, 'LAST_DATE was not in the columns of the dataframe'
        assert isinstance(float(person_id),float) is True, 'person_id could not be converted to a number'
        assert (float(person_id)%1==0) is True, 'person_id could not be converted to an integer'
        assert department_1 in list(data['DEPARTMENT_NAME'].unique()), 'department_1 is not in your dataframe'
        assert department_2 in list(data['DEPARTMENT_NAME'].unique()), 'department_2 is not in your dataframe'
        assert len(list(data['DEPARTMENT_NAME'].unique()))==2, 'you do not have exactly two departments' 
    else:
        assert isinstance(data,pd.DataFrame) is True, 'data was not a dataframe and was not marked as \'example\''
        
    # Define the first and last dates in the data set.
    first_date=data['FIRST_DATE'].min()
    last_date=data['LAST_DATE'].min()
    
    # Determine the maximum horizontal distance on all of the graphs. This 
    # this value is the maximum value across all providers so the scales are
    # directly comparable in all graphs.
    max_horizontal_value=data.copy(deep=True)
    max_horizontal_value=max_horizontal_value.groupby(['DEPARTMENT_NAME','AGE_AT_ADMISSION','PROV_ID']).sum('NUM_PAT')
    max_horizontal_value=max_horizontal_value['NUM_PAT'].max()
    
    # Build comparison dataframe, if applicable.
    # This dataframe has 
    # (number of ESI levels) * (number of departments) * (age range)
    # number of rows. Each row represents a unique combination of 
    # non-zero medians. In the case a zero does show up, that means we
    # served no person in that demographic. Think of this dataframe as
    # representing an arbitrary, average provider.
    comparison_df=build_comparison_df(data)

    # Because this is a comparison, we need to map the provider name down
    # to a generic provider. 
    comparison_df['PROV_NAME']='GENERIC PROVIDER'

    # Like above, this provider needs to have department volumes attached
    # to each department label. At first pass it may seem like we are 
    # redfining the dept_with_count column, but that is not true. We 
    # already eliminated that when we built comparison_df.
    comparison_df,comparison_dept_dict=set_dept_labels(comparison_df)

    # Similarly, acuity is no different. Same comment from above.
    comparison_df=set_acuity_labels(comparison_df,
                                    department_1,
                                    department_2)
    
    # Now massage the data into the proper form.
    data=data[data['PROV_ID']==int(person_id)].copy(deep=True)
    data['AGE_AT_ADMISSION_nominal']=data['AGE_AT_ADMISSION'].apply(lambda x: str(x))
    data['AGE_AT_ADMISSION_label']=data['AGE_AT_ADMISSION'].apply(lambda x: str(x) if x % 5 == 0 else ' ')
    comparison_df['AGE_AT_ADMISSION_nominal']=comparison_df['AGE_AT_ADMISSION'].apply(lambda x: str(x))
    comparison_df['AGE_AT_ADMISSION_label']=comparison_df['AGE_AT_ADMISSION'].apply(lambda x: str(x) if x % 5 == 0 else ' ')

    # Assign provider department volumes to each department label.
    data,data_dept_dict=set_dept_labels(data)

    # Assign provider acuity volumes to each acuity level by department.
    data=set_acuity_labels(data,department_1,department_2)
    
    # Build each graph component. Big picture, this build is joining either
    # three (3) graphs or six (6) graphs. No other value is possible. Three
    # graphs occur when the initial parameter compare=='no'. Six graphs occur
    # when compare=='yes'. It helps to think about this build in terms of two
    # halves, three graphs each. In each case, there is a left, a middle, and
    # a right graph. See below.
    # 
    #                   (LLG | M | LRG) | (RLG | M | RRG)
    # 
    # The middle on both sides is identical. The lefts and rights are not 
    # identical though. Those are controlled by the pairing of variables 
    # (compare, configuration). Assuming compare=='yes', the following will 
    # occur
    #     configuration in ['separate',None]
    #         This means the left graph of the left half (LLG) will be the 
    #         providers actual data in department_1. The right graph of the left
    #         half (LRG) will be the providers actual data in department_2.
    #         The left graph in the right half (RLG) will be the comparison 
    #         provider in department_1. The right graph in the right half (RRG)
    #         will be the comparison provider in department_2.
    #     configuration in ['together']
    #         This means the left graph of the left half (LLG) will be the 
    #         providers actual data in department_1. The right graph of the left
    #         half (LRG) will be the comparison provider in department_1.
    #         The left graph in the right half (RLG) will be the providers 
    #         actual data in department_2. The right graph in the right half 
    #         (RRG) will be the comparison provider in department_2. 
    # When compare=='no', we simply boil down to the case of the left graph in 
    #     configuration in ['separate',None].
    # When compare=='generic', we simply boil down to the case of the right 
    # graph in 
    #     configuration in ['separate',None].
    
    if compare=='no' and configuration=='together' and config_dept in [None,'department_1']:
        department_1 = department_1
        department_2 = department_1
    elif compare=='no' and configuration=='together' and config_dept in ['department_2']:
        department_1 = department_2
        department_2 = department_2
            
    middle_graph=build_middle_ed_age_dept_acuity_graph(data)
    
    if configuration in ['separate',None]:
        LLG=build_left_ed_age_dept_acuity_graph(
            data,
            department_1,
            max_horizontal_value,
            data_dept_dict)
        LRG=build_right_ed_age_dept_acuity_graph(
            data,
            department_2,
            max_horizontal_value,
            data_dept_dict)
        RLG=build_left_ed_age_dept_acuity_graph(
            comparison_df,
            department_1,
            max_horizontal_value,
            comparison_dept_dict)
        RRG=build_right_ed_age_dept_acuity_graph(
            comparison_df,
            department_2,
            max_horizontal_value,
            comparison_dept_dict)
    elif configuration=='together':
        LLG=build_left_ed_age_dept_acuity_graph(
            data,
            department_1,
            max_horizontal_value,
            data_dept_dict)
        RLG=build_left_ed_age_dept_acuity_graph(
            data,
            department_2,
            max_horizontal_value,
            data_dept_dict)
        LRG=build_right_ed_age_dept_acuity_graph(
            comparison_df,
            department_1,
            max_horizontal_value,
            comparison_dept_dict)
        RRG=build_right_ed_age_dept_acuity_graph(
            comparison_df,
            department_2,
            max_horizontal_value,
            comparison_dept_dict)
    else:
        assert False is True, 'you entered an incorrect configuration parameter'
    
    prov_name_string=data['PROV_NAME'].unique()[0]
    comp_name_string='GENERIC PROVIDER'
    
    # Build the final graph using the components above.
    if compare in ['yes'] and configuration in [None,'separate']:
        provider_graph=build_final_ed_age_dept_acuity_graph_w_comp(
            LLG, 
            middle_graph,
            LRG,
            RLG,
            middle_graph,
            RRG,
            first_date,
            last_date
        )
    elif compare in ['generic'] and configuration in [None,'separate']:
        provider_graph=build_final_ed_age_dept_acuity_graph_wo_comp(
            RLG, 
            middle_graph,
            RRG, 
            first_date,
            last_date
        )
    elif compare=='yes' and configuration in ['together']:
        provider_graph=build_final_ed_age_dept_acuity_graph_w_comp(
            LLG, 
            middle_graph,
            LRG, 
            RLG, 
            middle_graph,
            RRG,
            first_date,
            last_date
        )
    elif compare=='no' and configuration in [None,'separate']:
        provider_graph=build_final_ed_age_dept_acuity_graph_wo_comp(
            LLG, 
            middle_graph,
            LRG, 
            first_date,
            last_date
        )
    else: 
        provider_graph=build_final_ed_age_dept_acuity_graph_wo_comp(
            LLG,
            middle_graph,
            LRG, 
            first_date,
            last_date
        )
    
    final=provider_graph
    
    # Save the final chart. This function first converts to an HTML file, 
    # screen shots the result, use PIL to crop the image so we remove the 
    # black boundaries, and save to a png file. 
    save_altair_graph_as_png(person_id,
                             primary_graph=final,
                             comparison_graph=None
                            )
    
    
    return provider_graph
    


# In[3]:


def set_dept_labels(dept_df):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Generates a new column in the dataframe with counts on each department. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    dept_df
        The dataframe with department column you want counts on.
            
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    dept_df
        The altered dataframe including the new column with counts.
    
    dept_dict
        A dictionary of {department name : department name and values}.
    '''
    
    # Ensure we only modify the copy and not the original.
    dept_df=dept_df.copy(deep=True)
    
    # Add up the number of patients by department.
    group_sizes=dept_df.groupby('DEPARTMENT_NAME').sum('NUM_PAT')
    group_sizes.to_excel('dept_1.xlsx')
    
    # Take the index of the previous dataframe (i.e., the department names), 
    # and append the number of cases to it. 
    dept_dict=group_sizes.index + ' (n = ' + group_sizes['NUM_PAT'].astype(str) + ')'
    
    # Now determine the total number of patients for this provider by adding 
    # together the values we just calculated for the individual departments.
    # Save this value with the name of the provider. 
    name_value=0
    for idx in group_sizes.index:
        name_value+=group_sizes.loc[idx,'NUM_PAT']
    name_string=list(dept_df['PROV_NAME'].unique())[0]
    name_string=name_string.title() + ' (n = ' + str(name_value) + ')'
    
    # Reformat the names of the departments to look pretty if it is an 
    # Emergency Department. 
    for key in dept_dict.keys():
        dept_dict[key]=dept_dict[key].replace('EMERGENCY DEPARTMENT','Emergency Department')
    
    # Do not destroy the original department names because we will need those
    # later. So stroe them in a proxy column.
    dept_df['DEPARTMENT_NAME_with_count']=dept_df['DEPARTMENT_NAME'].replace(dept_dict)
    
    # Ensure we return a copy of the dataframe so we keep the original intact. 
    return dept_df.copy(deep=True), dept_dict


# In[4]:


def set_acuity_labels(acuity_df,dept_1,dept_2):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Generates a new column in the dataframe with counts on each acuity. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    acuity_df
        The dataframe with acuity column you want counts on.
        
    dept_1
        This parameter is required. The name of a department you want to cut 
        out of the acuity key. This can be the same as dept_2, but this is 
        not a desired state in most situations.
    
    dept_2
        This parameter is required. The name of a department you want to cut 
        out of the acuity key. This can be the same as dept_1, but this is 
        not a desired state in most situations.
            
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    acuity_df
        A dataframe containing the new column of acuity values tied to their
        count.
    
    
    '''
    
    # Ensure we do not alter the original. 
    acuity_df=acuity_df.copy(deep=True)
    
    # Create a temporary key that we can use it during summation. 
    acuity_df['ACUITY_DEPARTMENT']=acuity_df['ACUITY_LEVEL'] + acuity_df['DEPARTMENT_NAME']
    
    # Sum the key we just created. The result of this will look like 
    # 'ESI 1DEPARTMENT 1: 10'
    # 'ESI 2DEPARTMENT 1: 15'
    # ...
    # This continues till we run out of ESI-Department pairs.
    group_sizes=acuity_df.groupby('ACUITY_DEPARTMENT').sum('NUM_PAT')
    group_sizes.to_excel('acuity_dept_1.xlsx')
    
    # Attach the number of patients to the key values above.
    acuity_dict=group_sizes.index + ' (n = ' + group_sizes['NUM_PAT'].astype(str) + ')'
    
    # Create a proxy column so we do not destory the original data. We will 
    # need the original data later.
    acuity_df['ACUITY_LEVEL_with_count']=acuity_df['ACUITY_DEPARTMENT'].replace(acuity_dict)
    
    # Finally, we remove the mention of 'DEPARTMENT 1' and 'DEPARTMENT 2' from 
    # the key column we just created. 
    acuity_df['ACUITY_LEVEL_with_count']=acuity_df['ACUITY_LEVEL_with_count'].apply(lambda x: x.replace(dept_2,''))
    acuity_df['ACUITY_LEVEL_with_count']=acuity_df['ACUITY_LEVEL_with_count'].apply(lambda x: x.replace(dept_1,''))
    
    # Reformat the string for unknown ESI levels.
    acuity_df['ACUITY_LEVEL_with_count']=acuity_df['ACUITY_LEVEL_with_count'].apply(lambda x: x.replace('NOT SPECIFIED','Not Specified'))
    
    # Ensure we sever ties so we have clean data back in the trunk.
    return acuity_df.copy(deep=True)


# In[5]:


def build_comparison_df(comp_df):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Builds a comparison dataframe by eliminating the unnecessary information
    and grouping what remains. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    comp_df
        This is the original dataframe containing all data. 
            
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    comp_df
        This is an altered version of the original dataframe. This version 
        has been completely deduplicated and resummed using a median for 
        each age level. 
    
    '''
    
    # Ensure we do not edit the original data set. 
    comp_df=comp_df.copy(deep=True)
    
    # Strip down to the base columns we will need to group and sum.
    comp_df=comp_df[['AGE_AT_ADMISSION', 
                         'DEPARTMENT_NAME', 
                         'ACUITY_LEVEL', 
                         'NUM_PAT']]
    
    # We will need a copy of the comparison dataframe later, so make sure we
    # save it before we group. When we group, throw out the rows containing
    # a 0 for the number of patients. We do this to remove one off providers
    # from the calculation of the median. This is a necessary step because
    # we have a huge number of providers that are one offs. 
    group_df=comp_df.copy(deep=True)
    group_df=group_df[group_df['NUM_PAT']!=0]
    group_df=group_df.groupby(['AGE_AT_ADMISSION', 
                               'DEPARTMENT_NAME', 
                               'ACUITY_LEVEL'])['NUM_PAT'].median()
    
    # Now that we have grouped, we need to reset the index to recover the 
    # three grouping columns. These columns will be a join condition below. 
    group_df=group_df.reset_index(drop=False
                                 ).sort_values(by=['DEPARTMENT_NAME',
                                                   'AGE_AT_ADMISSION',
                                                   'ACUITY_LEVEL'])
    
    # Before we join, throw out all of the duplicate entries. This limits us
    # to (number of ESI levels) * (age range) * (number of departments) rows.
    # In case it isn't obvious, this produces unique combinations. 
    comp_df=comp_df[['AGE_AT_ADMISSION', 
                     'DEPARTMENT_NAME', 
                     'ACUITY_LEVEL']].drop_duplicates(ignore_index=True)
    
    # Join in the grouped data. Essentially this attachs a value to every row
    # and leaves np.nan values every place a combination didn't occur. This
    # data structure is reasonably sparse despite the visual generated from 
    # this data. That is why we fillna(0) below. This eliminates the np.nan
    # values, and the sparseness is now identified by the zeros.
    comp_df=pd.merge(left=comp_df,
                      right=group_df,
                      how='left',
                      left_on=['AGE_AT_ADMISSION', 
                               'DEPARTMENT_NAME', 
                               'ACUITY_LEVEL'],
                      right_on=['AGE_AT_ADMISSION', 
                                'DEPARTMENT_NAME', 
                                'ACUITY_LEVEL']
                 )
    comp_df['NUM_PAT']=comp_df['NUM_PAT'].fillna(0)
    comp_df['NUM_PAT']=comp_df['NUM_PAT'].apply(lambda x: int(round(x,0)))
    
    # Ensure we return a copy that doesn't alter this base table. 
    return comp_df.copy(deep=True)


# In[6]:


def build_left_ed_age_dept_acuity_graph(left_data,
                                        left_department,
                                        left_max_horizontal,
                                        left_dept_dict):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Build the graph for this filtered dataframe; this will be the left graph
    of the three in the final picture. The result will be a vertical bar 
    graph, where one level represents one age category, and each level is 
    colored by the acuity level.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    left_data
        This is a dataframe containing all of the initial data. 
    
    left_department
        This is a department name you want to display on the left side of a 
        graph. 
    
    left_max_horizontal
        This is the largest value to be displayed on the graph, autorounded 
        to the next appropriate increment (for instance, if 
        left_max_horizontal is 6, the display will round to 10).
    
    left_dept_dict
        Despite the name, this is a dataframe containing the department name 
        in the index and the (department name with volume label) in the only
        column. Effectively, think of this like a pd.Series. 

    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    An altair chart.
    
    
    '''
    
    # Create a filtered dataframe for one ed.
    left_data=left_data.copy(deep=True)
    left_data=left_data.drop(left_data[left_data['DEPARTMENT_NAME']!=left_department].index)
    left_prov_name=left_data['PROV_NAME'].unique()[0]

    # Set the coloring properties of this filtered dataframe. This wil match
    # the coloring scheme from the graph on the right given below.
    color_scale=alt.Scale(domain=list(left_data['ACUITY_LEVEL_with_count'].unique()),
                            range=['#dc050c','#f6c141','#4eb265','#1965b0','#882e72','#000000'])
    
    # Build the graph.
    left=alt.Chart(left_data
                    ).transform_filter(alt.datum.DEPARTMENT_NAME==left_department
                    ).encode(
                        y=alt.Y('AGE_AT_ADMISSION_nominal:N', 
                                sort=sorted(list(left_data['AGE_AT_ADMISSION'].sort_values(ascending=True).unique()), 
                                              reverse=True),
                                axis=alt.Axis(orient='right',
                                                title=None, 
                                                labels=False)
                               ),
                        x=alt.X('sum(NUM_PAT):Q',
                                title='Cumulative Volume',
                                scale=alt.Scale(domain=[0, left_max_horizontal]),
                                sort='descending'
                               ),
                        color=alt.Color('ACUITY_LEVEL_with_count:N', 
                                          scale=color_scale, 
                                          legend=alt.Legend(title='Acuity Level Volumes', 
                                                            orient='left', 
                                                            labelFontSize=14, 
                                                            titleFontSize = 16)
                                         )
                    ).mark_bar(align='right', 
                               size=5
                    ).properties(height=700,
                                 title = {'text':left_prov_name, 
                                          'subtitle':[left_dept_dict[left_department],' '],
                                          'anchor':'middle',
                                         }
                    )
    
    return left


# In[7]:


def build_middle_ed_age_dept_acuity_graph(middle_data):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Now we build the middle graph. This is graph will be a vertical graph 
    of numbers counted by 5 in the labels (i.e., 0, 5, 10, 15, ...) all the
    way up to the maximum (which is currently 105). These values represent 
    ages of patients, and age are ordered with 0 at the top down to 105.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
            
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    An altair chart.
    
    
    '''
    
    middle_data=middle_data.copy(deep=True)
    
    # Set up the unique age labels for the graph. 
    unique_age_labels=middle_data[['AGE_AT_ADMISSION','AGE_AT_ADMISSION_nominal','AGE_AT_ADMISSION_label']].copy()
    unique_age_labels=unique_age_labels.drop_duplicates().sort_values(by='AGE_AT_ADMISSION', ascending=True)

    # Build the graph.
    middle=alt.Chart(unique_age_labels
                    ).encode(
                        y=alt.Y('AGE_AT_ADMISSION_nominal:N', 
                                sort=sorted(list(middle_data['AGE_AT_ADMISSION'].sort_values(ascending=True).unique()),
                                              reverse=True),
                                axis=None),
                        text=alt.Text('AGE_AT_ADMISSION_label:N'),
                    ).mark_text(fontSize=14).properties(width=8).properties(height=700, title={'text':'Age'
                                                                                     })
    
    return middle


# In[8]:


def build_right_ed_age_dept_acuity_graph(right_data,
                                         right_department,
                                         right_max_horizontal,
                                         right_dept_dict):
    '''
    Build the graph for this filtered dataframe; this will be the right graph
    of the three in the final picture. The result will be a vertical bar 
    graph, where one level represents one age category, and each level is 
    colored by the acuity level.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    right_data
        This is a dataframe containing all of the initial data. 
    
    right_department
        This is a department name you want to display on the left side of a 
        graph. 
    
    right_max_horizontal
        This is the largest value to be displayed on the graph, autorounded 
        to the next appropriate increment (for instance, if 
        left_max_horizontal is 6, the display will round to 10).
    
    right_dept_dict
        Despite the name, this is a dataframe containing the department name 
        in the index and the (department name with volume label) in the only
        column. Effectively, think of this like a pd.Series. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    An altair chart.
    
    
    '''
    
    # Create a filtered dataframe for one ed.
    right_data=right_data.copy(deep=True)
    right_data=right_data.drop(right_data[right_data['DEPARTMENT_NAME']!=right_department].index)
    right_prov_name=right_data['PROV_NAME'].unique()[0]

    # Set the coloring properties of this filtered dataframe. This wil match
    # the coloring scheme from the graph on the left given above. 
    color_scale=alt.Scale(domain=list(right_data['ACUITY_LEVEL_with_count'].unique()),
                            range=['#dc050c','#f6c141','#4eb265','#1965b0','#882e72','#000000'])
    
    # Build the graph for this filtered dataframe; this will be the right graph
    # of the three in the final picture. The result will be a vertical bar 
    # graph, where one level represents one age category, and each level is 
    # colored by the acuity level.
    right=alt.Chart(right_data
                     ).transform_filter(alt.datum.DEPARTMENT_NAME==right_department
                    ).encode(
                        y=alt.Y('AGE_AT_ADMISSION_nominal:N', 
                                sort=sorted(list(right_data['AGE_AT_ADMISSION'].sort_values(ascending=True).unique()), reverse=True),
                                axis=alt.Axis(orient='left',
                                                title=None, 
                                                labels=False)
                               ),
                        x=alt.X('sum(NUM_PAT):Q',
                                title='Cumulative Volume',
                                scale=alt.Scale(domain=[0, right_max_horizontal])
                               ),
                        color=alt.Color('ACUITY_LEVEL_with_count:N', 
                                          scale=color_scale, 
                                          legend=alt.Legend(title='Acuity Level Volumes', 
                                                            labelFontSize=14, 
                                                            titleFontSize=16)
                                         )
                    ).mark_bar(size=5
                    ).properties(height=700,
                                 title = {'text':right_prov_name, 
                                          'subtitle':[right_dept_dict[right_department],' '],
                                          'anchor':'middle',
                                         }
                    )
    
    return right


# In[9]:


def build_final_ed_age_dept_acuity_graph_wo_comp(left_final,
                                                 middle_final,
                                                 right_final,
                                                 first_date_final,
                                                 last_date_final
                                                ):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function assembles a six-part altair graph with the structure 
    described below. Letters correspond to actual variable names, and the 
    numbers help you think about those variables in terms of position and 
    grouping. 
        (left | middle | right)
        alternatively, position number
        ( 1 |  2 |  3) 
    The intent of this function is to include either (i) two separate 
    departments in one chart, or (ii) one department and its' corresponding
    comparison chart.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    left_final
        This parameter is required. This is the position 1 piece in the graph. 
        Another way to think about it is the left third of the graph.
    
    middle_final
        This parameter is required. This is the position 2 piece in the graph. 
        Another way to think about it is the middle third of the graph.
    
    right_final
        This parameter is required. This is the position 3 piece in the graph. 
        Another way to think about it is the right third of the graph.
    
    first_date_final
        This parameter is required. This value represents the earliest date in 
        the data set. 
    
    last_date_final
        This parameter is required. This value represents the last date in 
        the data set. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    An altair chart with final formatting.
            
            
    '''
    
    title_name='Provider ED Volumes by Department, Age and Acuity'
    
    # Finally, we build the final chart. This concatenates the three charts 
    # (left, middle, and right) and sets the global properties of the final
    # chart. This code also there are two distinct legends, one for each ED.
    # This multiple legend is important because acuity volumes for each 
    # facility are different. 
    final_chart=alt.concat(left_final, 
                             middle_final, 
                             right_final, 
                             spacing=0
                              ).configure_view(strokeWidth=0
                              ).configure_axis(labelFontStyle='normal', 
                                               labelFontSize=14, 
                                               titleFontSize=16
                              ).configure_legend(labelLimit=0,titleLimit=0
                              ).properties(title = {'text':title_name, 
                                                    'subtitle':['Date Range: ' + first_date_final + ' - ' + last_date_final,' '],
                                                    'fontSize':24, 
                                                    'subtitleFontSize':14,
                                                    'anchor':'middle',
                                                   }
                              ).resolve_scale(color='independent'
                              ).resolve_legend(color='independent'
                              ).configure_title(fontSize=16
                              )
    
    return final_chart


# In[10]:


def build_final_ed_age_dept_acuity_graph_w_comp(ll_final,
                                                lm_final,
                                                lr_final,
                                                rl_final,
                                                rm_final,
                                                rr_final,
                                                first_date_final,
                                                last_date_final
                                               ):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function assembles a six-part altair graph with the structure 
    described below. Letters correspond to actual variable names, and the 
    numbers help you think about those variables in terms of position and 
    grouping. 
        (ll | lm | lr) | (rl | rm | rr)
        alternatively, position number
        ( 1 |  2 |  3) | ( 4 |  5 |  6)
    The intent of this function is to include a pair of comparison functions.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    ll_final
        This parameter is required. This is the position 1 piece in the graph. 
        Another way to think about it is the left graph of the left half.
    
    lm_final
        This parameter is required. This is the position 2 piece in the graph. 
        Another way to think about it is the middle graph of the left half.
    
    lr_final
        This parameter is required. This is the position 3 piece in the graph. 
        Another way to think about it is the right graph of the left half.
    
    rl_final
        This parameter is required. This is the position 4 piece in the graph. 
        Another way to think about it is the left graph of the right half.
    
    rm_final
        This parameter is required. This is the position 5 piece in the graph. 
        Another way to think about it is the middle graph of the right half.
    
    rr_final
        This parameter is required. This is the position 6 piece in the graph. 
        Another way to think about it is the right graph of the right half.
    
    first_date_final
        This parameter is required. This value represents the earliest date in 
        the data set. 
    
    last_date_final
        This parameter is required. This value represents the last date in the 
        data set. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    An altair chart with final formatting.
    
    
    '''
    
    title_name='Provider ED Volumes by Department, Age and Acuity'
    
    # Finally, we build the final chart. This concatenates the three charts 
    # (left, middle, and right) and sets the global properties of the final
    # chart. This code also there are two distinct legends, one for each ED.
    # This multiple legend is important because acuity volumes for each 
    # facility are different. 
    final_chart=alt.concat(ll_final, 
                           lm_final, 
                           lr_final,
                           rl_final, 
                           rm_final, 
                           rr_final,
                           spacing=0
                          ).configure_view(strokeWidth=0
                          ).configure_axis(labelFontStyle='normal', 
                                           labelFontSize=14, 
                                           titleFontSize=16
                          ).configure_legend(labelLimit=0,titleLimit=0
                          ).properties(title = {'text':title_name, 
                                                'subtitle':['Date Range: ' + first_date_final + ' - ' + last_date_final,' ',' ',' '],
                                                'fontSize':24, 
                                                'subtitleFontSize':14,
                                                'anchor':'middle',
                                               }
                          ).resolve_scale(color='independent'
                          ).resolve_legend(color='independent'
                          ).configure_title(fontSize=16
                          )
    
    return final_chart


# In[11]:


def save_altair_graph_as_png(id_for_title,
                             primary_graph,
                             comparison_graph
                            ):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Saves an altair graph to a png file via an HTML file. 
    
    This function DOES NOT rely on altair_saver with selenium or chromedriver 
    extensions/backends. This simplifies installation requirements and will
    work nicely on any system.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    id_for_title
        This parameter is required. This value represents the first part of 
        the file title you want to use. 
        
    primary_graph
        This parameter is required. This is an altair graph in its' final
        state before saving. 
    
    comparison_graph
        This parameter is required. This value represents a category value 
        ('yes'/'no'/'generic') that adjusts the crop to an appropriate size.
        If this function is used / altered for any other purpose than this 
        file, the crop values in this function will need to be adjusted.
    
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function returns None. This function saves an HTML file.   
    
    
    '''
    
    # Save the altair graph to an HTML file.
    html_title='{}_ed_age_department_acuity_graph.html'.format(id_for_title)
    png_title='{}_ed_age_department_acuity_graph.png'.format(id_for_title)
    if comparison_graph=='no':
        primary_graph.save(html_title)
        width_value=1500
        height_value=870
    else:
        fg=primary_graph
        fg.save(html_title)
        width_value=3000
        height_value=870
    
    # Convert that HTML file to a png.
    html_file_to_png(file_to_convert=html_title,
                     output_file=png_title,
                     width_of_screenshot=width_value,
                     height_of_screenshot=height_value)
    
    # Remove HTML file.
    (pathlib.Path.cwd() / html_title).unlink()
    
    # Crop the png file.
    crop_the_png_file(png_title)
    
    return None
    


# In[12]:


def html_file_to_png(file_to_convert,output_file,width_of_screenshot,height_of_screenshot):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function screen shots an HTML file. 
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    file_to_convert
        This parameter is required. This represents the name of the HTML file
        we need to convert to a png. 
    
    output_file
        The parameter is required. This represents the name of the png file 
        that is created.
    
    width_of_screenshot
        This parameter is required. This represents the width of the 
        screenshot.
    
    height_of_screenshot
        This parameter is required. This represents the height of the 
        screenshot.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function returns None. This function save a png file. 
            
    
    '''
    
    hti = Html2Image()
    hti.screenshot(html_file=file_to_convert,
                   size=(width_of_screenshot,height_of_screenshot),
                   save_as=output_file)
    return None


# In[13]:


def crop_the_png_file(png_file_title):
    '''
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Description
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function crops a png file to an outer boundary of white pixels.
    
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    Parameters
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    png_file_title
        This parameter is required. The title of the png file we want to crop.
            
    
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    return / save
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
    This function returns None. This function saves the cropped png by 
    replacing the orignal png file (meaning the original png file is 
    destroyed and cannot be recovered).
    
    For instance, if an x is a non-white pixel and o is a white pixel
    
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxooooxoooooooxooooooooooooooooooxoooooooooooooxxxxxxxxxxxxxx
    xxxooooooooxooooooooooooxooooooooooooxooooooooooxxxxxxxxxxxxxx
    xxxooooooxxxooooooooooooooooxxxxxoooooooooooooooxxxxxxxxxxxxxx
    xxxooooooooooooooooooooooooxxxxxxxxxxxxxxoooooooxxxxxxxxxxxxxx
    xxxooooooooooooooooooooooooooooooooooooooxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    this function will save the following cropped png image 
    
    ooooxoooooooxooooooooooooooooooxooooooooooooo
    ooooooooxooooooooooooxooooooooooooxoooooooooo
    ooooooxxxooooooooooooooooxxxxxooooooooooooooo
    ooooooooooooooooooooooooxxxxxxxxxxxxxxooooooo
    ooooooooooooooooooooooooooooooooooooooxxxxxoo
    
    
    '''
    # Read image.
    img=cv2.imread(png_file_title)
    
    # Convert image to HSV color space from BGR color space.
    gray=cv2.cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    gray=cv2.GaussianBlur(gray,(5,5),0)
    
    # Set color thresholds.
    retval,thresh=cv2.threshold(gray,210,255,cv2.THRESH_BINARY)
    
    # Grab the pixels in the threshold
    mask=Image.fromarray(thresh)
    
    # Return the upper left and lower right corners. This is a tuple of 
    # (left x, left upper y, right x, right lower y) representing the color
    # pixels.
    crop_box=mask.getbbox()
    
    # We need to reload image to preserve original colors.
    img=Image.open(png_file_title) 
    
    # Crop and save.
    img=img.crop(crop_box)
    img.save(png_file_title)
    
    return None


# ed_data=pd.read_excel('ed_ages_2.xlsx')

# In[14]:


graph=generate_ed_age_department_acuity_graph(data='example',
                                              person_id=12214386,
                                              department_1='TFH EMERGENCY DEPARTMENT',
                                              department_2='TFH EMERGENCY DEPARTMENT',
                                              compare='no', 
                                              configuration='together',
                                              config_dept='department_2')
graph


# In[ ]:




