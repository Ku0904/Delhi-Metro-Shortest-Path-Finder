from tkinter import *
from tkinter import ttk
from collections import defaultdict
from tkinter import messagebox
import webbrowser
import pickle
import sys
import time

class Graph(object):
    def __init__(self):
        f=open('station_map',"rb")
        self.a=pickle.load(f)
        self.b=pickle.load(f)
        self.graph =self.a
        self.station=[]
        self.distance=0

    def BFS(self,s,f):
        visited = [False] * (len(self.graph))
        queue=[]
        dist=[None]*(len(self.graph))
        pred=[None]*(len(self.graph))
        queue.append(s)
        visited[s]=True
        dist[s]=0
        s1=s

        # Clear previous visualization
        canvas.delete("all")
        
        # Add a legend to the canvas
        canvas.create_rectangle(800, 20, 825, 45, fill="lightgray")
        canvas.create_text(835, 32.5, text="Unvisited", anchor="w")
        canvas.create_rectangle(800, 50, 825, 75, fill="yellow")
        canvas.create_text(835, 62.5, text="Current", anchor="w")
        canvas.create_rectangle(800, 80, 825, 105, fill="blue")
        canvas.create_text(835, 92.5, text="Visited", anchor="w")
        canvas.create_rectangle(800, 110, 825, 135, fill="green")
        canvas.create_text(835, 122.5, text="Path", anchor="w")

        # Create pixels for each station
        station_pixels = {}
        for i, station in self.b.items():
            x = (i % 25) * 30 + 50
            y = (i // 25) * 30 + 180
            station_pixels[i] = canvas.create_rectangle(x, y, x+25, y+25, fill="lightgray")
            canvas.create_text(x+12.5, y+12.5, text=str(i), font=("Arial", 8))

        while queue:
            s = queue.pop(0)
            canvas.itemconfig(station_pixels[s], fill="yellow")  # Current station
            canvas.create_text(400, 750, text=f"Processing station {s}", font=("Arial", 14), tags="status")
            main_window.update()
            time.sleep(0.5)  # Slow down visualization

            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
                    dist[i]=dist[s]+1
                    pred[i]=s
                    canvas.itemconfig(station_pixels[i], fill="blue")  # Visited station
                    canvas.delete("status")
                    canvas.create_text(400, 750, text=f"Visiting station {i}", font=("Arial", 14), tags="status")
                    main_window.update()
                    time.sleep(0.2)  # Slow down visualization
                    if i==f:
                        p=pred[i]
                        self.distance=dist[i]
                        self.station.append(self.b[f])
                        while p!=s1:
                            self.station.append(self.b[p])
                            p=pred[p]
                        else:
                            self.station.append(self.b[s1])
                        break

        # Highlight the final path
        canvas.delete("status")
        canvas.create_text(400, 750, text="Highlighting the shortest path", font=("Arial", 14), tags="status")
        for station in reversed(self.station):
            station_index = list(self.b.keys())[list(self.b.values()).index(station)]
            canvas.itemconfig(station_pixels[station_index], fill="green")
            main_window.update()
            time.sleep(0.5)  # Slow down visualization

main_window = Tk()
main_window.title("DELHI METRO")
main_window.geometry("1920x1080")
main_window.configure(background="lightgray")

topside = LabelFrame(main_window, bd=2, bg="#0032FF")
topside.pack(side=TOP, fill=X, pady=10, padx=5)

img = PhotoImage(file=r"logo.png")

photo_lable=Label(topside, image=img, bg="white")
photo_lable.pack(side=LEFT)

text_label = Label(topside, text="DELHI METRO ROUTE FINDER", font=("Arial", 30), fg="white", bg="#0032FF")
text_label.pack(side=LEFT, padx=30)

input_frame = LabelFrame(main_window, text="Input", font=("Arial", 16), bg="lightgray")
input_frame.place(x=20, y=100, height=200, width=450)

start = Label(input_frame, text="SOURCE", font=("Arial", 16), fg="black", bg="lightgray")
start.grid(row=0, column=0, padx=10, pady=20)
value1 = StringVar()
combo1 = ttk.Combobox(input_frame, width=20, font=("Arial", 14), height=10, textvariable=value1, state='readonly', justify='center')
combo1['values']=['Select Station','AIIMS Yellow Line', 'ANVT Pink Line', 'Adarsh Nagar Yellow Line', 'Arjan Garh Yellow Line', 'Arthala Red Line', 'Ashram Pink Line', 'Azadpur', 'Badarpur Violet Line', 'Badkal Mor Violet Line', 'Bata Chownk Violet Line', 'Bhikaji Cama Place Pink Line', 'Central Secretariat', 'Chandhni Chowk Yellow Line', 'Chawri Bazar Yellow Line', 'Chhattarpur Yellow Line', 'Civil Lines Yellow Line', 'Delhi Cantt Pink Line', 'Delhi Gate Violet Line', 'Dilshad Garden Red Line', 'Durgabai Deshmukh South Campus Pink Line', 'ESI Hospital Pink Line', 'East Azad Nagar Pink Line', 'Escorts Mujesar Violet Line', 'Faridabad Old Violet Line', 'GTB Nagar Yellow Line', 'Ghotorni Yellow Line', 'Gokulpuri Pink Line', 'Govindpuri Violet Line', 'Green Park Yellow Line', 'Gurudronacharya Yellow Line', 'Haiderpur Badli Mor Yellow Line', 'Hauz Khas Yellow Line', 'Hazrat Nizamuddin Pink Line', 'Hindon Red Line', 'Huda City Centre Yellow Line', 'IFFCO Chowk Yellow Line', 'INA', 'IP Extension Pink Line', 'ITO Violet Line', 'Inder Lok Red Line', 'JLN Violet Line', 'Jaffrabad Pink Line', 'Jahangirpuri Yellow Line', 'Jama Masjid Violet Line', 'Jangpura Violet Line', 'Janpath Violet Line', 'Jasola-Apollo Violet Line', 'Jhil Mil Red Line', 'Johri Enclave Pink Line', 'Jorbagh Yellow Line', 'Kailash Colony Violet Line', 'Kalkaji Mandir Violet Line', 'Kanhaiya Nagar Red Line', 'Karkarduma Court Pink Line', 'Karkarduma Pink Line', 'Kashmere Gate', 'Keshav Puram Red Line', 'Khan Market Violet Line', 'Kohat Enclave Red Line', 'Krishna Nagar Pink Line', 'Lajpat Nagar', 'Lal Quila Violet Line', 'Lok Kalyan Marg Yellow Line', 'MG Road Yellow Line', 'Majlis Park Pink Line', 'Major Mohit Sharma Red Line', 'Malvia Nagar Yellow Line', 'Mandawali - West Vinod Nagar Pink Line', 'Mandi House Violet Line', 'Mansarovar Park Red Line', 'Maujpur Pink Line', 'Maya Puri Pink Line', 'Mayur Vihar 1 Pink Line', 'Mayur Vihar Pocket 1 Pink Line', 'Mewla Maharajpur Violet Line', 'Model Town Yellow Line', 'Mohan Estate Violet Line', 'Mohan Nagar Red Line', 'Moolchand Violet Line', 'NHPC Chownk Violet Line', 'Naraina Vihar Pink Line', 'Neelam Chownk Ajronda Violet Line', 'Nehru Place Violet Line', 'Netaji Subhash Place', 'New Delhi Yellow Line', 'Okhla Violet Line', 'Patel Chowk Yellow Line', 'Pitam Pura Red Line', 'Pratap Nagar Red Line', 'Pul Bangash Red Line', 'Punjabi Bagh West Pink Line', 'Qutab Minar Yellow Line', 'Raj Bagh Red Line', 'Raja Nahar singh marg Violet Line', 'Rajiv Chowk Yellow Line', 'Rajouri Garden Pink Line', 'Rithala Red Line', 'Rohini East Red Line', 'Rohini Sector 18, 19 Yellow Line', 'Rohini West Red Line', 'Saket Yellow Line', 'Samaypur Badli Yellow Line', 'Sant Surdas Violet Line', 'Sarai Violet Line', 'Sarita Vihar Violet Line', 'Sarojini Nagar Pink Line', 'Sector 28 Violet Line', 'Seelampur Red Line', 'Shahdara Red Line', 'Shaheed Nagar Red Line', 'Shaheed Sthal(New Bus Adda) Red Line', 'Shakurpur Pink Line', 'Shalimar Bagh Pink Line', 'Shastri Nagar Red Line', 'Shastri Park Red Line', 'Shiv Vihar Pink Line', 'Shyam park Red Line', 'Sikandarpur. Yellow Line', 'Sir Vishweshwaraiah Moti Bagh Pink Line', 'South Extension Pink Line', 'Sultanpur Yellow Line', 'Tis Hazari Red Line', 'Trilokpuri Sanjay Lake Pink Line', 'Tuglakabad Violet Line', 'Udyog Bhawan Yellow Line', 'Vidhan Sabha Yellow Line', 'Vinobapuri Pink Line', 'Vinod Nagar East Pink Line', 'Viswavidyalaya Yellow Line', 'Welcome']
combo1.current(0)
combo1.grid(row=0, column=1, padx=10, pady=20)

dest = Label(input_frame, text="DESTINATION", font=("Arial", 16), fg="black", bg="lightgray")
dest.grid(row=1, column=0, padx=10, pady=20)
value2 = StringVar()
combo2 = ttk.Combobox(input_frame, width=20, font=("Arial", 14), height=10, textvariable=value2, state='readonly', justify='center')
combo2['values']=['Select Station','AIIMS Yellow Line', 'ANVT Pink Line', 'Adarsh Nagar Yellow Line', 'Arjan Garh Yellow Line', 'Arthala Red Line', 'Ashram Pink Line', 'Azadpur', 'Badarpur Violet Line', 'Badkal Mor Violet Line', 'Bata Chownk Violet Line', 'Bhikaji Cama Place Pink Line', 'Central Secretariat', 'Chandhni Chowk Yellow Line', 'Chawri Bazar Yellow Line', 'Chhattarpur Yellow Line', 'Civil Lines Yellow Line', 'Delhi Cantt Pink Line', 'Delhi Gate Violet Line', 'Dilshad Garden Red Line', 'Durgabai Deshmukh South Campus Pink Line', 'ESI Hospital Pink Line', 'East Azad Nagar Pink Line', 'Escorts Mujesar Violet Line', 'Faridabad Old Violet Line', 'GTB Nagar Yellow Line', 'Ghotorni Yellow Line', 'Gokulpuri Pink Line', 'Govindpuri Violet Line', 'Green Park Yellow Line', 'Gurudronacharya Yellow Line', 'Haiderpur Badli Mor Yellow Line', 'Hauz Khas Yellow Line', 'Hazrat Nizamuddin Pink Line', 'Hindon Red Line', 'Huda City Centre Yellow Line', 'IFFCO Chowk Yellow Line', 'INA', 'IP Extension Pink Line', 'ITO Violet Line', 'Inder Lok Red Line', 'JLN Violet Line', 'Jaffrabad Pink Line', 'Jahangirpuri Yellow Line', 'Jama Masjid Violet Line', 'Jangpura Violet Line', 'Janpath Violet Line', 'Jasola-Apollo Violet Line', 'Jhil Mil Red Line', 'Johri Enclave Pink Line', 'Jorbagh Yellow Line', 'Kailash Colony Violet Line', 'Kalkaji Mandir Violet Line', 'Kanhaiya Nagar Red Line', 'Karkarduma Court Pink Line', 'Karkarduma Pink Line', 'Kashmere Gate', 'Keshav Puram Red Line', 'Khan Market Violet Line', 'Kohat Enclave Red Line', 'Krishna Nagar Pink Line', 'Lajpat Nagar', 'Lal Quila Violet Line', 'Lok Kalyan Marg Yellow Line', 'MG Road Yellow Line', 'Majlis Park Pink Line', 'Major Mohit Sharma Red Line', 'Malvia Nagar Yellow Line', 'Mandawali - West Vinod Nagar Pink Line', 'Mandi House Violet Line', 'Mansarovar Park Red Line', 'Maujpur Pink Line', 'Maya Puri Pink Line', 'Mayur Vihar 1 Pink Line', 'Mayur Vihar Pocket 1 Pink Line', 'Mewla Maharajpur Violet Line', 'Model Town Yellow Line', 'Mohan Estate Violet Line', 'Mohan Nagar Red Line', 'Moolchand Violet Line', 'NHPC Chownk Violet Line', 'Naraina Vihar Pink Line', 'Neelam Chownk Ajronda Violet Line', 'Nehru Place Violet Line', 'Netaji Subhash Place', 'New Delhi Yellow Line', 'Okhla Violet Line', 'Patel Chowk Yellow Line', 'Pitam Pura Red Line', 'Pratap Nagar Red Line', 'Pul Bangash Red Line', 'Punjabi Bagh West Pink Line', 'Qutab Minar Yellow Line', 'Raj Bagh Red Line', 'Raja Nahar singh marg Violet Line', 'Rajiv Chowk Yellow Line', 'Rajouri Garden Pink Line', 'Rithala Red Line', 'Rohini East Red Line', 'Rohini Sector 18, 19 Yellow Line', 'Rohini West Red Line', 'Saket Yellow Line', 'Samaypur Badli Yellow Line', 'Sant Surdas Violet Line', 'Sarai Violet Line', 'Sarita Vihar Violet Line', 'Sarojini Nagar Pink Line', 'Sector 28 Violet Line', 'Seelampur Red Line', 'Shahdara Red Line', 'Shaheed Nagar Red Line', 'Shaheed Sthal(New Bus Adda) Red Line', 'Shakurpur Pink Line', 'Shalimar Bagh Pink Line', 'Shastri Nagar Red Line', 'Shastri Park Red Line', 'Shiv Vihar Pink Line', 'Shyam park Red Line', 'Sikandarpur. Yellow Line', 'Sir Vishweshwaraiah Moti Bagh Pink Line', 'South Extension Pink Line', 'Sultanpur Yellow Line', 'Tis Hazari Red Line', 'Trilokpuri Sanjay Lake Pink Line', 'Tuglakabad Violet Line', 'Udyog Bhawan Yellow Line', 'Vidhan Sabha Yellow Line', 'Vinobapuri Pink Line', 'Vinod Nagar East Pink Line', 'Viswavidyalaya Yellow Line', 'Welcome']
combo2.current(0)
combo2.grid(row=1, column=1, padx=10, pady=20)

def print_route(arr_sta, dis):
    route_window = Toplevel(main_window)
    route_window.title("Route Details")
    route_window.geometry("400x600+760+240")  # Positioned over the visualization

    route_frame = Frame(route_window, bg="white")
    route_frame.pack(fill=BOTH, expand=True)

    scrollbar = Scrollbar(route_frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    listbox = Listbox(route_frame, bd=2, bg="white", fg="black", font=("Arial", 12), yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    listbox.insert(END, f"Total Stations: {dis}")
    listbox.insert(END, "")
    listbox.insert(END, "Route:")
    for i, station in enumerate(reversed(arr_sta), 1):
        listbox.insert(END, f"{i}. {station}")

    listbox.pack(fill=BOTH, expand=TRUE)

def find_route(s,d):
    g = Graph()
    dict_station = g.b
    try:
        for i in range(len(dict_station)):
            if dict_station[i] == s:
                s_index = i
            elif dict_station[i] == d:
                d_index = i
        g.BFS(s_index, d_index)
        print_route(g.station, g.distance)
    except:
        messagebox.showinfo("Error", "Please select valid stations", icon="warning")

def click_me():
    source = value1.get()
    destination = value2.get()
    find_route(source, destination)

def exit_window():
    sys.exit()

def openlink():
    webbrowser.open_new("https://delhimetrorail.info/delhi-metro-map")

button_frame = LabelFrame(main_window, text="Actions", font=("Arial", 16), bg="lightgray")
button_frame.place(x=20, y=320, height=200, width=450)

click_button = Button(button_frame, text="Find Route", width=20, font=("Arial", 14), command=click_me)
click_button.pack(pady=10)

link_button = Button(button_frame, text="View Metro Map", width=20, font=("Arial", 14), command=openlink)
link_button.pack(pady=10)

exit_button = Button(button_frame, text="Exit", width=20, font=("Arial", 14), command=exit_window)
exit_button.pack(pady=10)

# Create a frame for the visualization
vis_frame = LabelFrame(main_window, text="BFS Algorithm Visualization", font=("Arial", 16), bg="white")
vis_frame.place(x=500, y=100, height=900, width=1400)

# Create a canvas inside the visualization frame
canvas = Canvas(vis_frame, width=1380, height=860, bg="white")
canvas.pack(padx=10, pady=10)

main_window.mainloop()