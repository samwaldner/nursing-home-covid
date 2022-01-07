import streamlit as st
import pandas as pd

lookup = pd.read_csv('../data/lookup.csv')
df = pd.read_csv('../data/for_user.csv')

page = st.selectbox("Choose your page", ["Overview", "FAQ", "Nursing Home Finder"]) 

if page == "Overview":
    st.title('Project 5: Predicting Covid Deaths in Nursing Homes')
    st.subheader('By: Shirley Lin, Jamie Squires, Sam Waldner')
    st.markdown("***")
    st.markdown('US Government oversight is comprehensive in how it scores and evaluates nursing homes. However, they have yet to incorporate any COVID related data into these scores. This web-app concept is part of a project that aimed to predict COVID deaths in nursing homes based on a wide variety of features provided by the US Governemnt. We hypothesized incorrectly that the overall safety, sanitation, and operational efficiency of a nursing home was indicative of how COVID affected each specific nursing homes. With the data we had available there was not enough evidence to disprove the null hypothesis; however, we concluded that any information relating to COVID is still an important decision-making tool for people looking to find a safe nursing home for their loved ones.')
    st.markdown('If you navigate to the next page you will find an intuitive tool that can be used by anyone to see the nursing homes available in their area with basic safety and COVID information included. If there are any Government listed nursing home facilities in your ZIP code, it will return some of the safer ones in that state.')
    st.markdown('Below we can see the coefficients from a LinearRegression attempting to predict COVID deaths using Government data. We can interpret this as for every one unit increase in a feature, deaths either increase or decrease by the supplied amount. It is clear that the supplied data is insufficient, and because COVID data is **not** used in the "Overall Score" that is carefully constructed through Government regulation we have created this tool for the average consumer to use.')
    st.image('../data/coefficients3.png', caption='Coefficients Affecting Covid Deaths in Nursing homes')
    
    
    
elif page == "FAQ":
    st.title('FAQ')
    st.markdown("***")

    
    st.markdown('### 1. What is the Five Star Rating?')
    st.markdown('The Five Star Rating is based on three factors: Staffing (number of staff and hours they work), QM (Quality Measure or measureing improvement over time), and Health Inspections. Much of the information that goes into these ratings is self-reported which causes significant reliability problems. Further, while the Five Star Rating is good basic indicator of quality, it is graded on a curve per state. In other words, a 5-star nursing home in Illinois will have a completely different set of standards and past record from a 5-star nursing home in California.')
    st.markdown('"CMS bases Five-Star quality ratings in the health inspection domain on the relative performance of facilities within a state...The top 10 percent (with the lowest health inspection weighted scores) in each state receive ahealth inspection rating of five stars." While this practice makes sense under current systems, it leaves a wide margin of difference between a 5-star home between states.')
    
    st.markdown('### 2. How does COVID play into the rating?')
    st.markdown('Despite the extended nature of the pandemic, none of the state or federal regulatory measures takes vaccinations, past cases, or past deaths into account when deciding rating. This is short-sighted and limits the decision-making abilities of people looking at potential homes.')
    
    st.markdown('### 3. Does it matter which state the home is in?')
    st.markdown('State location matters! Two predictive studies have been done, one for California and one for West Virgina that both attempt to predict COVID impact in nursing homes, and the studies each found opposite results. California found an inverse relationship between star ratings and COVID deaths, while West Virgina found a postitive relationship. This means impact between states is volatile and is worth serious consideration.')
                
    st.markdown('### 4. How about the size of the facility?')
    st.markdown('According to our research, size of facility only has a slight impact on COVID-related deaths and cases. While definitely something worth considering, this should not be the main factor of choosing or not choosing a facility if COVID is your primary concern.')
    
    st.markdown('### 5. Why bother with this app if the government has something similar already?')
    st.markdown('Great Question! The [Medicare Compare Tool](https://www.medicare.gov/care-compare/) is a great tool that you should definitely check out. We feel that a lot of the information is hard to interpret, and does not include everything that it should include, such as annual reported COVID deaths and cases. Our tool (including this FAQ!) is meant to help interpret and compile all the information for ease of use. Also, in order to understand the star ratings, the Governemnt provides a dense 30-page technical user manual breaking it down. While extremely informative, we thought a more straightforward explanation could be helpful.')
                
    st.subheader('Sources:')
    st.markdown(' - Bui, David P, et al. “Association between CMS Quality Ratings and Covid-19 Outbreaks in Nursing Homes - West Virginia, March 17-June 11, 2020.” MMWR. Morbidity and Mortality Weekly Report, Centers for Disease Control and Prevention, 18 Sept. 2020, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7498166/.')
    st.markdown(' - Predicting Covid-19 at Skilled Nursing ... - BMJ Open Quality. https://bmjopenquality.bmj.com/content/bmjqir/10/1/e001099.full.pdf.')
    st.markdown(' - “Quality, Safety & Oversight - Certification &amp; Compliance.” CMS, https://www.cms.gov/Medicare/Provider-Enrollment-and Certification/CertificationandComplianc.')
    
elif page == "Nursing Home Finder":


    st.title('Which nursing homes are in your area?')

    zipcode = st.number_input('Whats your zip?', min_value=None, max_value=99999, format='%d')


    if zipcode == 0:
        print('')

    elif len(df[df['Provider Zip Code']==zipcode]) != 0:

        st.write('These are the nursing homes in your area:')

        new_df=df[df['Provider Zip Code']==zipcode]

        successful= new_df.loc[(df['Overall Rating']==5)
    #               (df['2021_cases_per_1000'] <= 50) & 
    # #                (df['2021_cases_per_1000'] > 0) &
    #                (df['2021_deaths_per_1000'] <= 50)
    #                (df['2021_deaths_per_1000'] > 0)
                 ][:5]

        st.table(data=new_df[['Provider Name','Provider State','Ownership Type','Number of Certified Beds','Overall Rating','Health Inspection Rating','QM Rating','Staffing Rating','2021 Covid Cases','2021 Covid Deaths']].sort_values(by = ['Overall Rating','2021 Covid Deaths','2021 Covid Cases'],ascending=[False,True,True]))

    elif len(lookup[lookup['zip']==zipcode]['Provider State'])==0:    
        st.write('Sorry that ZIP code does not exist.' )
        
    else:
        state = lookup[lookup['zip']==zipcode]['Provider State'].values
        st.write('Sorry, no data available for your ZIP code...')
        st.write(f'Checkout some of the safest nursing homes in {state[0]} instead!')


        new_df2 = df[df['Provider State']==state[0]]

        failed = new_df2.loc[(df['Overall Rating']==5) 
    #               (df['2021_cases_per_1000'] <= 50) & 
    # #                (df['2021_cases_per_1000'] > 0) &
    #                (df['2021_deaths_per_1000'] <= 50)
    #                (df['2021_deaths_per_1000'] > 0)
                 ][:10]

        st.table(data=failed[['Provider Name','Provider State','Ownership Type','Number of Certified Beds','Overall Rating','Health Inspection Rating','QM Rating','Staffing Rating','2021 Covid Cases','2021 Covid Deaths']].sort_values(by=['2021 Covid Deaths','2021 Covid Cases'],ascending=True))

