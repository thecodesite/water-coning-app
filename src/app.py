import pandas as pd
import streamlit as st
from utils.calculations import (
    meyer_gardner,
    chaperson,
    schols,
    muskat_wyckoff,
    sobocinski_cornelius
)
def process_uploaded_file(file):
    # Read the uploaded Excel file
    df = pd.read_excel(file)

    # Ensure required columns are present
    required_columns = [
        "Well", "hp (feet)", "h (feet)", "kho (mD)", "kvo (mD)", 
        "Oil visc (cP)", "Bo (bbl/STB)", "re (feet)", "rw (feet)", 
        "Oil den (lb/feet3)", "Water den (lb/feet3)"
    ]
    if not all(col in df.columns for col in required_columns):
        st.error("Uploaded file is missing required columns.")
        return None

    # Add columns for results
    df["Meyer & Gardner"] = df.apply(
        lambda row: meyer_gardner(
            row["kho (mD)"], row["h (feet)"], row["hp (feet)"], 
            row["Oil visc (cP)"], row["Bo (bbl/STB)"], row["re (feet)"], 
            row["rw (feet)"], row["Oil den (lb/feet3)"], row["Water den (lb/feet3)"]
        ), axis=1
    )
    df["Chaperson"] = df.apply(
        lambda row: chaperson(
            row["kho (mD)"], row["kvo (mD)"], row["h (feet)"], 
            row["hp (feet)"], row["Oil visc (cP)"], row["Bo (bbl/STB)"], 
            row["Water den (lb/feet3)"], row["Oil den (lb/feet3)"], row["re (feet)"]
        ), axis=1
    )
    df["Schols"] = df.apply(
        lambda row: schols(
            row["kho (mD)"], row["h (feet)"], row["hp (feet)"], 
            row["Oil visc (cP)"], row["rw (feet)"], row["re (feet)"], 
            row["Water den (lb/feet3)"], row["Oil den (lb/feet3)"], row["Bo (bbl/STB)"]
        ), axis=1
    )
    df["Muskat & Wyckoff"] = df.apply(
        lambda row: muskat_wyckoff(
            row["kho (mD)"], row["h (feet)"], row["hp (feet)"], 
            row["Oil visc (cP)"], row["re (feet)"], row["Water den (lb/feet3)"], 
            row["Oil den (lb/feet3)"], row["Bo (bbl/STB)"], row["rw (feet)"]
        ), axis=1
    )

    return df

