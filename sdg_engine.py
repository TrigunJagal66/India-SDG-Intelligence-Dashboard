import pandas as pd
import numpy as np





feature_direction = {

    # Poverty & Inequality (Lower is Better)
    "population_in_the_lowest_two_wealth_quintiles_percent": "negative",
    "head_count_ratio_as_per_the_multidimensional_poverty_index_percent": "negative",
    "population_living_below_the_national_poverty_line_percent": "negative",

    # Financial Inclusion (Higher is Better)
    "automated_teller_machines_atms_per_1_00_000_population": "positive",
    "functioning_branches_of_commercial_banks_per_1_00_000_population": "positive",

    # Connectivity (Higher is Better)
    "mobile_connections_per_100_persons_mobile_tele_density_as_per_deptof_telecommunications": "positive",
    "lpg_png_connections_against_number_of_households_as_per_mopng_calculations_as_on_31072020_percent": "positive",

    # Education (Higher is Better)
    "schools_with_access_to_basic_infrastructure_such_as_electricity_drinking_water_percent": "positive",
    "gross_enrolment_ratio_ger_in_higher_secondary_for_classes_11_to_12": "positive",
    "students_in_grade_viii_achieving_atleast_a_minimum_proficiency_level_in_terms_of_nationally_defined_learning_outcomes_to_be_attained_by_the_pupils_at_the_end_of_the_grade_percent": "positive",
    "gross_enrolment_ratio_ger_in_higher_education_in_the_age_group_of_18_to_23_years": "positive",
    "persons_with_disability_completed_at_least_secondary_education_with_age_15_years_and_above_percent": "positive",
    
    
    
    # Education (Lower is Better)
    
    
    "average_annual_dropout_rate_at_secondary_level_for_classes_9_to_10": "negative",

    # Health (Lower is Better)
    "maternal_mortality_ratio_per_1_00_000_live_births": "negative",
    "human_immunodeficiency_virus_hiv_incidence_per_1_000_uninfected_population": "negative",
    "anaemic_adolescents_in_the_age_group_of_10_to_19_years_percent": "negative",
    "mortality_rate_per_1_000_live_births_under_5_years_of_age": "negative",

    # Employment & Gender (Higher is Better)
    "ratio_of_female_to_male_labour_force_participation_rate_lfpr_in_the_age_group_of_15_to_59_years": "positive",
    "labour_force_participation_rate_lfpr_percent_in_the_age_group_of_15_to_59_years": "positive",
    "operational_land_holding_gender_wise_percentage_of_female_operated_operational_holdings_percent": "positive",

    # Environment & Sustainability
    "industries_complying_with_wastewater_treatment_17_categories_of_highly_polluting_industries_or_grossly_polluting_or_red_category_of_industries_complying_with_wastewater_treatment_percent": "positive",
    "per_capita_fossil_fuel_consumption": "negative",

    # Safety (Lower is Better)
    "deaths_due_to_road_accidents_in_urban_areas_per_1_00_000_population": "negative",
    "death_rate_due_to_road_traffic_accidents_per_1_00_000_population": "negative",

    # Economy (Higher is Better)
    "gross_value_added_constant_prices_in_agriculture_per_worker": "positive"
}

