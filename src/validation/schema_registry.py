from datetime import datetime

CURRENT_YEAR = datetime.now().year


SCHEMAS = {

    "companies": {

        "primary_key": ["id"],

        "required_columns": [
            "id",
            "company_name"
        ],

        "dq_rules": [
            "dataset_not_empty",
            "required_columns_present",
            "no_duplicate_columns",
            "primary_key_not_null",
            "primary_key_unique",
            "company_name_not_null",
            "company_name_not_blank",
            "website_valid"
        ]
    },

    "analysis": {

        "primary_key": ["id"],

        "foreign_key": {
            "column": "company_id",
            "reference_table": "companies",
            "reference_column": "id"
        },

        "required_columns": [
            "id",
            "company_id",
            "roe"
        ],

        "dq_rules": [
            "dataset_not_empty",
            "required_columns_present",
            "primary_key_not_null",
            "primary_key_unique",
            "foreign_key_valid",
            "roe_numeric",
            "roe_reasonable_range"
        ]
    },

    "balancesheet": {

        "primary_key": ["id"],

        "foreign_key": {
            "column": "company_id",
            "reference_table": "companies",
            "reference_column": "id"
        },

        "required_columns": [
            "id",
            "company_id",
            "year",
            "total_assets",
            "total_liabilities"
        ],

        "dq_rules": [
            "dataset_not_empty",
            "required_columns_present",
            "primary_key_not_null",
            "primary_key_unique",
            "foreign_key_valid",
            "year_valid",
            "total_assets_non_negative",
            "total_liabilities_non_negative"
        ]
    },

    "cashflow": {

        "primary_key": ["id"],

        "foreign_key": {
            "column": "company_id",
            "reference_table": "companies",
            "reference_column": "id"
        },

        "required_columns": [
            "id",
            "company_id",
            "year",
            "net_cash_flow"
        ],

        "dq_rules": [
            "dataset_not_empty",
            "required_columns_present",
            "primary_key_not_null",
            "primary_key_unique",
            "foreign_key_valid",
            "year_valid",
            "net_cash_flow_numeric"
        ]
    },

    "documents": {

        "primary_key": ["id"],

        "foreign_key": {
            "column": "company_id",
            "reference_table": "companies",
            "reference_column": "id"
        },

        "required_columns": [
            "id",
            "company_id",
            "year",
            "annual_report"
        ],

        "dq_rules": [
            "dataset_not_empty",
            "required_columns_present",
            "primary_key_not_null",
            "primary_key_unique",
            "foreign_key_valid",
            "year_valid",
            "annual_report_not_null"
        ]
    },

    "profitandloss": {

        "primary_key": ["id"],

        "foreign_key": {
            "column": "company_id",
            "reference_table": "companies",
            "reference_column": "id"
        },

        "required_columns": [
            "id",
            "company_id",
            "year",
            "sales",
            "net_profit"
        ],

        "dq_rules": [
            "dataset_not_empty",
            "required_columns_present",
            "primary_key_not_null",
            "primary_key_unique",
            "foreign_key_valid",
            "year_valid",
            "sales_non_negative",
            "net_profit_numeric"
        ]
    },

    "prosandcons": {

        "primary_key": ["id"],

        "foreign_key": {
            "column": "company_id",
            "reference_table": "companies",
            "reference_column": "id"
        },

        "required_columns": [
            "id",
            "company_id"
        ],

        "dq_rules": [
            "dataset_not_empty",
            "required_columns_present",
            "primary_key_not_null",
            "primary_key_unique",
            "foreign_key_valid",
            "pros_or_cons_present"
        ]
    }
}


DQ_RULES = {

    1: "dataset_not_empty",
    2: "required_columns_present",
    3: "no_duplicate_columns",
    4: "primary_key_not_null",
    5: "primary_key_unique",
    6: "foreign_key_valid",
    7: "year_valid",
    8: "company_name_not_null",
    9: "company_name_not_blank",
    10: "website_valid",
    11: "roe_numeric",
    12: "roe_reasonable_range",
    13: "total_assets_non_negative",
    14: "total_liabilities_non_negative",
    15: "sales_non_negative",
    16: "pros_or_cons_present"
}