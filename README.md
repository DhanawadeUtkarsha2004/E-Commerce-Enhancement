#Author

Utkarsha Dhanawade

# Image Search Web App

This is a simple Flask-based web application that allows users to upload an image, perform a Google Lens search, and display search results in a tabular format. The search results include the source, link, and price of related items.

## Features

- Upload an image from your local device.
- Utilize Google Lens to search for similar items.
- Display search results with source, link, and price in a tabular format.
- Clickable links to view the original items.


## Usage

1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run the Flask app by executing `python app.py`.
4. Access the web app in your browser at `http://localhost:5000`.
5. Upload an image and click the "Search" button.
6. View the search results with source, link, and price.

## Dependencies

- Flask
- pandas
- requests

## File Structure

- `app.py`: Main Flask application.
- `index.html`: HTML template for rendering the web page.
- `style.css`: CSS file for styling the web page.
- `requirements.txt`: List of required Python packages.
- `uploads/`: Folder to store uploaded images.
- `results.csv`: CSV file containing search results data.

