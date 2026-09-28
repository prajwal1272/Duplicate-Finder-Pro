import pandas as pd
import tempfile
import os


MAX_CSV_ROWS = 2000000


def process_file(file):

    filename = file.filename.lower()


    # ==========================
    # READ FILE
    # ==========================

    if filename.endswith(".csv"):

        df = pd.read_csv(
            file,
            dtype=str,
            low_memory=False
        )


        if len(df) > MAX_CSV_ROWS:

            raise ValueError(
                "CSV file too large. Maximum 20 lakh records allowed."
            )


    elif filename.endswith((".xlsx", ".xls")):

        df = pd.read_excel(
            file,
            engine="openpyxl",
            dtype=str
        )


    else:

        raise ValueError(
            "Only CSV and Excel files are allowed."
        )
    # ==========================
    # COLUMN CLEANUP
    # ==========================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )



    required_columns = [

        "Client Code",
        "CID",
        "Campaign Name",
        "Domain"

    ]



    missing_columns = [

        col for col in required_columns
        if col not in df.columns

    ]


    if missing_columns:

        raise ValueError(
            f"Missing columns: {', '.join(missing_columns)}"
        )



    # ==========================
    # CLEAN DATA
    # ==========================

    for col in required_columns:

        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )



    # ==========================
    # REMOVE DUPLICATES
    # ==========================

    final_data = df.drop_duplicates(

        subset=[

            "Client Code",
            "CID",
            "Campaign Name",
            "Domain"

        ],

        keep="first"

    )



    # ==========================
    # SORT DATA
    # ==========================

    final_data = final_data.sort_values(

        by=[

            "Client Code",
            "CID",
            "Campaign Name",
            "Domain"

        ]

    )


    # ==========================
    # CREATE OUTPUT FILE
    # ==========================


    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    )


    output_path = temp_file.name

    temp_file.close()


    final_data.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )


    file_type = "csv"



    # ==========================
    # RETURN RESULT
    # ==========================


    return {

        "total": len(df),

        "clean": len(final_data),

        "duplicate": len(df) - len(final_data),

        "cid": df["CID"].nunique(),

        "domain": df["Domain"].nunique(),

        "client": df["Client Code"].nunique(),

        "file": output_path,

        "file_type": file_type

    }