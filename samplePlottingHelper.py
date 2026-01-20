import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

def get_figure_size(layout='single', journal_type='cmame'):
    """
    Calculate figure size in inches based on journal specifications.
    
    Parameters
    ----------
    layout : str
        Layout type ('single', 'one_half', 'double', '1x2', '1x3', '2x2', '2x3', '3x2', '3x3').
    journal_type : str
        Journal size or specific journal name ('large' or 'small', or 'cmame').
    
    Returns
    -------
    tuple
        Figure size in inches (width, height).
    """
    mm_to_inches = 1 / 25.4  # Conversion factor from mm to inches

    # Journal-specific dimensions
    if journal_type == 'large':
        single_column = 84 * mm_to_inches  # 84 mm width for single column
        double_column = 174 * mm_to_inches  # 174 mm width for double column
        max_height = 234 * mm_to_inches  # Max height: 234 mm
    elif journal_type == 'small':
        single_column = 119 * mm_to_inches  # 119 mm width for single column
        double_column = 119 * mm_to_inches  # Use single-column width for all
        max_height = 195 * mm_to_inches  # Max height: 195 mm
    elif journal_type == 'cmame':
        # Custom dimensions can be defined here if needed
        single_column = 90 * mm_to_inches
        one_half_column = 140 * mm_to_inches
        double_column = 190 * mm_to_inches
        max_height = 240 * mm_to_inches
    else:
        raise ValueError("For now, journal_type must be 'large' or 'small', or 'cmame'.")

    # Aspect ratio constants
    aspect_ratios = {
        'single': (4, 3),  # Standard 4:3 for single plot
        'one_half': (5, 3), # Wider for one-half column
        'double': (5, 3),   # Wider for double column
        '1x2': (8, 3),     # Wider for 1x2 (16:6 or 8:3)
        '1x3': (12, 3),    # Very wide for 1x3
        '2x2': (4, 4),     # Square for 2x2
        '2x3': (6, 4),     # Moderate height for 2x3
        '3x2': (4, 6),     # Taller for 3x2
        '3x3': (4, 4)      # Square for 3x3
    }

    # Get aspect ratio for the layout
    ratio = aspect_ratios.get(layout, aspect_ratios['single'])
    width, height = ratio

    # Scale width and height to fit the journal's column width
    if layout == 'single':
        width = single_column
    elif layout == 'one_half':
        width = one_half_column
    elif layout == 'double':
        width = double_column
    else:
        width = double_column
    height = (width / ratio[0]) * ratio[1]

    # Ensure height doesn't exceed maximum allowed
    height = min(height, max_height)
    return (width, height)

