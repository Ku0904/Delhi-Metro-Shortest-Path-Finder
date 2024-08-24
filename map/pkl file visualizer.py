import os
import pickle
import networkx as nx
import matplotlib.pyplot as plt

def load_and_visualize(file_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the file
    file_path = os.path.join(script_dir, file_name)
    
    print(f"Attempting to load file from: {file_path}")
    
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    
    G = nx.Graph(data)
    
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    nx.draw(G, pos, 
            node_color='lightblue',
            node_size=300,
            font_size=6,
            font_weight='bold',
            width=0.3,
            with_labels=True)
    
    plt.title("Delhi Metro Station Map", fontsize=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        load_and_visualize('og_station_map.pkl')
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
        print(f"Current script directory: {os.path.dirname(os.path.abspath(__file__))}")
        print("Contents of the directory:")
        for item in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            print(f"  - {item}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")