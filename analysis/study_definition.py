from datalab_cohorts import StudyDefinition, patients, codelist_from_csv, codelist


## CODE LISTS
# All codelist are held within the codelist/ folder.

chronic_respiratory_disease_codes = codelist_from_csv(
    "codelists/chronic_respiratory_disease.csv", system="ctv3", column="CTV3ID"
)

asthma_codes = codelist_from_csv(
    "codelists/asthma_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

salbutamol_codes = codelist_from_csv(
    "codelists/sabutamol_asthma.csv", system="snomed", column="id"
)

ics_codes = codelist_from_csv(
    "codelists/ics_asthma.csv", system="snomed", column="id"
)

chronic_cardiac_disease_codes = codelist_from_csv(
    "codelists/chronic_cardiac_disease.csv", system="ctv3", column="CTV3ID"
)

diabetes_codes = codelist_from_csv(
    "codelists/diabetes_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

lung_cancer_codes = codelist_from_csv(
    "codelists/lung_cancer_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

haem_cancer_codes = codelist_from_csv(
    "codelists/haematological_cancer_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

other_cancer_codes = codelist_from_csv(
    "codelists/other_cancer_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

bone_marrow_transplant_codes = codelist_from_csv(
    "codelists/bone_marrow_transplant_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

chemo_radio_therapy_codes = codelist_from_csv(
    "codelists/chemo_radio_therapy_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

chronic_liver_disease_codes = codelist_from_csv(
    "codelists/chronic_liver_disease.csv", system="ctv3", column="CTV3ID"
)
gi_bleed_and_ulcer_codes = codelist_from_csv(
    "codelists/gi_bleed_and_ulcer.csv", system="ctv3", column="CTV3ID"
)
inflammatory_bowel_disease_codes = codelist_from_csv(
    "codelists/inflammatory_bowel_disease.csv", system="ctv3", column="CTV3ID"
)

organ_transplant_codes = codelist_from_csv(
    "codelists/organ_transplant.csv", system="ctv3", column="CTV3ID"
)

spleen_codes = codelist_from_csv(
    "codelists/spleen_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

sickle_cell_codes = codelist_from_csv(
    "codelists/sickle_cell_2020-04-16.csv", system="ctv3", column="CTV3ID"
)

ra_sle_psoriasis_codes = codelist_from_csv(
    "codelists/ra_sle_psoriasis.csv", system="ctv3", column="CTV3ID"
)

systolic_blood_pressure_codes = codelist(["2469."], system="ctv3")
diastolic_blood_pressure_codes = codelist(["246A."], system="ctv3")

## STUDY POPULATION
# Defines both the study population and points to the important covariates

study = StudyDefinition(
    # This line defines the study population
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),

    # Outcomes
    icu=patients.admitted_to_icu(
        on_or_after="2020-02-01", include_day=True, include_admission_date=True
    ),

    # The rest of the lines define the covariates with associated GitHub issues
    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/33
    age=patients.age_as_of("2020-02-01"),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/46
    sex=patients.sex(),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/52
    imd=patients.address_as_of(
        "2020-02-01", returning="index_of_multiple_deprivation", round_to_nearest=100
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/37
    rural_urban=patients.address_as_of(
        "2020-02-01", returning="rural_urban_classification"
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/54
    geographic_area=patients.registered_practice_as_of("2020-02-01", returning="stp_code"),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/10
    bmi=patients.most_recent_bmi(
        on_or_after="2010-02-01",
        minimum_age_at_measurement=16,
        include_measurement_date=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/6
    #smoking_status= # still to be implemented

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/27
    #ethnicity= # still to be implemented - this will be just the Read code for now then can be categorised with the list we're making.

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/21
    chronic_respiratory_disease=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/55
    asthma=patients.satisfying(
        """recent_asthma_code OR (asthma_code_ever AND NOT copd_code_ever AND (recent_salbutamol_count >= 3 OR recent_ics))""",
        recent_asthma_code=patients.with_these_clinical_events(
            asthma_codes,
            between=['2018-02-01', '2020-02-01']
        ),
        asthma_code_ever=patients.with_these_clinical_events(asthma_codes),
        copd_code_ever=patients.with_these_clinical_events(chronic_respiratory_disease_codes),
        recent_salbutamol_count=patients.with_these_medications(
            salbutamol_codes,
            between=['2018-02-01', '2020-02-01'],
            returning="number_of_matches_in_period"
        ),
        recent_ics=patients.with_these_medications(
            ics_codes,
            between=['2018-02-01', '2020-02-01'],
        )
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/7
    chronic_cardiac_disease=patients.with_these_clinical_events(
        chronic_cardiac_disease_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/30
    diabetes=patients.with_these_clinical_events(
        diabetes_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/32
    lung_cancer=patients.with_these_clinical_events(
        lung_cancer_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),
    haem_cancer=patients.with_these_clinical_events(
        haem_cancer_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),
    other_cancer=patients.with_these_clinical_events(
        other_cancer_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),
    bone_marrow_transplant=patients.with_these_clinical_events(
        bone_marrow_transplant_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),
    chemo_radio_therapy=patients.with_these_clinical_events(
        chemo_radio_therapy_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),

    # # https://github.com/ebmdatalab/tpp-sql-notebook/issues/12
    chronic_liver_disease=patients.with_these_clinical_events(
        chronic_liver_disease_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/14
    neurological_condition=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes, #################################### CHANGE TO CORRECT CODELIST WHEN READY ####################################
        return_first_date_in_period=True,
        include_month=True,
    ),

    # # Chronic kidney disease
    # # https://github.com/ebmdatalab/tpp-sql-notebook/issues/17
    # egfr=patients.with_these_clinical_events(
    #     egfr_codes,
    #     find_last_match_in_period=True,
    #     on_or_before="2020-02-01",
    #     returning="numeric_value",
    #     include_date_of_match=True
    #     include_month=True,
    # ),
    dialysis=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes, #################################### CHANGE TO CORRECT CODELIST WHEN READY ####################################
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/31
    organ_transplant=patients.with_these_clinical_events(
        organ_transplant_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/13
    dysplenia=patients.with_these_clinical_events(
        spleen_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),
    sickle_cell=patients.with_these_clinical_events(
        sickle_cell_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/36
    aplastic_anaemia=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes, #################################### CHANGE TO CORRECT CODELIST WHEN READY ####################################
        return_first_date_in_period=True,
        include_month=True,
    ),
    hiv=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes, #################################### CHANGE TO CORRECT CODELIST WHEN READY ####################################
        return_first_date_in_period=True,
        include_month=True,
    ),
    genetic_immunodeficiency=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes, #################################### CHANGE TO CORRECT CODELIST WHEN READY ####################################
        return_first_date_in_period=True,
        include_month=True,
    ),
    immunosuppression_nos=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes, #################################### CHANGE TO CORRECT CODELIST WHEN READY ####################################
        return_first_date_in_period=True,
        include_month=True,
    ),

    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/23
    #immunosuppressant_med=

    # Blood pressure
    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/35
    bp_sys=patients.mean_recorded_value(
        systolic_blood_pressure_codes,
        on_most_recent_day_of_measurement=True,
        on_or_before="2020-02-01",
        include_measurement_date=True,
        include_month=True,
    ),
    bp_dias=patients.mean_recorded_value(
        diastolic_blood_pressure_codes,
        on_most_recent_day_of_measurement=True,
        on_or_before="2020-02-01",
        include_measurement_date=True,
        include_month=True,
    ),

    # # https://github.com/ebmdatalab/tpp-sql-notebook/issues/49
    ra_sle_psoriasis=patients.with_these_clinical_events(
        ra_sle_psoriasis_codes,
        return_first_date_in_period=True,
        include_month=True,
    ),
    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/51
    gi_bleed_and_ulcer=patients.with_these_clinical_events(
        gi_bleed_and_ulcer_codes,
        return_first_date_in_period=True,
        include_month=True
    ),
    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/50
    inflammatory_bowel_disease=patients.with_these_clinical_events(
        inflammatory_bowel_disease_codes,
        return_first_date_in_period=True,
        include_month=True
    ),
)
