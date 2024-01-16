from flask import Flask, render_template, request
import csv
import folium
from folium import plugins

app = Flask(__name__)

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data

def write_data_to_file(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

@app.route('/')
def sea_the_waste():
    raw_data = read_data_from_file('data.txt')

    # Enumerate the data to create index and row pairs
    enumerated_data = list(enumerate(raw_data, 1))

    # Create Folium map
    m = folium.Map(location=(48.8555116109269, 2.2986300761024547), zoom_start=10)

    # Create a MarkerCluster
    marker_cluster = plugins.MarkerCluster()

    # Add markers to the MarkerCluster based on your data
    for index, row in enumerated_data:
        # Add a new column for the row number in the table
        row_with_index = [index] + row

        # Create a pin popup with the row number
        popup_content = f"{index}: {row_with_index[4]}"

        marker = folium.Marker(location=(float(row[1]), float(row[2])), popup=popup_content)
        marker.add_to(marker_cluster)

    # Add the MarkerCluster to the map
    marker_cluster.add_to(m)

    # Generate the HTML for the map and pass it to the template
    map_html = m.get_root().render()

    return render_template('index.html', data=enumerated_data, map_html=map_html)

@app.route('/delete_row/<int:position>', methods=['DELETE'])
def delete_row(position):
    data = read_data_from_file('data.txt')

    # Check if the position is valid
    if 1 <= position <= len(data):
        # Remove the row at the specified position
        del data[position - 1]

        # Write the updated data back to the file
        write_data_to_file('data.txt', data)

        return 'Row deleted successfully', 200
    else:
        return 'Invalid position', 400

if __name__ == '__main__':
    app.run()