# Set up matplotlib for publication quality - journal style
def setup_matplotlib_for_publication():
    """Configure matplotlib for publication-quality plots matching journal standards"""
    
    # Use sans-serif fonts as requested by journal
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    rcParams['text.usetex'] = True  # Use matplotlib's math renderer
    
    # Enable better math rendering without LaTeX
    rcParams['mathtext.fontset'] = 'dejavusans'  # Sans-serif math
    
    # Font sizes optimized for journal figures
    rcParams['font.size'] = 7          # Base size (in pt) for general text; tick labels inherit from it unless overridden.
    rcParams['axes.titlesize'] = 10     # Size of each subplot’s title (ax.set_title).
    rcParams['axes.labelsize'] = 7     # Size of the x/y axis label text.
    rcParams['xtick.labelsize'] = 7    # Tick label size along x-axis (Overridden from base font.size)
    rcParams['ytick.labelsize'] = 7    # Tick label size along y-axis (Overridden from base font.size)
    
    # Tick sizes and widths (Major)
    rcParams['xtick.major.width'] = 0.5  # Width of major ticks on x-axis
    rcParams['ytick.major.width'] = 0.5  # Width of major ticks on y-axis
    rcParams['xtick.major.size'] = 2    # Length of major ticks on x-axis
    rcParams['ytick.major.size'] = 2    # Length of major ticks on y-axis
    
    # Tick sizes and widths (Minor)
    # Call ax.minorticks_on() (or plt.minorticks_on() before plotting) to enable minor ticks on both axes. 
    rcParams['xtick.minor.width'] = 0.4  # Width of minor ticks on x-axis
    rcParams['ytick.minor.width'] = 0.4  # Width of minor ticks on y-axis
    rcParams['xtick.minor.size'] = 1    # Length of minor ticks on x-axis
    rcParams['ytick.minor.size'] = 1    # Length of minor ticks on y-axis

    rcParams['legend.handlelength'] = 0.6  # Length of the legend lines
    rcParams['legend.handletextpad'] = 0.4  # Padding between legend handle and text
    rcParams['legend.borderpad'] = 0.2     # Border padding around the legend
    rcParams['legend.fontsize'] = 7    # Legend entry font size
    rcParams['legend.frameon'] = True      # Draw a frame around the legend
    rcParams['legend.fancybox'] = True   # No rounded corners on legend box
    rcParams['legend.framealpha'] = 0.3   # Opaque legend box
    rcParams['legend.title_fontsize'] = 7  # Legend title font size (if legend has a title)
    rcParams['figure.titlesize'] = 10   # Size of a figure-level title (e.g., plt.suptitle).

    # Tick configuration matching journal style
    rcParams['xtick.direction'] = 'in'  # Draw x-axis ticks pointing inward
    rcParams['ytick.direction'] = 'in'  # Draw y-axis ticks pointing inward
    rcParams['xtick.top'] = True        # Mirror x ticks along the top axis
    rcParams['ytick.right'] = True      # Mirror y ticks along the right axis
    
    # Line and marker settings - KEY CHANGES from suggestions
    rcParams['axes.linewidth'] = 0.5           # Width/ thickness of the axis spines—the borders around the plot area.
    rcParams['lines.linewidth'] = 0.75          # Default plotted line width
    rcParams['lines.markersize'] = 1.5         # Default marker size for scatter/line markers
    rcParams['lines.markeredgewidth'] = 0.3    # It controls the thickness of the outline around markers for line plots/scatter. Default is 1.0 pt.
    rcParams['lines.solid_capstyle'] = 'round' # Rounded line caps for smoother appearance
    rcParams['lines.solid_joinstyle'] = 'round' # Rounded joins where line segments meet
    
    # Grid settings - OFF by default like journal figures
    rcParams['grid.linestyle'] = ':'
    rcParams['axes.grid'] = False               # No grid by default
    
    # Higher DPI for crisp rendering
    rcParams['figure.dpi'] = 300
    rcParams['savefig.dpi'] = 600
    rcParams['savefig.bbox'] = 'tight'
    
    # Use TrueType fonts
    rcParams['pdf.fonttype'] = 42
    rcParams['ps.fonttype'] = 42

# Improved color palettes for journal-style plots

# Your custom journal-style colors - diverse, high contrast, professional
JOURNAL_MIXED_COLORS = [
    "#7C1919",  # Fire brick
    '#000080',  # Navy blue
    '#4B0082',  # Indigo
    "#A17E7B",  # Red
    "#490613",  # Crimson
    '#2F4F4F',  # Dark slate gray
    '#8B0000',  # Dark red
    "#117E32",  # Medium Green (neutral)
    '#800080',  # Purple
    "#29507c",  # Cyan (cool)
    "#555151",  # Gray (neutral)
    "#B9503C",  # Brown (warm)
    "#1f77b4",  # Blue (cool)
    "#d62728",  # Red (warm)
    "#706f0c",  # Orange (warm)
]

# Cool-biased version for specific use cases
COOL_JOURNAL_COLORS = [
    "#1f77b4","#377eb8","#4c78a8","#6baed6",
    "#17becf","#76b7b2","#1b9e77","#31a354","#59a14f","#66a61e",
    "#9467bd","#7b6ea8","#984ea3","#8da0cb",
    "#5f9ea0","#2b8cbe","#a6cee3",
    "#636363","#9e9ac8","#bdbdbd",
]