feature_names = {

    "population_in_the_lowest_two_wealth_quintiles_percent":
        "Population in Lowest Two Wealth Quintiles",

    "head_count_ratio_as_per_the_multidimensional_poverty_index_percent":
        "Multidimensional Poverty Index (MPI)",

    "population_living_below_the_national_poverty_line_percent":
        "Population Below Poverty Line",

    "automated_teller_machines_atms_per_1_00_000_population":
        "ATMs per 100,000 Population",

    "functioning_branches_of_commercial_banks_per_1_00_000_population":
        "Commercial Bank Branches",

    "mobile_connections_per_100_persons_mobile_tele_density_as_per_deptof_telecommunications":
        "Mobile Connections per 100 Persons",

    "schools_with_access_to_basic_infrastructure_such_as_electricity_drinking_water_percent":
        "Schools with Basic Infrastructure",

    "gross_enrolment_ratio_ger_in_higher_secondary_for_classes_11_to_12":
        "Higher Secondary Enrolment Ratio",

    "industries_complying_with_wastewater_treatment_17_categories_of_highly_polluting_industries_or_grossly_polluting_or_red_category_of_industries_complying_with_wastewater_treatment_percent":
        "Industries Complying with Wastewater Treatment",

    "maternal_mortality_ratio_per_1_00_000_live_births":
        "Maternal Mortality Ratio",

    "ratio_of_female_to_male_labour_force_participation_rate_lfpr_in_the_age_group_of_15_to_59_years":
        "Female to Male Labour Participation Ratio",

    "human_immunodeficiency_virus_hiv_incidence_per_1_000_uninfected_population":
        "HIV Incidence Rate",

    "anaemic_adolescents_in_the_age_group_of_10_to_19_years_percent":
        "Anaemic Adolescents",

    "average_annual_dropout_rate_at_secondary_level_for_classes_9_to_10":
        "Secondary School Dropout Rate",

    "students_in_grade_viii_achieving_atleast_a_minimum_proficiency_level_in_terms_of_nationally_defined_learning_outcomes_to_be_attained_by_the_pupils_at_the_end_of_the_grade_percent":
        "Grade VIII Learning Proficiency",

    "per_capita_fossil_fuel_consumption":
        "Per Capita Fossil Fuel Consumption",

    "gross_enrolment_ratio_ger_in_higher_education_in_the_age_group_of_18_to_23_years":
        "Higher Education Enrolment Ratio",

    "mortality_rate_per_1_000_live_births_under_5_years_of_age":
        "Under-5 Mortality Rate",

    "deaths_due_to_road_accidents_in_urban_areas_per_1_00_000_population":
        "Urban Road Accident Deaths",

    "persons_with_disability_completed_at_least_secondary_education_with_age_15_years_and_above_percent":
        "Secondary Education among Persons with Disability",

    "labour_force_participation_rate_lfpr_percent_in_the_age_group_of_15_to_59_years":
        "Labour Force Participation Rate",

    "operational_land_holding_gender_wise_percentage_of_female_operated_operational_holdings_percent":
        "Female Operated Land Holdings",

    "death_rate_due_to_road_traffic_accidents_per_1_00_000_population":
        "Road Traffic Accident Death Rate",

    "gross_value_added_constant_prices_in_agriculture_per_worker":
        "Agricultural Productivity per Worker",

    "lpg_png_connections_against_number_of_households_as_per_mopng_calculations_as_on_31072020_percent":
        "LPG/PNG Household Coverage"
}


recommendation_map = {

    # Poverty & Inequality
    "population_in_the_lowest_two_wealth_quintiles_percent":
        "Improve income generation opportunities and strengthen social welfare programs for economically weaker households.",

    "head_count_ratio_as_per_the_multidimensional_poverty_index_percent":
        "Improve access to healthcare, education, housing, sanitation, and other basic services.",

    "population_living_below_the_national_poverty_line_percent":
        "Strengthen poverty alleviation, livelihood generation, and employment programs.",

    # Financial Inclusion
    "automated_teller_machines_atms_per_1_00_000_population":
        "Increase ATM penetration and improve access to formal banking services.",

    "functioning_branches_of_commercial_banks_per_1_00_000_population":
        "Expand banking infrastructure and financial inclusion initiatives.",

    # Connectivity
    "mobile_connections_per_100_persons_mobile_tele_density_as_per_deptof_telecommunications":
        "Improve telecom infrastructure and digital connectivity.",

    "lpg_png_connections_against_number_of_households_as_per_mopng_calculations_as_on_31072020_percent":
        "Promote clean cooking fuel adoption and expand LPG/PNG coverage.",

    # Education
    "schools_with_access_to_basic_infrastructure_such_as_electricity_drinking_water_percent":
        "Improve school infrastructure, electricity access, drinking water, and sanitation facilities.",

    "gross_enrolment_ratio_ger_in_higher_secondary_for_classes_11_to_12":
        "Increase higher secondary school enrollment and retention.",

    "students_in_grade_viii_achieving_atleast_a_minimum_proficiency_level_in_terms_of_nationally_defined_learning_outcomes_to_be_attained_by_the_pupils_at_the_end_of_the_grade_percent":
        "Improve learning outcomes through teacher training and quality education initiatives.",

    "gross_enrolment_ratio_ger_in_higher_education_in_the_age_group_of_18_to_23_years":
        "Increase access to higher education and skill development opportunities.",

    "persons_with_disability_completed_at_least_secondary_education_with_age_15_years_and_above_percent":
        "Strengthen inclusive education and accessibility for persons with disabilities.",

    "average_annual_dropout_rate_at_secondary_level_for_classes_9_to_10":
        "Implement targeted interventions to reduce school dropout rates.",

    # Health
    "maternal_mortality_ratio_per_1_00_000_live_births":
        "Improve maternal healthcare services and institutional deliveries.",

    "human_immunodeficiency_virus_hiv_incidence_per_1_000_uninfected_population":
        "Expand HIV awareness, testing, prevention, and treatment programs.",

    "anaemic_adolescents_in_the_age_group_of_10_to_19_years_percent":
        "Strengthen nutrition programs and iron supplementation initiatives.",

    "mortality_rate_per_1_000_live_births_under_5_years_of_age":
        "Improve child healthcare, immunization, and nutrition services.",

    # Employment & Gender
    "ratio_of_female_to_male_labour_force_participation_rate_lfpr_in_the_age_group_of_15_to_59_years":
        "Promote women's workforce participation and economic empowerment.",

    "labour_force_participation_rate_lfpr_percent_in_the_age_group_of_15_to_59_years":
        "Create employment opportunities and strengthen workforce participation.",

    "operational_land_holding_gender_wise_percentage_of_female_operated_operational_holdings_percent":
        "Promote women's ownership and management of agricultural land and assets.",

    # Environment & Sustainability
    "industries_complying_with_wastewater_treatment_17_categories_of_highly_polluting_industries_or_grossly_polluting_or_red_category_of_industries_complying_with_wastewater_treatment_percent":
        "Improve industrial environmental compliance and wastewater treatment practices.",

    "per_capita_fossil_fuel_consumption":
        "Promote renewable energy adoption and improve energy efficiency.",

    # Safety
    "deaths_due_to_road_accidents_in_urban_areas_per_1_00_000_population":
        "Improve urban road safety infrastructure and traffic management systems.",

    "death_rate_due_to_road_traffic_accidents_per_1_00_000_population":
        "Strengthen road safety awareness, enforcement, and emergency response systems.",

    # Economy
    "gross_value_added_constant_prices_in_agriculture_per_worker":
        "Improve agricultural productivity through technology adoption and farmer support programs."
}


