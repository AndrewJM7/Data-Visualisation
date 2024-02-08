import pandas as pd
import numpy as np
from fancyimpute import IterativeImputer

# Excel life index
input_file_path = 'OECD_betterLifeIndex.xlsx'

# Read the Excel file
df = pd.read_excel(input_file_path)

# Get the columns from D9 to AA50
numerical_columns = df.iloc[8:, 3:50]

# Replace ".." with NaN in the selected columns
numerical_columns = numerical_columns.replace("..", np.nan)

# Initialize the MICE imputer
imputer = IterativeImputer(max_iter=500, random_state=0)

# Perform imputation with MICE on the selected columns
numerical_columns_imputed = imputer.fit_transform(numerical_columns)

# Round the imputed values to 1 decimal place
numerical_columns_imputed_rounded = np.round(numerical_columns_imputed, 1)

# Update the original DataFrame with imputed and rounded values
df.iloc[8:, 3:51] = numerical_columns_imputed_rounded

# Specify the path for the new Excel file
output_file_path = 'OECD_betterLifeIndex_imputed.xlsx'

# Save the modified DataFrame to the new Excel file
df.to_excel(output_file_path, index=False)

print(f"Modified data (imputed and rounded) saved to {output_file_path}")