# Balanced set with your custom warm/cool mix
BALANCED_JOURNAL_COLORS = [
    "#7C1919",  # Fire brick
    '#000080',  # Navy blue
    '#4B0082',  # Indigo
    "#A17E7B",  # Red
    "#490613",  # Crimson
    '#2F4F4F',  # Dark slate gray
    '#8B0000',  # Dark red
    "#117E32",  # Medium Green (neutral)
    '#800080',  # Purple
    "#29507c",  # Cyan (cool)
    "#555151",  # Gray (neutral)
    "#B9503C",  # Brown (warm)
    "#1f77b4",  # Blue (cool)
    "#d62728",  # Red (warm)
    "#706f0c",  # Orange (warm)
    "#9467bd",  # Purple (cool)
    "#753022",  # Brown (warm)
    "#17becf",  # Cyan (cool)
    "#e377c2",  # Pink (warm)
    "#555151",  # Gray (neutral)
    "#bcbd22",  # Olive (warm)
    "#377eb8",  # Medium Blue (cool)
    "#ff9896",  # Light Red (warm)
    "#c5b0d5",  # Light Purple (cool)
    "#117E32",  # Medium Green (neutral)
    "#ffbb78",  # Light Orange (warm)
    "#98df8a",  # Light Green (neutral)
    "#c7c7c7",  # Light Gray (neutral)
    "#dbdb8d",  # Light Olive (warm)
    "#9edae5",  # Light Cyan (cool)
    "#b7b8d8"   # Dark Blue (cool)
]

# Atlas24 palette extracted from the atlas24 colormap.
ATLAS24_COLORS = [
    "#458B74",
    "#F5F5DC",
    "#BB3A3A",
    "#005E9D",
    "#C1CDCD",
    "#DEB887",
    "#B1C6ED",
    "#8B8878",
    "#E9967A",
    "#BDB76B",
    "#8B0A50",
    "#313A97",
    "#CAD9BB",
    "#EEC900",
    "#ADD8E6",
    "#6E7B8B",
    "#8B4789",
    "#EEE8AA",
    "#B8CEC6",
    "#B8B8DB",
    "#CEA46B",
    "#6A5ACD",
    "#EEE9E9",
    "#003366",
]

