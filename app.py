from flask import Flask, render_template, request, url_for
from serpapi import GoogleSearch
import pandas as pd
import requests
import os

app = Flask(__name__)

def upload_image_to_imgbb(image_path, api_key):
    url = "https://api.imgbb.com/1/upload"
    files = {"image": (image_path, open(image_path, "rb"))}
    params = {"key": api_key}
    
    response = requests.post(url, files=files, params=params)
    data = response.json()
    
    return data.get("data", {}).get("url")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                image_filename = file.filename
                image_path = os.path.join(image_folder, image_filename)
                file.save(image_path)
                
                api_key = "c827337aeafb1373739e432865f88e0f"
                url = upload_image_to_imgbb(image_path, api_key)
                
                if url:
                    params = {
                        "engine": "google_lens",
                        "url": url,
                        "no_cache": "true",
                        "api_key": "f85ddacb9bd8e32cbeafe8d2cc5b1d5ae736577cca325f776a4a7912a1d1418f",
                    }

                    search = GoogleSearch(params)
                    results = search.get_dict()

                    name_price_url = []

                    if results['search_metadata']['status'] != "Success":
                        print("No item found")
                    else:
                        for item in results['visual_matches']:
                            name_price_url.append({
                                "source": item.get('source'),
                                "title": item.get('title'),
                                "link": item.get('link'),
                                "price": item['price'].get('extracted_value') if 'price' in item else None,
                                "currency": item['price'].get('currency') if 'price' in item else None,
                                "thumbnail": item.get('thumbnail')  # Store the thumbnail URL for display
                            })

                    df = pd.DataFrame(name_price_url)
                    filtered_df = df[df['link'].notnull() & df['currency'].notnull()]
                    filtered_df = filtered_df.sort_values(by='price').reset_index(drop=True)
                    filtered_df = filtered_df[["source", "link", "price", "thumbnail"]]  # Include thumbnail

                    # Save CSV (optional)
                    filtered_df.to_csv("results.csv", index=False)

                    # Pass image URL for rendering
                    return render_template('index.html', data=filtered_df.to_dict('records'), image_url=url_for('static', filename=f'uploads/{image_filename}'))
                else:
                    return "Error uploading image... retry again :)"
        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html', data=[])

image_folder = "static/uploads"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

if __name__ == '__main__':
    app.run(debug=True)