def main():
    st.title("Water Coning Critical Flow Rate Calculator")

    method = st.selectbox("Select Calculation Method", [
        "Meyer & Gardner",
        "Chaperson",
        "Schols",
        "Muskat & Wyckoff",
        "Sobocinski & Cornelius"
    ])

    st.sidebar.header("Input Parameters")

    if method == "Meyer & Gardner":
        ko = st.sidebar.number_input("Effective Permeability (ko) [mD]", value=93.5)
        h = st.sidebar.number_input("Formation Thickness (h) [ft]", value=40.0)
        hp = st.sidebar.number_input("Perforated Thickness (hp) [ft]", value=15.0)
        mu = st.sidebar.number_input("Fluid Viscosity (mu) [cP]", value=0.73)
        Bo = st.sidebar.number_input("Oil Volume Factor (Bo) [bbl/STB]", value=1.1)
        re = st.sidebar.number_input("Drainage Radius (re) [ft]", value=660.0)
        rw = st.sidebar.number_input("Well Radius (rw) [ft]", value=0.25)
        Deno = st.sidebar.number_input("Oil Density (Deno) [lb/ft³]", value=47.5)
        Denw = st.sidebar.number_input("Water Density (Denw) [lb/ft³]", value=63.76)

    elif method == "Chaperson":
        kh = st.sidebar.number_input("Horizontal Permeability (kh) [mD]", value=100.0)
        kv = st.sidebar.number_input("Vertical Permeability (kv) [mD]", value=10.0)
        h = st.sidebar.number_input("Formation Thickness (h) [ft]", value=50.0)
        hp = st.sidebar.number_input("Perforated Thickness (hp) [ft]", value=15.0)
        mu = st.sidebar.number_input("Fluid Viscosity (mu) [cP]", value=0.73)
        Bo = st.sidebar.number_input("Oil Volume Factor (Bo) [bbl/STB]", value=1.1)
        Denw = st.sidebar.number_input("Water Density (Denw) [lb/ft³]", value=63.76)
        Deno = st.sidebar.number_input("Oil Density (Deno) [lb/ft³]", value=47.5)
        re = st.sidebar.number_input("Drainage Radius (re) [ft]", value=1000.0)

    elif method == "Schols":
        ko = st.sidebar.number_input("Effective Permeability (ko) [mD]", value=93.0)
        h = st.sidebar.number_input("Formation Thickness (h) [ft]", value=50.0)
        hp = st.sidebar.number_input("Perforated Thickness (hp) [ft]", value=15.0)
        mu = st.sidebar.number_input("Fluid Viscosity (mu) [cP]", value=0.73)
        Bo = st.sidebar.number_input("Oil Volume Factor (Bo) [bbl/STB]", value=1.1)
        re = st.sidebar.number_input("Drainage Radius (re) [ft]", value=1000.0)
        rw = st.sidebar.number_input("Well Radius (rw) [ft]", value=0.25)
        Deno = st.sidebar.number_input("Oil Density (Deno) [lb/ft³]", value=47.5)
        Denw = st.sidebar.number_input("Water Density (Denw) [lb/ft³]", value=63.76)

    elif method == "Muskat & Wyckoff":
        ko = st.sidebar.number_input("Effective Permeability (ko) [mD]", value=93.0)
        h = st.sidebar.number_input("Formation Thickness (h) [ft]", value=50.0)
        hp = st.sidebar.number_input("Perforated Thickness (hp) [ft]", value=15.0)
        mu = st.sidebar.number_input("Fluid Viscosity (mu) [cP]", value=0.73)
        rw = st.sidebar.number_input("Well Radius (rw) [ft]", value=0.25)
        re = st.sidebar.number_input("Drainage Radius (re) [ft]", value=1000.0)
        Deno = st.sidebar.number_input("Oil Density (Deno) [lb/ft³]", value=47.5)
        Denw = st.sidebar.number_input("Water Density (Denw) [lb/ft³]", value=63.76)
        Bo = st.sidebar.number_input("Oil Volume Factor (Bo) [bbl/STB]", value=1.1)

    elif method == "Sobocinski & Cornelius":
        kh = st.sidebar.number_input("Horizontal Permeability (kh) [mD]", value=93.0)
        kv = st.sidebar.number_input("Vertical Permeability (kv) [mD]", value=9.0)
        h = st.sidebar.number_input("Formation Thickness (h) [ft]", value=50.0)
        hp = st.sidebar.number_input("Perforated Thickness (hp) [ft]", value=15.0)
        mu = st.sidebar.number_input("Fluid Viscosity (mu) [cP]", value=0.73)
        rw = st.sidebar.number_input("Well Radius (rw) [ft]", value=0.25)
        re = st.sidebar.number_input("Drainage Radius (re) [ft]", value=1000.0)
        Denw = st.sidebar.number_input("Water Density (Denw) [lb/ft³]", value=63.76)
        Deno = st.sidebar.number_input("Oil Density (Deno) [lb/ft³]", value=47.5)
        Bo = st.sidebar.number_input("Oil Volume Factor (Bo) [bbl/STB]", value=1.1)
        Qo = st.sidebar.number_input("Oil Flow Rate (Qo) [STB/d]", value=250.0)
        kro = st.sidebar.number_input("Relative Permeability to Oil (kro)", value=1.0)
        krw = st.sidebar.number_input("Relative Permeability to Water (krw)", value=1.0)
        mw = st.sidebar.number_input("Water Viscosity (mw) [cP]", value=1.0)
        phi = st.sidebar.number_input("Porosity (phi)", value=0.13)

    if st.button("Run"):
        if method == "Meyer & Gardner":
            result = meyer_gardner(ko, h, hp, mu, Bo, re, rw, Deno, Denw)
            st.success(f"Critical Flow Rate (Qoc): {result:.2f} (STB/d)")
        elif method == "Chaperson":
            result = chaperson(kh, kv, h, hp, mu, Bo, Denw, Deno, re)
            st.success(f"Critical Flow Rate (Qoc): {result:.2f} (STB/d)")
        elif method == "Schols":
            result = schols(ko, h, hp, mu, rw, re, Denw, Deno, Bo)
            st.success(f"Critical Flow Rate (Qoc): {result:.2f} (STB/d)")
        elif method == "Muskat & Wyckoff":
            result = muskat_wyckoff(ko, h, hp, mu, re, Denw, Deno, Bo, rw)
            st.success(f"Critical Flow Rate (Qoc): {result:.2f} (STB/d)")
        elif method == "Sobocinski & Cornelius":
            Tbt, Qoc = sobocinski_cornelius(kh, h, hp, mu, rw, re, Denw, Deno, Bo, Qo, kro, krw, mw, phi, kv)
            st.success(f"Critical Flow Rate (Qoc): {Qoc:.2f} (STB/d), Time W: {Tbt:.2f} (days)")
    st.header("Batch Processing via Excel File")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if uploaded_file:
        df = process_uploaded_file(uploaded_file)
        if df is not None:
            st.success("File processed successfully!")
            
            # Display the dataframe
            st.dataframe(df)

            # Download link for the processed file
            output_file = "processed_results.xlsx"
            df.to_excel(output_file, index=False)
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Results",
                    data=f,
                    file_name="processed_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # Generate bar chart
            st.subheader("Bar Chart of Results")
            chart_data = df.melt(
                id_vars=["Well"], 
                value_vars=["Meyer & Gardner", "Chaperson", "Schols", "Muskat & Wyckoff"],
                var_name="Method", value_name="Critical Flow Rate"
            )
            fig, ax = plt.subplots(figsize=(10, 6))
            for well, group in chart_data.groupby("Well"):
                ax.bar(group["Method"], group["Critical Flow Rate"], label=well)
            ax.set_ylabel("Critical Flow Rate (STB/d)")
            ax.set_title("Critical Flow Rate by Method")
            ax.legend(title="Well")
            st.pyplot(fig)

    # Add the copyright message at the bottom
    st.markdown(
        '<div style="text-align: center; font-size: small; color: gray;">'
        'Contact: Jose Perez Garcia (www.linkedin.com/in/perezjgg)'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
