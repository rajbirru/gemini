import matplotlib.pyplot as plt
import numpy as np
import io

def create_gradient_bar(stock_percentage, bond_percentage):
    fig, ax = plt.subplots(figsize=(8, 1))
    
    # Create the gradient
    gradient = np.linspace(0, 1, 100).reshape(1, -1)
    ax.imshow(gradient, extent=[0, 100, 0, 1], cmap='RdYlGn', aspect='auto')
    
    # Add stock and bond percentages
    ax.axvline(stock_percentage, color='black', linewidth=1)
    ax.text(stock_percentage/2, 0.5, f"Stocks: {stock_percentage}%", ha='center', va='center', color='white')
    ax.text((stock_percentage + 100)/2, 0.5, f"Bonds: {bond_percentage}%", ha='center', va='center', color='black')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
    buffer.seek(0)
    
    return buffer