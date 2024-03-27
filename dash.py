import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NetflixDashboard", page_icon=":bar_chart:", layout="wide")

# Netflix colors
primary_red = '#ff0000'
red1 = '#ae123a'
red2 = '#fb9984'

# Adding CSS style to center and justify text
st.markdown(
    """
    <style>
        /* Center text */
        .stMarkdown {
            text-align: center;
        }
        .stMarkdown h2 {
            color: white;
            background-color: red;
            border-radius: 5px;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Importing data
data = pd.read_excel('netflix_titles.xlsx')

# Displaying Netflix logo and title on the same line
st.write("<style>div.Widget.row-widget.stRadio > div{flex-direction:row; justify-content:center;}</style>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=200)
with col2:
    st.markdown("<h1 style='text-align: left;'>📊📈Netflix Dashboard</h1>", unsafe_allow_html=True)

# Displaying first few rows of the Netflix dataset
st.write("<p style='text-align: left;'>Netflix Dataset Overview:</p>", unsafe_allow_html=True)
st.write(data.head())

col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    # Select unique program types
    program_types = data['type'].unique()
    # Select programs corresponding to selected type
    selected_type = st.selectbox("Select Program Type", program_types)
    # Filter data to include only programs of selected type
    filtered_data = data[data['type'] == selected_type]
    # Select a specific program of the selected type
    selected_program = st.selectbox("Select Program", filtered_data['title'])
    # Display details of the selected program
    program_details = filtered_data[filtered_data['title'] == selected_program].squeeze()
with col2:
    st.markdown('<h2 style="background-color:#FF0000;color:#FFFFFF;padding:1px;text-align:center;">Description</h2>', unsafe_allow_html=True)
    st.write(program_details['description'])
with col3:
    st.markdown('<h2 style="background-color:#FF0000;color:#FFFFFF;padding:1px;text-align:center;">Genre</h2>', unsafe_allow_html=True)
    st.write(program_details['listed_in'])
with col4:
    st.markdown('<h2 style="background-color:#FF0000;color:#FFFFFF;padding:1px;text-align:center;">Rating</h2>', unsafe_allow_html=True)
    st.write(program_details['rating'])
with col5:
    st.markdown('<h2 style="background-color:#FF0000;color:#FFFFFF;padding:1px;text-align:center;;">Duration</h2>', unsafe_allow_html=True)
    st.write(program_details['duration'])
with col6:
    st.markdown('<h2 style="background-color:#FF0000;color:#FFFFFF;padding:1px;text-align:center;">Release Year</h2>', unsafe_allow_html=True) 
    st.write(f"Release Year: {program_details['release_year']}")

col1, col2, col3= st.columns([1,1,1])

### Visualization 1
with col1:
    # Analyze different values of the "rating" variable
    ratings_counts = data['rating'].value_counts()
    # Create bar chart
    fig = px.bar(x=ratings_counts.index, y=ratings_counts.values, 
                labels={'x': 'Age Rating', 'y': 'Number of Titles'},
                title='Distribution of Age Ratings for Netflix Titles')
    fig.update_layout(xaxis={'categoryorder': 'total descending'})  # Order categories by total count descending
    fig.update_traces(marker_color=primary_red)
    fig.update_traces(text=ratings_counts.values.round(2), textposition='outside')
    fig.update_layout(width=450, height=400)
    st.plotly_chart(fig)

### Visualization 2
with col2:
    # Count the number of programs released each year for each type
    programs_released_by_year_type = data.groupby(['release_year', 'type']).size().reset_index(name='Count')
    # Filter data to include only years starting from 2000
    programs_released_by_year_type = programs_released_by_year_type[programs_released_by_year_type['release_year'] >= 2000]
    # Create line chart
    fig = px.area(programs_released_by_year_type, x='release_year', y='Count', color='type', 
                title='Number of Programs Released by Year and Type',
                labels={'release_year': 'Release Year', 'Count': 'Programs Released', 'type': 'Type'},
                color_discrete_map={'Movie': red1, 'TV Show': red2},
                hover_data={'release_year': True, 'Count': True, 'type': True})
    fig.update_layout(width=450, height=400)
    st.plotly_chart(fig)


### Visualization 3
with col3:
    # Count the number of movies and TV shows
    type_counts = data['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    # Calculate percentages
    total = type_counts['Count'].sum()
    type_counts['Percentage'] = (type_counts['Count'] / total) * 100
    # Create text for treemap (type name and count)
    type_counts['Text'] = 'Count: ' + type_counts['Count'].astype(str) + '<br>' + \
                        'Percentage: ' + type_counts['Percentage'].round(2).astype(str) + '%'
    # Create treemap chart for distribution of program types
    fig = px.treemap(type_counts, path=['Type'], values='Count', 
                    color='Type', color_discrete_map={'Movie': red1, 'TV Show': red2},
                    title='Distribution of Program Types on Netflix',
                    custom_data=['Text'])
    # Show text on treemap
    fig.update_traces(text=fig.data[0]['customdata'])
    fig.update_traces(root_color="black")
    fig.update_layout(width=450, height=400)
    st.plotly_chart(fig)
    
col1, col2 = st.columns([1, 1])

### Visualization 4
with  col1:
    # Split genres for each title and stack them into a new DataFrame
    genre_df = data['listed_in'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename('genre')
    genre_df = data.drop('listed_in', axis=1).join(genre_df).reset_index(drop=True)
    # Count occurrences of each genre
    top_genres = genre_df['genre'].value_counts().reset_index(name='Count')
    # Select the top 10 most frequent genres
    top_10_genres = top_genres.head(10)
    # Create horizontal bar chart
    fig = px.bar(top_10_genres, x='Count', y=top_10_genres.index, orientation='h',
                title='Top 10 Genres on Netflix',
                labels={'index': 'Genre', 'Count': 'Number of Titles'})
    fig.update_traces(marker_color=primary_red)
    fig.update_traces(text=top_10_genres['Count'], textposition='outside')
    fig.update_layout(width=700, height=400)
    st.plotly_chart(fig)

### Visualization 5
with  col2:
    # Split multiple country entries for each title and stack them into a new DataFrame
    country_df = data['country'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename('country')
    country_df = data.drop('country', axis=1).join(country_df).reset_index(drop=True)
    # Count the number of programs per country
    country_counts = country_df['country'].value_counts().reset_index(name='Count')
    # Create chloropleth map for the number of programs per country
    fig = px.choropleth(country_counts, locations=country_counts.index, locationmode='country names', color='Count',
                        hover_name=country_counts.index,
                        projection='natural earth',
                        labels={'Count': 'Number of Programs'},
                        title='Distribution of Netflix Programs by Country',
    )
    # Customize the appearance of the map for a black background
    fig.update_layout(
        geo=dict(
            bgcolor='#111',
            showcountries=True,
            showcoastlines=True
        ),
        coloraxis_colorbar=dict(
            title='Number of Programs',
            tickvals=[country_counts['Count'].min(), (country_counts['Count'].max()/2).round(), 1],
            ticktext=[str(country_counts['Count'].max()), str((country_counts['Count'].max()/2).round()), '1'],
            tickfont=dict(color='white'),
        ),
        coloraxis=dict(
            colorscale=[[0, '#8B0000'], [1, red2]], 
        )
    )
    # Show the chloropleth map in Streamlit
    st.plotly_chart(fig)

st.markdown(
    """
    <div style='text-align: center;'>
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" width="200">
    </div>
    """,
    unsafe_allow_html=True
)





