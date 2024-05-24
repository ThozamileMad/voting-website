import matplotlib.pyplot as plt


class ResultsChart:
    def __init__(self, parties, vote_calcs, colors):
        self.parties = parties
        self.vote_calcs = vote_calcs
        self.colors = colors

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