def _get_distinct_colors(n, palette='journal_mixed'):
    """
    Get n distinct colors from curated journal-style palettes.
    
    Parameters
    ----------
    n : int
        Number of colors needed
    palette : str
        'journal_mixed' (default), 'balanced', 'cool', or 'atlas24'
    
    Returns
    -------
    list : Color hex codes
    """
    
    if palette == 'journal_mixed':
        base = JOURNAL_MIXED_COLORS
    elif palette == 'balanced':
        base = BALANCED_JOURNAL_COLORS  
    elif palette == 'cool':
        base = COOL_JOURNAL_COLORS
    elif palette == 'atlas24':
        base = ATLAS24_COLORS
    else:
        # Default to journal_mixed if unknown palette
        base = JOURNAL_MIXED_COLORS
    
    # Extend by repeating if needed
    colors = base * ((n // len(base)) + 1)
    return colors[:n]

def get_journal_style_combinations(n_curves, markevery=7, prefer_open_markers=True,
                                  palette='journal_mixed'):
    """
    Generate journal-style plotting combinations optimized for 15+ curves.
    
    Key features matching journal figures:
    - Open markers with colored edges (default)
    - Sparse marker placement (markevery)
    - Mostly solid lines with strategic dashed/dotted
    - Cool-toned, professional color progression
    
    Parameters
    ----------
    n_curves : int
        Number of curves to plot
    markevery : int
        Place markers every nth point (reduces clutter)
    prefer_open_markers : bool
        Use open markers (facecolor='none') like journal figures
    palette : str
        Color palette: 'cool', 'balanced', 'warm', 'matplotlib'
    method : str
        Color method: 'categorical' or 'cmap'
        
    Returns
    -------
    list of dict : Style dictionaries for plt.plot(**style)
    """
    
    colors = _get_distinct_colors(max(n_curves, 12), palette=palette)
    
    # Marker set: many distinct shapes, readable and printable
    markers = ['o', 's', '^', 'v', 'D', 'P', 'X', 'h', '>', '<', 'p', 
               '1', '2', '3', '4', '8', '*', '+', 'd', '|']
    
    # Line styles: prioritize solid, then add variety
    linestyles_primary = ['-'] * 10     # First 10 are solid
    linestyles_secondary = ['--', '-.', ':', '--', '-.', ':', 
                           '--', '-.', ':', '--']
    
    linestyles = linestyles_primary + linestyles_secondary
    
    # Extend if needed
    if len(linestyles) < n_curves:
        linestyles = (linestyles * ((n_curves // len(linestyles)) + 1))[:n_curves]
    
    styles = []
    for i in range(n_curves):
        color = colors[i]
        marker = markers[i % len(markers)]
        linestyle = linestyles[i]
        
        if prefer_open_markers:
            # Open markers with colored edges - journal style
            mfc = 'none'
            mec = color
        else:
            # Filled markers
            mfc = color
            mec = 'white'
        
        style = {
            'color': color,
            'linestyle': linestyle,
            'marker': marker,
            'markerfacecolor': mfc,
            'markeredgecolor': mec,
            # 'markeredgewidth': 0.9,     # Crisp marker edges
            # 'linewidth': 1.6,           # Thinner than before
            'markevery': markevery,     # Sparse markers
            # 'markersize': 5.0
        }
        
        styles.append(style)
    
    return styles

def get_experimental_style():
    """
    Return style for experimental/reference curve - the 'hero' curve.
    Thick, solid black line, no markers.
    """
    return {
        'color': 'black',
        'linewidth': 1.0,           # Thicker than simulation curves
        'linestyle': '--',
        'marker': None,
        'label': 'Experimental'     # Default label
    }

def plot_multiple_curves_journal_style(x_data, y_data_list, labels, 
                                     xlabel, ylabel, title=None,
                                     include_experimental=False,
                                     x_exp=None, y_exp=None,
                                     markevery=7,
                                     palette='journal_mixed',
                                     figsize=(10, 8),
                                     legend_loc='best',
                                     grid=False):
    """
    Create a publication-quality plot matching journal standards.
    
    Features:
    - Open markers with sparse placement
    - One thick 'hero' experimental curve
    - Colorblind-safe color progression
    - Optimized for 15+ curves
    
    Parameters
    ----------
    x_data : array-like
        X-axis data for simulation curves
    y_data_list : list of array-like
        List of y-data arrays for each simulation curve
    labels : list of str
        Labels for each simulation curve
    xlabel, ylabel : str
        Axis labels
    title : str, optional
        Plot title
    include_experimental : bool
        Whether to include experimental reference curve
    x_exp, y_exp : array-like, optional
        Experimental data (if include_experimental=True)
    markevery : int
        Place markers every nth point
    palette : str
        Color palette: 'journal_mixed' (default), 'balanced', or 'cool'
    figsize : tuple
        Figure size (width, height)
    legend_loc : str
        Legend location
    grid : bool
        Whether to show grid (default False like journal)
        
    Returns
    -------
    fig, ax : matplotlib figure and axes objects
    """
    
    # Apply publication settings
    setup_matplotlib_for_publication()
    
    # Get style combinations for simulation curves
    styles = get_journal_style_combinations(len(y_data_list), 
                                           markevery=markevery, 
                                           prefer_open_markers=True,
                                           palette=palette)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot experimental curve first (if provided) - the 'hero' curve
    if include_experimental and x_exp is not None and y_exp is not None:
        exp_style = get_experimental_style()
        ax.plot(x_exp, y_exp, **exp_style)
    
    # Plot simulation curves with journal styling
    for i, (y_data, label) in enumerate(zip(y_data_list, labels)):
        style = styles[i].copy()
        style['label'] = label  # Add label to style dict
        ax.plot(x_data, y_data, **style)
    
    # Formatting
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    
    # Grid (off by default like journal)
    if grid:
        ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    
    # Legend with journal-style formatting
    legend = ax.legend(loc=legend_loc, frameon=True, fancybox=False, 
                      edgecolor='0.2', handlelength=2.2, 
                      handletextpad=0.6, borderpad=0.6)
    
    # Optimize legend marker sizes (suggested improvement)
    for legend_handle in legend.legend_handles:
        try:
            if hasattr(legend_handle, '_legmarker'):
                legend_handle._legmarker.set_markersize(4)  # Smaller in legend
            legend_handle.set_linewidth(1.6)
        except (AttributeError, Exception):
            pass
    
    # Tight layout
    plt.tight_layout()
    
    return fig, ax

def create_advanced_journal_plot(x_data, y_data_list, labels,
                               xlabel, ylabel, title=None,
                               x_exp=None, y_exp=None,
                               markevery='auto',
                               palette='journal_mixed',
                               even_odd_alternation=False):
    """
    Advanced plotting function with optional refinements for >20 curves.
    
    Parameters
    ----------
    markevery : int or 'auto'
        Marker spacing. If 'auto', scales with data length
    even_odd_alternation : bool
        Use alternating open/filled markers for >16 curves
    """
    
    setup_matplotlib_for_publication()
    
    n_curves = len(y_data_list)
    
    # Auto-calculate markevery based on data density
    if markevery == 'auto':
        if isinstance(x_data, (list, tuple)):
            avg_length = sum(len(x) for x in x_data) / len(x_data)
        else:
            avg_length = len(x_data)
        markevery = max(5, int(avg_length // 60))
    
    # For >16 curves, use alternating marker styles
    if n_curves > 16 and even_odd_alternation:
        # First 16: open markers, solid lines
        styles_1 = get_journal_style_combinations(16, markevery, 
                                                prefer_open_markers=True,
                                                palette=palette)
        # Remaining: filled markers, dashed lines  
        styles_2 = get_journal_style_combinations(n_curves - 16, markevery,
                                                prefer_open_markers=False,
                                                palette=palette)
        # Force dashed lines for second group
        for style in styles_2:
            if style['linestyle'] == '-':
                style['linestyle'] = '--'
        
        styles = styles_1 + styles_2
    else:
        styles = get_journal_style_combinations(n_curves, markevery, 
                                              palette=palette)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 9))  # Larger for many curves
    
    # Experimental curve
    if x_exp is not None and y_exp is not None:
        exp_style = get_experimental_style()
        ax.plot(x_exp, y_exp, **exp_style)
    
    # Simulation curves
    for i, (y_data, label) in enumerate(zip(y_data_list, labels)):
        style = styles[i].copy()
        style['label'] = label
        ax.plot(x_data, y_data, **style)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    
    # Multi-column legend for many curves
    ncol = 1 if n_curves <= 8 else 2 if n_curves <= 16 else 3
    legend = ax.legend(loc='best', frameon=True, fancybox=False,
                      edgecolor='0.2', ncol=ncol, fontsize=10)
    
    plt.tight_layout()
    return fig, ax

# Example usage demonstrating the improved functions
def example_journal_style():
    """Demonstrate the journal-style plotting functions"""
    
    # Generate sample data similar to stress-strain curves
    x = np.linspace(0, 20, 200)
    x_exp = np.linspace(0, 20, 180)  # Experimental with different sampling
    
    # Experimental curve (noisy, realistic)
    y_exp = 60 * (1 - np.exp(-x_exp * 0.15)) * np.exp(-x_exp * 0.08) + \
            np.random.normal(0, 3, len(x_exp))
    
    # Multiple simulation curves with variations
    y_data_list = []
    labels = []
    
    for i in range(15):
        # Vary parameters systematically
        amplitude = 50 + i * 2
        growth_rate = 0.12 + i * 0.008
        decay_rate = 0.06 + i * 0.004
        
        y = amplitude * (1 - np.exp(-x * growth_rate)) * np.exp(-x * decay_rate)
        y_data_list.append(y)
        
        # Create realistic parameter labels
        k_val = 10 + i * 5
        labels.append(f'K={k_val}N/mm²')
    
    # Create the journal-style plot with mixed color palette
    fig, ax = plot_multiple_curves_journal_style(
        x, y_data_list, labels,
        xlabel='Displacement (mm)',
        ylabel='Load (N)',
        title='Multi-Parameter Analysis',
        include_experimental=True,
        x_exp=x_exp,
        y_exp=y_exp,
        markevery=8,  # Sparse markers
        palette='journal_mixed',  # Use your custom color palette
        figsize=(10, 8)
    )
    
    plt.show()
    return fig, ax

# Alternative: even more curves with advanced function
def example_many_curves():
    """Demonstrate plotting 20+ curves"""
    
    x = np.linspace(0, 15, 150)
    y_data_list = []
    labels = []
    
    for i in range(20):
        y = (40 + i * 1.5) * np.sin(x * 0.5 + i * 0.1) * np.exp(-x * 0.1)
        y_data_list.append(y)
        labels.append(f'Series {i+1}')
    
    fig, ax = create_advanced_journal_plot(
        x, y_data_list, labels,
        xlabel='Time (s)',
        ylabel='Response',
        markevery='auto',
        palette='balanced',  # Try balanced palette for variety
        method='categorical',
        even_odd_alternation=True
    )
    
    plt.show()
    return fig, ax

if __name__ == "__main__":
    # Run the example
    example_journal_style()