cluster_names = {

    0: "Development Challenge Cluster",

    1: "High Development Cluster",

    2: "North-East Development Cluster",

    3: "Unique Outlier Cluster"
}


master = pd.read_csv(
    "output/SDG_Master_Clustered.csv"
)

top_features = list(
    feature_direction.keys()
)

national_avg = master[
    top_features
].mean()



def generate_state_report(state_name):

    if state_name not in master["state"].values:
        return {
            "error": "State not found"
        }

    state_row = master[
        master["state"] == state_name
    ].iloc[0]

    cluster = int(state_row["cluster"])

    cluster_name = cluster_names[cluster]

    composite_score = state_row[
        "composite_score_of_sdg_india_index"
    ]

    strengths = []
    weaknesses = []
    neutral = []

    for feature in top_features:

        state_value = state_row[feature]
        avg_value = national_avg[feature]

        threshold = avg_value * 0.10

        direction = feature_direction[feature]

        if direction == "positive":

            if state_value > avg_value + threshold:
                strengths.append(feature)

            elif state_value < avg_value - threshold:
                weaknesses.append(feature)

            else:
                neutral.append(feature)

        else:

            if state_value < avg_value - threshold:
                strengths.append(feature)

            elif state_value > avg_value + threshold:
                weaknesses.append(feature)

            else:
                neutral.append(feature)

    strength_details = []

    for feature in strengths:

        strength_details.append({

            "feature": feature,
            "name": feature_names[feature],
            "state_value": round(float(state_row[feature]), 2),
            "india_avg": round(float(national_avg[feature]), 2)

        })

    weakness_details = []

    for feature in weaknesses:

        weakness_details.append({

            "feature": feature,
            "name": feature_names[feature],
            "state_value": round(float(state_row[feature]), 2),
            "india_avg": round(float(national_avg[feature]), 2)

        })

    recommendations = list(
        set(
            recommendation_map[feature]
            for feature in weaknesses
        )
    )

    report = {

        "state": state_name,

        "cluster_id": cluster,

        "cluster": cluster_name,

        "composite_score": round(
            float(composite_score), 2
        ),

        "strength_count": len(strengths),

        "weakness_count": len(weaknesses),

        "neutral_count": len(neutral),

        "strengths": strength_details,

        "weaknesses": weakness_details,

        "recommendations": recommendations

    }

    return report