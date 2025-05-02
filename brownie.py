import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 

st.title('America’s Test Kitchen Recipes: Brownies, Bars, and More')

st.write("This is an app built from data scraped from [America's Test Kitchen](https://www.americastestkitchen.com/search?q=brownies)." )

data = pd.read_csv('brownie_recipes.csv') 
#st.dataframe(data, hide_index=True)

recipes_list = np.sort(data['Title'].unique())

recipes_list = np.insert(recipes_list, 0, "All Recipes")

#________

col1, col2, col3, col4, col5 = st.columns([0.2,0.2,0.2,0.2,0.2])
with col1:
    st.text("Type of Recipe:") 
with col2:
    brownie_reci = st.checkbox('Brownies', value=True)
with col3:
    bar_reci = st.checkbox('Bars', value=True)
with col4:
    other_reci = st.checkbox ('Other', value = True)
with col5:
    all_reci = st.checkbox ('All', value= True)


#----------mine

if all_reci:
    filtered_data = data  
else:
    masks = []

    if brownie_reci:
        masks.append(data['Title'].str.contains(r'brownie', flags=re.IGNORECASE, na=False))
    if bar_reci:
        masks.append(data['Title'].str.contains(r'bar', flags=re.IGNORECASE, na=False))
    if other_reci:
        masks.append(~data['Title'].str.contains(r'(bar|brownie)', flags=re.IGNORECASE, na=False))

    if masks:
        combined_mask = masks[0]
        for m in masks[1:]:
            combined_mask |= m
        filtered_data = data[combined_mask]
    else:
        filtered_data = pd.DataFrame(columns=data.columns)  
#_________

left_col,mid_col, right_col = st.columns([.48 ,.02 ,.5])  

with right_col:
    fig, ax = plt.subplots()
    ax.hist(data['Ingredient Count'].dropna(), bins=14, color='orange', edgecolor='black')
    ax.set_xlabel('Number of Ingredients')
    ax.set_ylabel('Number of Recipes')
    ax.set_title('Distribution of Ingredient Count')
    
    st.pyplot(fig)


#_________
with left_col:

    numeric_cols = ["Review Rating", "Review Count", "Ingredient Count", "Bake and Prep Time", "Cool Time"]
    for col in numeric_cols:
        filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')

    if not filtered_data.empty:

        rating_range = st.slider(
            "Select a range of review ratings",
            value=(0.0, 5.0),
            step=0.1)

        review_count_range = st.slider(
            "Select a range of Review Counts",
            value=(0.0, 850.0),
            step=0.1)


        ingredient_range = st.slider(
            "Select a range of Ingredients",
            value = (0.0, 21.0),
            step= 0.1)


        bake_prep_range = st.slider(
            "Select a range of bake and prep time in min",
            value = (0.0, 165.0),
            step= 0.1)

        with right_col:
            cool_time_range = st.slider(
                "Select a range of cool time in min",
                value = (0.0, 315.0),
                step= 0.1)

    filtered_data = filtered_data[
        (filtered_data["Review Rating"] >= rating_range[0]) & (filtered_data["Review Rating"] <= rating_range[1]) &
        (filtered_data["Review Count"] >= review_count_range[0]) & (filtered_data["Review Count"] <= review_count_range[1]) &
        (filtered_data["Ingredient Count"] >= ingredient_range[0]) & (filtered_data["Ingredient Count"] <= ingredient_range[1]) &
        (filtered_data["Bake and Prep Time"] >= bake_prep_range[0]) & (filtered_data["Bake and Prep Time"] <= bake_prep_range[1]) &
        (filtered_data["Cool Time"] >= cool_time_range[0]) & (filtered_data["Cool Time"] <= cool_time_range[1])]


st.dataframe(filtered_data, hide_index=True)
