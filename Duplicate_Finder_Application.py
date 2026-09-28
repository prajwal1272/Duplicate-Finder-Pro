import pandas as pd
from io import BytesIO


OUTPUT_FILE = None


def process_file(file):

    filename = file.filename.lower()


    # CSV handling (20 lakh limit)
    if filename.endswith(".csv"):

        df = pd.read_csv(file)

        if len(df) > 2000000:
            raise ValueError(
                "CSV file too large. Maximum 20 lakh records allowed."
            )


    # Excel handling (small files only)
    else:

        df = pd.read_excel(
            file,
            engine="openpyxl"
        )

        if len(df) > 500000:
            raise ValueError(
                "Excel file too large. Please upload CSV for large data."
            )



    # Column cleanup
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



    current_columns = list(df.columns)


    missing_columns = [
        col for col in required_columns
        if col not in current_columns
    ]



    extra_columns = [
        col for col in current_columns
        if col not in required_columns
    ]



    errors = []


    if missing_columns:

        errors.append(
            f"Missing columns: {', '.join(missing_columns)}"
        )


    if extra_columns:

        errors.append(
            f"Extra columns found: {', '.join(extra_columns[:10])}"
        )



    if errors:

        raise ValueError(
            "Invalid file format. " + " | ".join(errors)
        )



    # Clean data

    for col in required_columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
        )



    # Duplicate removal

    final_data = df.drop_duplicates(

        subset=[
            "Client Code",
            "CID",
            "Campaign Name",
            "Domain"
        ],

        keep="first"

    )



    # Sorting

    final_data = final_data.sort_values(

        by=[
            "Client Code",
            "CID",
            "Campaign Name",
            "Domain"
        ]

    )



    # Output Excel memory

    output = BytesIO()


    final_data.to_excel(

        output,

        index=False

    )


    output.seek(0)



    return {


        "total": len(df),

        "clean": len(final_data),

        "duplicate": len(df) - len(final_data),

        "cid": df["CID"].nunique(),

        "domain": df["Domain"].nunique(),

        "client": df["Client Code"].nunique(),

        "file": output

    }