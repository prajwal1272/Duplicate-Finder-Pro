import pandas as pd
from io import BytesIO


OUTPUT_FILE = None


MAX_CSV_ROWS = 2000000   # 20 lakh limit


def process_file(file):


    filename = file.filename.lower()



    # ==========================
    # READ FILE
    # ==========================


    if filename.endswith(".csv"):


        df = pd.read_csv(file)



        if len(df) > MAX_CSV_ROWS:

            raise ValueError(
                "CSV file too large. Maximum 20 lakh records allowed."
            )



    elif filename.endswith((".xlsx", ".xls")):


        df = pd.read_excel(
            file,
            engine="openpyxl"
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
    # OUTPUT FILE
    # ==========================


    output = BytesIO()



    # Large data CSV
    if len(final_data) > 900000:


        final_data.to_csv(

            output,

            index=False,

            encoding="utf-8-sig"

        )


        file_type = "csv"



    # Small data Excel
    else:


        final_data.to_excel(

            output,

            index=False,

            engine="openpyxl"

        )


        file_type = "xlsx"




    output.seek(0)





    return {


        "total": len(df),


        "clean": len(final_data),


        "duplicate": len(df) - len(final_data),


        "cid": df["CID"].nunique(),


        "domain": df["Domain"].nunique(),


        "client": df["Client Code"].nunique(),


        "file": output,


        "file_type": file_type


    }