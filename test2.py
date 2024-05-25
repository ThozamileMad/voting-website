import matplotlib.pyplot as plt

parties = ['Party A', 'Party B', 'Party C']
votes = [350, 240, 180]

# Calculate percentages
total_votes = sum(votes)
percentages = [vote / total_votes for vote in votes]

# Define colors for each pie chart
colors = ['skyblue', 'lightgreen', 'lightcoral']

# Generate and save a chart for each party
for i, (party, percentage) in enumerate(zip(parties, percentages)):
    # Create a figure and axis
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})

    # Create a pie chart with a single wedge
    ax.pie([percentage, 1 - percentage], colors=[colors[i], 'white'], startangle=90, wedgeprops=dict(width=0.3))

    # Add a filled circle in the center with a thinner width
    centre_circle = plt.Circle((0, 0), 0.25, fc='white')
    ax.add_artist(centre_circle)

    # Add the percentage in the center with bigger and bolder font
    ax.text(0, 0, f'{percentage * 100:.1f}%', horizontalalignment='center', verticalalignment='center',
            fontsize=32, fontweight='bold')

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    # Save each pie chart as an image with transparent background
    plt.savefig(f'{party}_chart.png', transparent=True)

    # Close the figure to avoid displaying it
    plt.close(fig)

# Display message indicating completion
print("Charts have been saved.")



