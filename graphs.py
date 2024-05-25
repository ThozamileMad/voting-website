import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class ResultsChart:
    def __init__(self, parties, vote_calcs, colors):
        self.parties = parties
        self.vote_calcs = vote_calcs
        self.colors = colors
        self.percentages = 0
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = 'Roboto'

    def make_bar_chart(self):
        # Create horizontal bar chart
        fig, ax = plt.subplots()
        bars = ax.barh(self.parties, self.vote_calcs, height=0.5, edgecolor='black', linewidth=0, color=self.colors)

        # Add value labels at the end of each bar
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2, f'{width} ({width / sum(self.vote_calcs) * 100:.1f}%)',
                    va='center')

        # Remove the top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Adjust spacing between bars
        ax.xaxis.set_tick_params(pad=10)

        # Make the party names lighter
        ax.set_yticklabels(self.parties, fontweight='light')

        # save to static/images
        fig.savefig("./static/images/bar_chart.jpeg", bbox_inches='tight')

    def make_pie_charts(self):
        # Calculate percentages
        total_votes = sum(self.vote_calcs)
        percentages = [vote / total_votes for vote in self.vote_calcs]
        self.percentages = percentages[::-1]

        # Generate and save a chart for each party
        for i, (party, percentage) in enumerate(zip(self.parties, percentages)):
            # Create a figure and axis
            fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})

            # Create a pie chart with a single wedge
            ax.pie([percentage, 1 - percentage], colors=[self.colors[i], 'white'], startangle=90, wedgeprops=dict(width=0.3))

            # Add a filled circle in the center with a thinner width
            centre_circle = plt.Circle((0, 0), 0.25, fc='white')
            ax.add_artist(centre_circle)

            # Add the percentage in the center with bigger and bolder font
            ax.text(0, 0, f'{percentage * 100:.1f}%', horizontalalignment='center', verticalalignment='center',
                    fontsize=32, fontweight='bold')

            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')

            # Save each pie chart as an image with transparent background
            plt.savefig(f'./static/images/{party.split()[-1].lower()}_pie_chart.jpeg', transparent=True)

            # Close the figure to avoid displaying it
            plt.close(fig)