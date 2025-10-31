# CODE IS DIRECTLY FROM GEMINI
# AI generated code is usually quite bad
# but AI is quite good with simple data analysis with python
# Therefore it is used in this instance


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import scienceplots
plt.style.use(['science','ieee'])


# --- 1. Data Preparation ---

# Data from the uploaded image
data = {
    'Type of UAA': [
        'Arable land', 'Forage plants', 'Potatoes', 'Vegetables in the open', 
        'Other', 'Fallow land', 
        'Permanent crops', 'Fruit and berry plantations', 'Citrus plantations', 
        'Olive plantations', 'Vineyards', 'Nurseries', 'Kitchen gardens'
    ],
    'Total land (ha)': [
        7782, 5251, 570, 1090, 146, 725, 
        953, 228, 107, 154, 456, 8, 1995
    ]
}
df = pd.DataFrame(data)

# --- 2. Define Groups and Calculate Totals ---

# Group 1: Crops and Cultivation (High-intensity/Annual)
group1_components = [
    'Arable land', 'Forage plants', 'Potatoes', 'Vegetables in the open', 
    'Other'
]
group1_name = 'Crops \& Cultivation'

# Group 2: Permanent Plantations (Trees/Vines/Bushes)
group2_components = [
    'Permanent crops', 'Fruit and berry plantations', 'Citrus plantations', 
    'Olive plantations', 'Vineyards', 'Nurseries'
]
group2_name = 'Permanent Plantations'

# Group 3: Other Use (Fallow/Small Scale)
group3_components = [
    'Fallow land', 'Kitchen gardens'
]
group3_name = 'Other UAA'

# List of all groups for the central chart
main_groups = [group1_name, group2_name, group3_name]
group_components = [group1_components, group2_components, group3_components]
group_data_subsets = []
group_sums = []

for components in group_components:
    subset = df[df['Type of UAA'].isin(components)]
    group_data_subsets.append(subset)
    group_sums.append(subset['Total land (ha)'].sum())

total_sum = sum(group_sums)


# --- 3. Plotting Setup ---

# Create a figure with a 2x2 grid for the four charts
fig = plt.figure(figsize=(15, 12))
# Use GridSpec to define the layout: 2 rows, 2 columns
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Define colors for the three main categories
main_colors = plt.cm.Set1([0, 1, 2]) # e.g., Red, Blue, Green

# Assign subplots to the grid
ax_central = fig.add_subplot(gs[0, 0])  # Top-Left for the main chart
ax_g1 = fig.add_subplot(gs[0, 1])       # Top-Right for Group 1
ax_g2 = fig.add_subplot(gs[1, 0])       # Bottom-Left for Group 2
ax_g3 = fig.add_subplot(gs[1, 1])       # Bottom-Right for Group 3


# --- 4. Central Pie Chart (The Three Parts) ---

ax_central.pie(
    group_sums, 
    labels=[f'{name}\n({s:,} ha)' for name, s in zip(main_groups, group_sums)],
    colors=main_colors,
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1}
)
ax_central.set_title(
    f'Overview: Three Main Categories\n(Total: {total_sum:,} ha)', 
    fontsize=16, 
    fontweight='bold'
)


# --- 5. Detail Pie Charts (The Sub-Divisions) ---

# Function to plot the detailed charts
def plot_detail_chart(ax, subset, group_name, base_color):
    sizes = subset['Total land (ha)'].tolist()
    labels = subset['Type of UAA'].tolist()
    
    # Generate shades of the base color for sub-components
    color_map = plt.cm.get_cmap('Pastel2')
    sub_colors = color_map(np.linspace(0, 1, len(sizes))) # Use a consistent palette

    ax.pie(
        sizes, 
        labels=[f'{l}\n({s:,} ha)' for l, s in zip(labels, sizes)],
        autopct='%1.1f%%',
        startangle=90,
        colors=sub_colors,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.5},
        textprops={'fontsize': 8}
    )
    ax.set_title(f'Breakdown: {group_name}', fontsize=14, fontweight='bold', color='black')


# Plot Group 1 Breakdown
plot_detail_chart(ax_g1, group_data_subsets[0], group1_name, main_colors[0])

# Plot Group 2 Breakdown
plot_detail_chart(ax_g2, group_data_subsets[1], group2_name, main_colors[1])

# Plot Group 3 Breakdown
plot_detail_chart(ax_g3, group_data_subsets[2], group3_name, main_colors[2])


# --- 6. Finalization ---

fig.suptitle("Hierarchical Land Use (UAA) Distribution", fontsize=18, y=1.02)
dir_path = os.path.dirname(os.path.realpath(__file__))

plt.savefig(os.path.join(dir_path, "land_distribution.svg"))